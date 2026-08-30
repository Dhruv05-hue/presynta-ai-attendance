import streamlit as st
import textwrap
import time

from src.database.db import enroll_student_to_subject
from src.database.config import supabase


@st.dialog("Quick Enrollment")
def auto_enroll_dialog(subject_code):

    student_id = st.session_state.student_data["student_id"]

    # =========================================================
    # FIND SUBJECT
    # =========================================================

    res = (
        supabase
        .table("subjects")
        .select("subject_id, name, subject_code")
        .eq("subject_code", subject_code)
        .execute()
    )

    if not res.data:

        st.html(
                """<div class="presynta-enroll-status">

                    <div class="presynta-status-icon presynta-error-icon">
                        !
                    </div>

                    <div class="presynta-status-title">
                        Subject not found
                    </div>

                    <div class="presynta-status-text">
                        We couldn't find a subject using this
                        enrollment code. Please check the code
                        and try again.
                    </div>

                </div>


                <style>

                    .presynta-enroll-status {
                        text-align: center;
                        padding: 0.5rem 0 1rem;
                    }


                    .presynta-status-icon {
                        width: 46px;
                        height: 46px;

                        display: flex;
                        align-items: center;
                        justify-content: center;

                        margin: 0 auto 0.8rem;

                        border-radius: 50%;

                        font-family: 'Space Grotesk', sans-serif;

                        font-size: 1.2rem;
                        font-weight: 800;
                    }


                    .presynta-error-icon {
                        background: #FFF1F1;
                        border: 1px solid #F2CACA;
                        color: #C0392B;
                    }


                    .presynta-status-title {
                        margin-bottom: 0.35rem;

                        color: #0B1220;

                        font-family: 'Space Grotesk', sans-serif;

                        font-size: 1.15rem;
                        font-weight: 700;
                    }


                    .presynta-status-text {
                        max-width: 400px;

                        margin: 0 auto;

                        color: #475569;

                        font-family: 'Manrope', sans-serif;

                        font-size: 0.75rem;
                        font-weight: 500;

                        line-height: 1.6;
                    }

                </style>
                """
            
        )

        if st.button(
            "Close",
            width="stretch",
            type="tertiary",
            icon=":material/close:",
        ):

            st.query_params.clear()
            st.rerun()

        return

    subject = res.data[0]

    # =========================================================
    # CHECK EXISTING ENROLLMENT
    # =========================================================

    check = (
        supabase
        .table("subject_students")
        .select("*")
        .eq(
            "subject_id",
            subject["subject_id"]
        )
        .eq(
            "student_id",
            student_id
        )
        .execute()
    )

    if check.data:

        st.html(
                f"""<div class="presynta-enroll-status">

                    <div class="presynta-status-icon presynta-success-icon">
                        ✓
                    </div>

                    <div class="presynta-status-title">
                        Already enrolled
                    </div>

                    <div class="presynta-status-text">
                        You are already enrolled in
                        <strong>{subject["name"]}</strong>.
                    </div>

                </div>


                <style>

                    .presynta-enroll-status {{
                        text-align: center;
                        padding: 0.5rem 0 1rem;
                    }}


                    .presynta-status-icon {{
                        width: 46px;
                        height: 46px;

                        display: flex;
                        align-items: center;
                        justify-content: center;

                        margin: 0 auto 0.8rem;

                        border-radius: 50%;

                        font-family: 'Space Grotesk', sans-serif;

                        font-size: 1.2rem;
                        font-weight: 800;
                    }}


                    .presynta-success-icon {{
                        background: #E8F5EF;
                        border: 1px solid #CDE8DB;
                        color: #19A974;
                    }}


                    .presynta-status-title {{
                        margin-bottom: 0.35rem;

                        color: #0B1220;

                        font-family: 'Space Grotesk', sans-serif;

                        font-size: 1.15rem;
                        font-weight: 700;
                    }}


                    .presynta-status-text {{
                        max-width: 400px;

                        margin: 0 auto;

                        color: #475569;

                        font-family: 'Manrope', sans-serif;

                        font-size: 0.75rem;
                        font-weight: 500;

                        line-height: 1.6;
                    }}


                    .presynta-status-text strong {{
                        color: #263247;

                        font-weight: 800;
                    }}

                </style>
                """
        )

        if st.button(
            "Got it",
            width="stretch",
            type="primary",
            icon=":material/check:",
        ):

            st.query_params.clear()
            st.rerun()

        return

    # =========================================================
    # ENROLLMENT CONFIRMATION
    # =========================================================

    st.html(
        f"""<div class="presynta-auto-enroll">

                <div class="presynta-auto-enroll-icon">
                    +
                </div>

                <div class="presynta-auto-enroll-content">

                    <div class="presynta-enroll-label">
                        SUBJECT INVITATION
                    </div>

                    <div class="presynta-enroll-title">
                        {subject["name"]}
                    </div>

                    <div class="presynta-enroll-description">
                        You have been invited to join this subject.
                        Would you like to enroll?
                    </div>

                </div>

            </div>


            <style>

                .presynta-auto-enroll {{
                    display: flex;
                    align-items: flex-start;

                    gap: 12px;

                    margin-bottom: 1.2rem;

                    padding: 14px;

                    background: #F7F9F8;

                    border: 1px solid #DCE4DF;

                    border-radius: 1rem;

                    box-sizing: border-box;
                }}


                .presynta-auto-enroll-icon {{
                    width: 42px;
                    height: 42px;

                    display: flex;
                    align-items: center;
                    justify-content: center;

                    flex-shrink: 0;

                    background: #E8F5EF;

                    border: 1px solid #CDE8DB;

                    border-radius: 0.8rem;

                    color: #19A974;

                    font-family: 'Space Grotesk', sans-serif;

                    font-size: 1.3rem;
                    font-weight: 700;
                }}


                .presynta-auto-enroll-content {{
                    min-width: 0;
                }}


                .presynta-enroll-label {{
                    color: #12845A;

                    font-family: 'Manrope', sans-serif;

                    font-size: 0.58rem;
                    font-weight: 800;

                    letter-spacing: 0.1em;

                    line-height: 1.2;
                }}


                .presynta-enroll-title {{
                    margin-top: 4px;

                    color: #0B1220;

                    font-family: 'Space Grotesk', sans-serif;

                    font-size: 1.15rem;
                    font-weight: 700;

                    line-height: 1.25;
                }}


                .presynta-enroll-description {{
                    margin-top: 5px;

                    color: #475569;

                    font-family: 'Manrope', sans-serif;

                    font-size: 0.73rem;
                    font-weight: 500;

                    line-height: 1.5;
                }}


                /* =====================================================
                   MOBILE
                   ===================================================== */

                @media (max-width: 480px) {{

                    .presynta-auto-enroll {{
                        gap: 9px;
                        padding: 11px;
                    }}


                    .presynta-auto-enroll-icon {{
                        width: 36px;
                        height: 36px;

                        font-size: 1rem;
                    }}


                    .presynta-enroll-title {{
                        font-size: 1rem;
                    }}


                    .presynta-enroll-description {{
                        font-size: 0.68rem;
                    }}

                }}

            </style>
            """
    )

    # =========================================================
    # ACTIONS
    # =========================================================

    col1, col2 = st.columns(
        2,
        gap="small"
    )

    with col1:

        if st.button(
            "No Thanks",
            width="stretch",
            type="tertiary",
            icon=":material/close:",
        ):

            st.query_params.clear()
            st.rerun()

    with col2:

        if st.button(
            "Yes, Enroll",
            type="primary",
            width="stretch",
            icon=":material/check_circle:",
        ):

            try:

                enroll_student_to_subject(
                    student_id,
                    subject["subject_id"]
                )

                st.success(
                    "Joined successfully!"
                )

                st.query_params.clear()

                time.sleep(1)

                st.rerun()

            except Exception as e:

                st.error(
                    f"Unable to join subject: {str(e)}"
                )