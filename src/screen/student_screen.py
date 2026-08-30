import streamlit as st

from src.ui.base_layout import style_background_dashboard, style_base_layout
from src.components.header import header_dashboard
from src.components.footer import footer_dashboard
import numpy as np
from PIL import Image
from src.pipelines.face_pipeline import (
    predict_attendance,
    get_face_embeddings,
    train_classifier
)
from src.pipelines.voice_pipeline import get_voice_embedding
from src.database.db import (
    get_all_students,
    create_student,
    get_student_subjects,
    get_student_attendance,
    unenroll_student_to_subject
)
from src.components.dialog_enroll import enroll_dialog
from src.components.subject_card import subject_card

import time


def student_dashboard():

    student_data = st.session_state.student_data
    student_id = student_data["student_id"]

    # =========================================================
    # DASHBOARD HEADER
    # =========================================================

    c1, c2 = st.columns(
        [2.2, 1],
        vertical_alignment="center",
        gap="large"
    )

    with c1:
        header_dashboard()

    with c2:

        st.markdown(
            f"""
            <div class="presynta-user-welcome">
                <span>WELCOME BACK</span>
                <strong>{student_data['name']}</strong>
            </div>
            """,
            unsafe_allow_html=True
        )

        if st.button(
            "Logout",
            type="secondary",
            key="loginbackbtn",
            shortcut="control+backspace",
            width="stretch"
        ):
            st.session_state["is_logged_in"] = False
            del st.session_state.student_data
            st.rerun()

       # =========================================================
    # DASHBOARD INTRO
    # =========================================================

    st.html(
        """<div class="presynta-dashboard-intro">

            <div class="presynta-dashboard-label">
                STUDENT DASHBOARD
            </div>

            <h2>Your learning space</h2>

            <p>
                Manage your enrolled subjects and keep track of
                your attendance from one place.
            </p>

        </div>


        <style>

            .presynta-dashboard-intro {
                margin: 1rem 0 1.5rem;
            }


            .presynta-dashboard-label {
                display: inline-block;

                color: #12845A;
                background: #E8F5EF;

                border: 1px solid #CDE8DB;

                border-radius: 999px;

                padding: 5px 10px;

                font-family: 'Manrope', sans-serif;

                font-size: 0.62rem;
                font-weight: 800;

                letter-spacing: 0.1em;
            }


            .presynta-dashboard-intro h2 {
                margin-top: 0.75rem;
                margin-bottom: 0.35rem;

                color: #0B1220;

                font-family: 'Space Grotesk', sans-serif;

                font-size: 2rem;
                font-weight: 700;

                letter-spacing: -0.04em;
            }


            .presynta-dashboard-intro p {
                margin: 0;

                color: #475569;

                font-family: 'Manrope', sans-serif;

                font-size: 0.9rem;

                line-height: 1.6;
            }


            /* =====================================================
               MOBILE
               ===================================================== */

            @media (max-width: 768px) {

                .presynta-dashboard-intro {
                    margin-top: 0.5rem;
                }


                .presynta-dashboard-intro h2 {
                    font-size: 1.65rem;
                }


                .presynta-dashboard-intro p {
                    font-size: 0.85rem;
                }

            }


            /* =====================================================
               VERY SMALL PHONES
               ===================================================== */

            @media (max-width: 480px) {

                .presynta-dashboard-intro h2 {
                    font-size: 1.45rem;
                }


                .presynta-dashboard-intro p {
                    font-size: 0.82rem;
                }

            }

        </style>
        """
    )

    # =========================================================
    # SUBJECT SECTION
    # =========================================================

    c1, c2 = st.columns(
        [1.5, 1],
        vertical_alignment="center"
    )

    with c1:

        st.header("Your Enrolled Subjects")

    with c2:

        if st.button(
            "Enroll in Subject",
            type="primary",
            width="stretch",
            icon=":material/add_circle:"
        ):
            enroll_dialog()

    st.divider()

    # =========================================================
    # LOAD SUBJECTS
    # =========================================================

    with st.spinner("Loading your enrolled subjects.."):

        subjects = get_student_subjects(student_id)
        logs = get_student_attendance(student_id)

        stats_map = {}

        for log in logs:

            sid = log["subject_id"]

            if sid not in stats_map:
                stats_map[sid] = {
                    "total": 0,
                    "attended": 0
                }

            stats_map[sid]["total"] += 1

            if log.get("is_present"):
                stats_map[sid]["attended"] += 1

        cols = st.columns(2)

        for i, sub_node in enumerate(subjects):

            sub = sub_node["subjects"]
            sid = sub["subject_id"]

            stats = stats_map.get(
                sid,
                {
                    "total": 0,
                    "attended": 0
                }
            )

            def unenroll_button():

                if st.button(
                    "Unenroll from this course",
                    type="tertiary",
                    width="stretch",
                    icon=":material/delete_forever:",
                    key=f"unenroll_{sid}"
                ):

                    unenroll_student_to_subject(
                        student_id,
                        sid
                    )

                    st.toast(
                        f"Unenrolled from {sub['name']} successfully"
                    )

                    st.rerun()

            with cols[i % 2]:

                subject_card(
                    name=sub["name"],
                    code=sub["subject_code"],
                    section=sub["section"],
                    stats=[
                        (
                            "📅",
                            "Total",
                            stats["total"]
                        ),
                        (
                            "✅",
                            "Attended",
                            stats["attended"]
                        )
                    ],
                    footer_callback=unenroll_button
                )

    footer_dashboard()


def student_screen():

    style_background_dashboard()
    style_base_layout()

    # =========================================================
    # LOGGED-IN STUDENT
    # =========================================================

    if "student_data" in st.session_state:

        student_dashboard()

        return

    # =========================================================
    # LOGIN HEADER
    # =========================================================

    c1, c2 = st.columns(
        [2.2, 1],
        vertical_alignment="center",
        gap="large"
    )

    with c1:

        header_dashboard()

    with c2:

        if st.button(
            "Go back to Home",
            type="secondary",
            key="loginbackbtn",
            shortcut="control+backspace",
            width="stretch"
        ):

            st.session_state["login_type"] = None
            st.rerun()

    # =========================================================
    # LOGIN INTRO
    # =========================================================

    st.html(
    """
    <div class="presynta-face-login">

        <div class="presynta-login-badge">
            <span class="presynta-login-dot"></span>
            SECURE STUDENT ACCESS
        </div>

        <h2>Welcome to Presynta</h2>

        <p class="presynta-login-description">
            Position your face inside the camera frame.
            Presynta will securely recognize your profile
            and sign you in automatically.
        </p>

        <div class="presynta-login-features">

            <div class="presynta-login-feature">

                <div class="presynta-feature-icon">◉</div>

                <div>
                    <strong>Face Recognition</strong>
                    <span>Fast profile identification</span>
                </div>

            </div>


            <div class="presynta-login-feature">

                <div class="presynta-feature-icon">✓</div>

                <div>
                    <strong>Secure Access</strong>
                    <span>Designed for registered students</span>
                </div>

            </div>

        </div>

    </div>


    <style>

        .presynta-face-login {
            max-width: 700px;
            margin: 1rem auto 1.5rem;
            text-align: center;
        }


        .presynta-login-badge {
            display: inline-flex;
            align-items: center;
            gap: 7px;

            padding: 6px 11px;

            background: #E8F5EF;
            border: 1px solid #CDE8DB;

            border-radius: 999px;

            color: #12845A;

            font-family: 'Manrope', sans-serif;
            font-size: 0.62rem;
            font-weight: 800;

            letter-spacing: 0.1em;
        }


        .presynta-login-dot {
            width: 6px;
            height: 6px;

            border-radius: 50%;

            background: #19A974;
        }


        .presynta-face-login h2 {
            margin-top: 0.9rem !important;
            margin-bottom: 0.5rem !important;

            color: #0B1220 !important;

            font-family: 'Space Grotesk', sans-serif !important;

            font-size: 2.25rem !important;
            font-weight: 700 !important;
        }


        .presynta-login-description {
            max-width: 570px;

            margin: 0 auto;

            color: #475569;

            font-family: 'Manrope', sans-serif;

            font-size: 0.9rem;

            line-height: 1.7;
        }


        .presynta-login-features {
            display: grid;

            grid-template-columns: repeat(2, 1fr);

            gap: 10px;

            margin-top: 1.4rem;
        }


        .presynta-login-feature {
            display: flex;
            align-items: center;

            gap: 10px;

            text-align: left;

            background: #FFFFFF;

            border: 1px solid #DCE4DF;

            border-radius: 0.9rem;

            padding: 11px 13px;
        }


        .presynta-feature-icon {
            width: 32px;
            height: 32px;

            display: flex;
            align-items: center;
            justify-content: center;

            flex-shrink: 0;

            background: #E8F5EF;

            color: #19A974;

            border-radius: 0.6rem;

            font-family: 'Space Grotesk', sans-serif;

            font-weight: 700;
        }


        .presynta-login-feature div:last-child {
            display: flex;
            flex-direction: column;
        }


        .presynta-login-feature strong {
            color: #172033;

            font-family: 'Manrope', sans-serif;

            font-size: 0.75rem;
            font-weight: 800;
        }


        .presynta-login-feature span {
            margin-top: 2px;

            color: #7A8494;

            font-family: 'Manrope', sans-serif;

            font-size: 0.68rem;
        }


        @media (max-width: 768px) {

            .presynta-face-login {
                margin-top: 0.5rem;
            }


            .presynta-face-login h2 {
                font-size: 1.75rem !important;
            }


            .presynta-login-description {
                font-size: 0.85rem;
            }


            .presynta-login-features {
                grid-template-columns: 1fr;
            }

        }


        @media (max-width: 480px) {

            .presynta-face-login h2 {
                font-size: 1.5rem !important;
            }


            .presynta-login-description {
                font-size: 0.8rem;
            }


            .presynta-login-feature {
                padding: 9px 10px;
            }

        }

    </style>
    """
)
    # =========================================================
    # FACE LOGIN
    # =========================================================

    photo_source = st.camera_input(
        "Position your face in the center"
    )

    show_registration = False

    if photo_source:

        img = np.array(
            Image.open(photo_source)
        )

        with st.spinner("AI is scanning..."):

            detected, all_ids, num_faces = predict_attendance(img)

            if num_faces == 0:

                st.warning("Face not found!")

            elif num_faces > 1:

                st.warning("Multiple faces found")

            else:

                if detected:

                    student_id = list(
                        detected.keys()
                    )[0]

                    all_students = get_all_students()

                    student = next(
                        (
                            s for s in all_students
                            if s["student_id"] == student_id
                        ),
                        None
                    )

                    if student:

                        st.session_state.is_logged_in = True
                        st.session_state.user_role = "student"
                        st.session_state.student_data = student

                        st.toast(
                            "Welcome Back " + student["name"]
                        )

                        time.sleep(1)

                        st.rerun()

                else:

                    st.info(
                        "Face not recognized! "
                        "You might be a new student"
                    )

                    show_registration = True

    # =========================================================
    # NEW STUDENT REGISTRATION
    # =========================================================

    if show_registration:

        with st.container(border=True):

            st.header("Register New Profile")

            st.markdown(
                """
                <p style="
                    color:#697586;
                    font-family:'Manrope',sans-serif;
                    font-size:0.85rem;
                    line-height:1.6;
                ">
                    Your face wasn't found in the system.
                    Create a student profile using the captured image.
                </p>
                """,
                unsafe_allow_html=True
            )

            new_name = st.text_input(
                "Enter your name",
                placeholder="E.g. Rohan"
            )

            st.subheader("Optional: Voice Enrollment")

            st.info(
                "Enroll your voice only for attendance."
            )

            audio_data = None

            try:

                audio_data = st.audio_input(
                    "Record a short phrase like "
                    "I am present, My name is Akash."
                )

            except Exception:

                st.error("Audio Data failed!")

            if st.button(
                "Create Account",
                type="primary",
                width="stretch",
                icon=":material/person_add:"
            ):

                if new_name:

                    with st.spinner("Creating profile.."):

                        img = np.array(
                            Image.open(photo_source)
                        )

                        encoding = get_face_embeddings(img)

                        if encoding:

                            face_emb = encoding[0].tolist()
                            voice_emb = None

                            if audio_data:

                                voice_emb = get_voice_embedding(
                                    audio_data.read()
                                )

                            response_data = create_student(
                                new_name,
                                face_embedding=face_emb,
                                voice_embedding=voice_emb
                            )

                            if response_data:

                                train_classifier()

                                st.session_state.is_logged_in = True
                                st.session_state.user_role = "student"
                                st.session_state.student_data = response_data[0]

                                st.toast(
                                    f"Profile Created! Hi {new_name}"
                                )

                                time.sleep(1)

                                st.rerun()

                        else:

                            st.error(
                                "Could not capture your facial "
                                "feature for registration"
                            )

    footer_dashboard()