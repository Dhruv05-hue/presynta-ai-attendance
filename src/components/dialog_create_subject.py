import streamlit as st

from src.database.db import create_subject


@st.dialog("Create New Subject")
def create_subject_dialog(teacher_id):

    st.html(
        """<div class="presynta-create-header">

            <div class="presynta-create-icon">
                +
            </div>

            <div>
                <h3>Create a subject</h3>
                <p>
                    Set up a new class and start managing
                    your student attendance.
                </p>
            </div>

        </div>

        <div class="presynta-create-note">
            <span>INFO</span>
            Share the subject code with students so they can enroll.
        </div>

        <style>

            .presynta-create-header {
                display: flex;
                align-items: center;
                gap: 12px;
                margin-bottom: 1.2rem;
            }


            .presynta-create-icon {
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


            .presynta-create-header h3 {
                margin: 0;

                color: #0B1220;

                font-family: 'Space Grotesk', sans-serif;

                font-size: 1.2rem;
                font-weight: 700;
            }


            .presynta-create-header p {
                margin: 3px 0 0;

                color: #7A8494;

                font-family: 'Manrope', sans-serif;

                font-size: 0.75rem;

                line-height: 1.5;
            }


            .presynta-create-note {
                display: flex;
                align-items: center;
                gap: 7px;

                margin-bottom: 1rem;

                padding: 9px 11px;

                background: #F7F9F8;

                border: 1px solid #E2E9E4;

                border-radius: 0.7rem;

                color: #697586;

                font-family: 'Manrope', sans-serif;

                font-size: 0.7rem;

                line-height: 1.4;
            }


            .presynta-create-note span {
                color: #19A974;

                font-size: 0.58rem;

                font-weight: 800;

                letter-spacing: 0.08em;
            }


            @media (max-width: 480px) {

                .presynta-create-header {
                    gap: 9px;
                }


                .presynta-create-icon {
                    width: 36px;
                    height: 36px;

                    font-size: 1.1rem;
                }


                .presynta-create-header h3 {
                    font-size: 1.05rem;
                }


                .presynta-create-header p {
                    font-size: 0.7rem;
                }


                .presynta-create-note {
                    font-size: 0.65rem;
                }

            }

        </style>
        """
    )

    sub_id = st.text_input(
        "Subject Code",
        placeholder="e.g. CS101"
    )

    sub_name = st.text_input(
        "Subject Name",
        placeholder="Introduction to Computer Science"
    )

    sub_section = st.text_input(
        "Section",
        placeholder="e.g. A"
    )

    if st.button(
        "Create Subject",
        type="primary",
        width="stretch",
        icon=":material/add_circle:"
    ):

        if sub_id and sub_name and sub_section:

            try:

                create_subject(
                    sub_id,
                    sub_name,
                    sub_section,
                    teacher_id
                )

                st.toast(
                    "Subject Created Successfully!",
                    icon="✅"
                )

                st.rerun()

            except Exception as e:

                st.error(
                    f"Unable to create subject: {str(e)}"
                )

        else:

            st.warning(
                "Please fill in all the fields."
            )