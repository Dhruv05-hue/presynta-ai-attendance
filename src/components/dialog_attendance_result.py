import streamlit as st

from src.database.db import create_attendance


def show_attendance_result(df, logs):

    st.html(
        """<div class="presynta-result-header">

            <div class="presynta-result-icon">
                ✓
            </div>

            <div>
                <h3>Review attendance</h3>
                <p>
                    Verify the recognition results before saving
                    this attendance session.
                </p>
            </div>

        </div>

        <div class="presynta-result-tip">
            <span>REVIEW</span>
            Check that every student's status is correct before confirming.
        </div>

        <style>

            .presynta-result-header {
                display: flex;
                align-items: center;
                gap: 12px;
                margin-bottom: 1rem;
            }


            .presynta-result-icon {
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
                font-size: 1.2rem;
                font-weight: 700;
            }


            .presynta-result-header h3 {
                margin: 0;

                color: #0B1220;

                font-family: 'Space Grotesk', sans-serif;

                font-size: 1.2rem;
                font-weight: 700;
            }


            .presynta-result-header p {
                margin: 3px 0 0;

                color: #7A8494;

                font-family: 'Manrope', sans-serif;

                font-size: 0.74rem;

                line-height: 1.5;
            }


            .presynta-result-tip {
                display: flex;
                align-items: flex-start;
                gap: 8px;

                margin-bottom: 1rem;

                padding: 9px 11px;

                background: #F7F9F8;

                border: 1px solid #E2E9E4;

                border-radius: 0.7rem;

                color: #697586;

                font-family: 'Manrope', sans-serif;

                font-size: 0.7rem;

                line-height: 1.5;
            }


            .presynta-result-tip span {
                flex-shrink: 0;

                color: #19A974;

                font-size: 0.58rem;

                font-weight: 800;

                letter-spacing: 0.08em;
            }


            /* Attendance table */

            div[data-testid="stDataFrame"] {
                border: 1px solid #DCE4DF !important;

                border-radius: 0.9rem !important;

                overflow: hidden !important;

                margin-bottom: 1rem;
            }


            /* Mobile */

            @media (max-width: 480px) {

                .presynta-result-header {
                    gap: 9px;
                }


                .presynta-result-icon {
                    width: 36px;
                    height: 36px;

                    font-size: 1rem;
                }


                .presynta-result-header h3 {
                    font-size: 1.05rem;
                }


                .presynta-result-header p {
                    font-size: 0.68rem;
                }


                .presynta-result-tip {
                    font-size: 0.65rem;
                }

            }

        </style>
        """
    )

    table_height = min(
        400,
        35 * (len(df) + 1)
    )

    st.dataframe(
        df,
        hide_index=True,
        width="stretch",
        height=table_height
    )

    col1, col2 = st.columns(
        2,
        gap="small"
    )

    with col1:

        if st.button(
            "Discard",
            width="stretch",
            type="tertiary",
            icon=":material/delete:"
        ):

            st.session_state.voice_attendance_results = None
            st.session_state.attendance_images = []

            st.rerun()

    with col2:

        if st.button(
            "Confirm & Save",
            width="stretch",
            type="primary",
            icon=":material/check_circle:"
        ):

            try:

                create_attendance(logs)

                st.toast(
                    "Attendance saved successfully",
                    icon="✅"
                )

                st.session_state.attendance_images = []
                st.session_state.voice_attendance_results = None

                st.rerun()

            except Exception as e:

                st.error(
                    f"Sync failed: {str(e)}"
                )


@st.dialog("Attendance Report")
def attendance_result_dialog(df, logs):

    show_attendance_result(
        df,
        logs
    )