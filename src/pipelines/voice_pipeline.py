from resemblyzer import VoiceEncoder, preprocess_wav

import numpy as np
import io
import librosa
import streamlit as st


# =========================================================
# CONFIGURATION
# =========================================================

VOICE_MATCH_THRESHOLD = 0.65
MIN_SPEECH_DURATION = 0.5
SILENCE_TOP_DB = 30


# =========================================================
# VOICE ENCODER
# =========================================================

@st.cache_resource
def load_voice_encoder():

    return VoiceEncoder()


# =========================================================
# CREATE VOICE EMBEDDING
# =========================================================

def get_voice_embedding(audio_bytes):

    try:

        if not audio_bytes:
            return None

        encoder = load_voice_encoder()

        audio, sr = librosa.load(
            io.BytesIO(audio_bytes),
            sr=16000,
            mono=True
        )

        if len(audio) == 0:
            return None

        # Reject invalid audio
        if not np.all(np.isfinite(audio)):
            return None

        wav = preprocess_wav(audio)

        if len(wav) == 0:
            return None

        embedding = encoder.embed_utterance(wav)

        norm = np.linalg.norm(embedding)

        if norm < 1e-10:
            return None

        # Normalize embedding
        embedding = embedding / norm

        return embedding.tolist()

    except Exception as e:

        st.error(
            f"Voice recognition error: {str(e)}"
        )

        return None


# =========================================================
# IDENTIFY SPEAKER
# =========================================================

def identify_speaker(
    new_embedding,
    candidates_dict,
    threshold=VOICE_MATCH_THRESHOLD
):

    if new_embedding is None:
        return None, 0.0

    if not candidates_dict:
        return None, 0.0

    # Convert new embedding
    new_embedding = np.asarray(
        new_embedding,
        dtype=np.float32
    )

    # Validate new embedding
    if not np.all(
        np.isfinite(new_embedding)
    ):
        return None, 0.0

    new_norm = np.linalg.norm(
        new_embedding
    )

    if new_norm < 1e-10:
        return None, 0.0

    new_embedding = (
        new_embedding / new_norm
    )

    best_sid = None
    best_score = -1.0

    # Compare against every enrolled student
    for sid, stored_embedding in candidates_dict.items():

        if stored_embedding is None:
            continue

        stored_embedding = np.asarray(
            stored_embedding,
            dtype=np.float32
        )

        # Validate stored embedding
        if not np.all(
            np.isfinite(stored_embedding)
        ):
            continue

        stored_norm = np.linalg.norm(
            stored_embedding
        )

        if stored_norm < 1e-10:
            continue

        # Normalize stored embedding
        stored_embedding = (
            stored_embedding / stored_norm
        )

        # Cosine similarity
        similarity = float(
            np.dot(
                new_embedding,
                stored_embedding
            )
        )

        # Keep highest similarity
        if similarity > best_score:

            best_score = similarity
            best_sid = sid

    # Accept only if similarity passes threshold
    if (
        best_sid is not None
        and best_score >= threshold
    ):

        return best_sid, best_score

    return None, best_score


# =========================================================
# PROCESS CLASSROOM AUDIO
# =========================================================

def process_bulk_audio(
    audio_bytes,
    candidates_dict,
    threshold=VOICE_MATCH_THRESHOLD
):

    try:

        if not audio_bytes:
            return {}

        if not candidates_dict:
            return {}

        encoder = load_voice_encoder()

        # -------------------------------------------------
        # Load classroom recording
        # -------------------------------------------------

        audio, sr = librosa.load(
            io.BytesIO(audio_bytes),
            sr=16000,
            mono=True
        )

        if len(audio) == 0:
            return {}

        # Reject invalid audio
        if not np.all(
            np.isfinite(audio)
        ):
            return {}

        # -------------------------------------------------
        # Detect speech segments
        # -------------------------------------------------

        segments = librosa.effects.split(
            audio,
            top_db=SILENCE_TOP_DB
        )

        identified_results = {}

        # -------------------------------------------------
        # Process every speech segment
        # -------------------------------------------------

        for start, end in segments:

            segment_length = end - start

            # Ignore very short segments
            if segment_length < (
                sr * MIN_SPEECH_DURATION
            ):
                continue

            segment_audio = audio[
                start:end
            ]

            if len(segment_audio) == 0:
                continue

            # -------------------------------------------------
            # Create embedding
            # -------------------------------------------------

            wav = preprocess_wav(
                segment_audio
            )

            if len(wav) == 0:
                continue

            embedding = encoder.embed_utterance(
                wav
            )

            norm = np.linalg.norm(
                embedding
            )

            if norm < 1e-10:
                continue

            # Normalize
            embedding = (
                embedding / norm
            )

            # -------------------------------------------------
            # Identify speaker
            # -------------------------------------------------

            sid, score = identify_speaker(
                embedding,
                candidates_dict,
                threshold
            )

            # -------------------------------------------------
            # Store best score for each student
            # -------------------------------------------------

            if sid is not None:

                if (
                    sid not in identified_results
                    or score > identified_results[sid]
                ):

                    identified_results[sid] = score

        return identified_results

    except Exception as e:

        st.error(
            f"Bulk voice processing error: {str(e)}"
        )

        return {}