import streamlit as st

from src.database.db import enroll_student_to_subject
from src.database.config import supabase
import time


@st.dialog("Enroll in Subject")
def enroll_dialog():

    st.html(
        """<div class="presynta-enroll-header">

            <div class="presynta-enroll-icon">
                +
            </div>

            <div>
                <h3>Join a subject</h3>
                <p>
                    Enter the enrollment code provided by your teacher
                    to join the class.
                </p>
            </div>

        </div>

        <style>

            .presynta-enroll-header {
                display: flex;
                align-items: center;
                gap: 12px;
                margin-bottom: 1.2rem;
            }


            .presynta-enroll-icon {
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
                font-size: 1.4rem;
                font-weight: 700;
            }


            .presynta-enroll-header h3 {
                margin: 0;

                color: #0B1220;

                font-family: 'Space Grotesk', sans-serif;

                font-size: 1.2rem;
                font-weight: 700;
            }


            .presynta-enroll-header p {
                margin: 3px 0 0;

                color: #7A8494;

                font-family: 'Manrope', sans-serif;

                font-size: 0.75rem;

                line-height: 1.5;
            }


            .presynta-code-hint {
                display: flex;
                align-items: center;
                gap: 7px;

                margin-top: 0.8rem;

                padding: 9px 11px;

                background: #F7F9F8;

                border: 1px solid #E2E9E4;

                border-radius: 0.7rem;

                color: #697586;

                font-family: 'Manrope', sans-serif;

                font-size: 0.7rem;
            }


            .presynta-code-hint strong {
                color: #19A974;
            }


            @media (max-width: 480px) {

                .presynta-enroll-header {
                    gap: 9px;
                }


                .presynta-enroll-icon {
                    width: 36px;
                    height: 36px;

                    font-size: 1.1rem;
                }


                .presynta-enroll-header h3 {
                    font-size: 1.05rem;
                }


                .presynta-enroll-header p {
                    font-size: 0.7rem;
                }

            }

        </style>
        """,
  
    )

    join_code = st.text_input(
        "Subject Code",
        placeholder="e.g. CS101"
    )

    st.markdown(
        """
        <div class="presynta-code-hint">
            <strong>TIP</strong>
            Use the exact code shared by your teacher.
        </div>
        """,
        unsafe_allow_html=True
    )

    if st.button(
        "Enroll Now",
        type="primary",
        width="stretch",
        icon=":material/add_circle:"
    ):

        if join_code:

            res = (
                supabase
                .table("subjects")
                .select(
                    "subject_id, name, subject_code"
                )
                .eq(
                    "subject_code",
                    join_code
                )
                .execute()
            )

            if res.data:

                subject = res.data[0]

                student_id = (
                    st.session_state.student_data["student_id"]
                )

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

                    st.warning(
                        "You are already enrolled in this subject."
                    )

                else:

                    enroll_student_to_subject(
                        student_id,
                        subject["subject_id"]
                    )

                    st.success(
                        "Successfully enrolled!"
                    )

                    time.sleep(1)

                    st.rerun()

            else:

                st.error(
                    "Subject code not found. Please check the code and try again."
                )

        else:

            st.warning(
                "Please enter a subject code."
            )