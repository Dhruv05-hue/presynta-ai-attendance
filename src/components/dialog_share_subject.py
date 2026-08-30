import streamlit as st

import segno
import io


@st.dialog("Share Subject")
def share_subject_dialog(subject_name, subject_code):

    app_domain = "https://snapclass-intelligent-attendance.streamlit.app"
    join_url = f"{app_domain}/?join-code={subject_code}"

    st.html(
        f"""<div class="presynta-share-header">

            <div class="presynta-share-icon">
                ↗
            </div>

            <div>
                <h3>Share this subject</h3>
                <p>
                    Invite students to <strong>{subject_name}</strong>
                    using the code or QR code below.
                </p>
            </div>

        </div>

        <style>

            .presynta-share-header {{
                display: flex;
                align-items: center;
                gap: 12px;
                margin-bottom: 1.2rem;
            }}


            .presynta-share-icon {{
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
                font-size: 1.35rem;
                font-weight: 700;
            }}


            .presynta-share-header h3 {{
                margin: 0;

                color: #0B1220;

                font-family: 'Space Grotesk', sans-serif;

                font-size: 1.2rem;
                font-weight: 700;
            }}


            .presynta-share-header p {{
                margin: 3px 0 0;

                color: #7A8494;

                font-family: 'Manrope', sans-serif;

                font-size: 0.75rem;

                line-height: 1.5;
            }}


            .presynta-share-header strong {{
                color: #263247;

                font-weight: 800;
            }}


            .presynta-share-section {{
                margin-bottom: 0.8rem;
            }}


            .presynta-share-section-title {{
                margin-bottom: 0.45rem;

                color: #172033;

                font-family: 'Space Grotesk', sans-serif;

                font-size: 0.85rem;
                font-weight: 700;
            }}


            .presynta-share-code {{
                padding: 0.8rem;

                background: #F7F9F8;

                border: 1px solid #DCE4DF;

                border-radius: 0.8rem;

                text-align: center;
            }}


            .presynta-share-code span {{
                display: block;

                color: #7A8494;

                font-family: 'Manrope', sans-serif;

                font-size: 0.6rem;
                font-weight: 800;

                letter-spacing: 0.1em;
            }}


            .presynta-share-code strong {{
                display: block;

                margin-top: 3px;

                color: #19A974;

                font-family: 'Space Grotesk', sans-serif;

                font-size: 1.4rem;

                letter-spacing: 0.08em;
            }}


            .presynta-qr-wrapper {{
                display: flex;
                justify-content: center;
                align-items: center;

                padding: 0.8rem;

                background: #FFFFFF;

                border: 1px solid #DCE4DF;

                border-radius: 1rem;
            }}


            .presynta-share-note {{
                margin-top: 0.8rem;

                padding: 9px 11px;

                background: #F7F9F8;

                border: 1px solid #E2E9E4;

                border-radius: 0.7rem;

                color: #697586;

                font-family: 'Manrope', sans-serif;

                font-size: 0.68rem;

                line-height: 1.5;
            }}


            @media (max-width: 768px) {{

                div[data-testid="stHorizontalBlock"] {{
                    gap: 0.6rem !important;
                }}

            }}


            @media (max-width: 480px) {{

                .presynta-share-header {{
                    gap: 9px;
                }}


                .presynta-share-icon {{
                    width: 36px;
                    height: 36px;

                    font-size: 1.1rem;
                }}


                .presynta-share-header h3 {{
                    font-size: 1.05rem;
                }}


                .presynta-share-header p {{
                    font-size: 0.68rem;
                }}


                div[data-testid="stHorizontalBlock"] {{
                    gap: 0.35rem !important;
                }}

            }}

        </style>
        """
    )

    qr = segno.make(join_url)

    out = io.BytesIO()

    qr.save(
        out,
        kind="png",
        scale=10,
        border=3
    )

    col1, col2 = st.columns(
        2,
        gap="medium"
    )

    with col1:

        st.markdown(
            """
            <div class="presynta-share-section">
                <div class="presynta-share-section-title">
                    Enrollment Link
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.code(
            join_url,
            language="text"
        )

        st.html(
            f"""<div class="presynta-share-section">
                <div class="presynta-share-section-title">
                    Subject Code
                </div>

                <div class="presynta-share-code">
                    <span>JOIN CODE</span>
                    <strong>{subject_code}</strong>
                </div>
            </div>
            """
        )

        st.markdown(
            """
            <div class="presynta-share-note">
                Share the enrollment link through WhatsApp,
                email, or any other messaging platform.
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:

        st.markdown(
            """
            <div class="presynta-share-section-title">
                Scan to Join
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            '<div class="presynta-qr-wrapper">',
            unsafe_allow_html=True
        )

        st.image(
            out.getvalue(),
            width="stretch"
        )

        st.markdown(
            "</div>",
            unsafe_allow_html=True
        )