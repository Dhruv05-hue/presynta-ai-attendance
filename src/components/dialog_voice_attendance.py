import streamlit as st

from src.pipelines.voice_pipeline import process_bulk_audio
from src.database.config import supabase
from datetime import datetime
import pandas as pd

from src.components.dialog_attendance_result import show_attendance_result


@st.dialog("Voice Attendance")
def voice_attendance_dialog(selected_subject_id):

    # =========================================================
    # INITIALIZE SESSION STATE
    # =========================================================

    if "voice_attendance_results" not in st.session_state:
        st.session_state.voice_attendance_results = None

    # =========================================================
    # HEADER / DESCRIPTION
    # =========================================================

    st.write(
        "Record audio of students saying 'I am present'. "
        "Then AI will recognize them."
    )

    audio_data = st.audio_input(
        "Record classroom audio"
    )

    # =========================================================
    # ANALYZE AUDIO
    # =========================================================

    if st.button(
        "Analyze Audio",
        width="stretch",
        type="primary"
    ):

        # -----------------------------------------------------
        # 1. VALIDATE AUDIO
        # -----------------------------------------------------

        if not audio_data:

            st.warning(
                "Please record classroom audio first."
            )

            return

        audio_bytes = audio_data.read()

        if not audio_bytes:

            st.warning(
                "No audio data was recorded. "
                "Please try again."
            )

            return

        # Clear previous analysis
        st.session_state.voice_attendance_results = None

        # -----------------------------------------------------
        # 2. PROCESS
        # -----------------------------------------------------

        with st.spinner("Processing audio..."):

            # =================================================
            # 2. GET ENROLLED STUDENTS
            # =================================================

            try:

                enrolled_res = (
                    supabase
                    .table("subject_students")
                    .select("*, students(*)")
                    .eq(
                        "subject_id",
                        selected_subject_id
                    )
                    .execute()
                )

            except Exception as e:

                st.error(
                    f"Could not load enrolled students: {str(e)}"
                )

                return

            enrolled_students = enrolled_res.data

            if not enrolled_students:

                st.warning(
                    "No students enrolled in this course."
                )

                return

            # =================================================
            # 3. BUILD VOICE CANDIDATES
            # =================================================

            candidates_dict = {}

            for node in enrolled_students:

                student = node.get("students")

                if not student:
                    continue

                student_id = student.get("student_id")
                voice_embedding = student.get("voice_embedding")

                if (
                    student_id
                    and voice_embedding
                ):

                    candidates_dict[student_id] = (
                        voice_embedding
                    )

            if not candidates_dict:

                st.error(
                    "No enrolled students have voice profiles registered."
                )

                return

            # =================================================
            # 4. RUN VOICE RECOGNITION
            # =================================================

            try:

                detected_scores = process_bulk_audio(
                    audio_bytes,
                    candidates_dict
                )

            except Exception as e:

                st.error(
                    f"Voice analysis failed: {str(e)}"
                )

                return

            if not detected_scores:

                st.warning(
                    "No enrolled student voices were recognized "
                    "in the recording."
                )

            # =================================================
            # 5. GENERATE ATTENDANCE RESULTS
            # =================================================

            results = []
            attendance_to_log = []

            current_timestamp = (
                datetime.now()
                .strftime("%Y-%m-%dT%H:%M:%S")
            )

            for node in enrolled_students:

                student = node.get("students")

                if not student:
                    continue

                student_id = student.get(
                    "student_id"
                )

                student_name = student.get(
                    "name",
                    "Unknown"
                )

                score = detected_scores.get(
                    student_id,
                    0.0
                )

                # process_bulk_audio()
                # already applies the voice threshold.
                #
                # Therefore, if the student exists
                # in detected_scores, the voice was
                # accepted by the recognition pipeline.

                is_present = (
                    student_id in detected_scores
                )

                results.append(
                    {
                        "Name": student_name,

                        "ID": student_id,

                        "Source": (
                            f"{score:.2f}"
                            if is_present
                            else "-"
                        ),

                        "Status": (
                            "✅ Present"
                            if is_present
                            else "❌ Absent"
                        )
                    }
                )

                attendance_to_log.append(
                    {
                        "student_id": student_id,

                        "subject_id": selected_subject_id,

                        "timestamp": current_timestamp,

                        "is_present": bool(
                            is_present
                        )
                    }
                )

            # =================================================
            # 6. STORE RESULTS
            # =================================================

            st.session_state.voice_attendance_results = (
                pd.DataFrame(results),
                attendance_to_log
            )

    # =========================================================
    # 7. SHOW ATTENDANCE RESULTS
    # =========================================================

    attendance_results = st.session_state.get(
        "voice_attendance_results"
    )

    if attendance_results:

        st.divider()

        df_results, logs = attendance_results

        show_attendance_result(
            df_results,
            logs
        )