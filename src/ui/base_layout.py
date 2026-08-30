import streamlit as st


def style_background_home():

    st.markdown("""
        <style>

            .stApp {
                background: #0B1220 !important;
            }

            .stApp div[data-testid="stColumn"] {
                background: #F4F7F5 !important;
                padding: 2.5rem !important;
                border-radius: 2rem !important;
                border: 1px solid rgba(255, 255, 255, 0.08) !important;
            }


            /* Mobile */

            @media (max-width: 768px) {

                .stApp div[data-testid="stColumn"] {
                    padding: 1.5rem !important;
                    border-radius: 1.5rem !important;
                }

            }

        </style>
    """, unsafe_allow_html=True)


def style_background_dashboard():

    st.markdown("""
        <style>

            .stApp {
                background: #F4F7F5 !important;
            }

        </style>
    """, unsafe_allow_html=True)


def style_base_layout():

    st.markdown("""
        <style>

        @import url('https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700;800&family=Space+Grotesk:wght@500;600;700&display=swap');


        /* =========================================================
           GLOBAL LAYOUT
           ========================================================= */

        #MainMenu,
        footer,
        header {
            visibility: hidden;
        }


        .block-container {
            padding-top: 1.5rem !important;
            padding-bottom: 2rem !important;
            max-width: 1400px !important;
        }


        /* =========================================================
           TYPOGRAPHY
           ========================================================= */

        h1,
        h2 {
            font-family: 'Space Grotesk', sans-serif !important;
            font-weight: 700 !important;
            letter-spacing: -0.04em !important;
            color: #0B1220 !important;
        }


        h1 {
            font-size: 3.4rem !important;
            line-height: 1.08 !important;
            margin-bottom: 0.4rem !important;
        }


        h2 {
            font-size: 2rem !important;
            line-height: 1.15 !important;
            margin-bottom: 0.4rem !important;
        }


        h3,
        h4,
        p,
        label,
        span {
            font-family: 'Manrope', sans-serif;
        }


        h3 {
            color: #172033 !important;
            font-weight: 700 !important;
        }


        h4 {
            color: #263247 !important;
            font-weight: 700 !important;
        }


        p {
            color: #475569;
        }


        /* =========================================================
           BUTTONS
           ========================================================= */

        button {
            border-radius: 0.85rem !important;
            background: #19A974 !important;
            color: #FFFFFF !important;
            padding: 0.65rem 1.25rem !important;
            border: 1px solid #19A974 !important;
            font-family: 'Manrope', sans-serif !important;
            font-weight: 700 !important;

            transition:
                transform 0.2s ease,
                background 0.2s ease,
                box-shadow 0.2s ease !important;
        }


        /* Force Streamlit button content to remain white */

        .stButton button,
        .stButton button p,
        .stButton button span,
        .stButton button div {
            color: #FFFFFF !important;
        }


        button:hover {
            background: #12845A !important;
            border-color: #12845A !important;
            transform: translateY(-2px);

            box-shadow:
                0 8px 20px rgba(25, 169, 116, 0.18) !important;
        }


        /* Secondary buttons */

        button[kind="secondary"] {
            border-radius: 0.85rem !important;
            background: #172033 !important;
            color: #FFFFFF !important;
            padding: 0.65rem 1.25rem !important;
            border: 1px solid #172033 !important;
            font-family: 'Manrope', sans-serif !important;
            font-weight: 700 !important;
        }


        button[kind="secondary"] p,
        button[kind="secondary"] span,
        button[kind="secondary"] div {
            color: #FFFFFF !important;
        }


        button[kind="secondary"]:hover {
            background: #263247 !important;
            border-color: #263247 !important;
            transform: translateY(-2px);
        }


        /* Tertiary buttons */

        button[kind="tertiary"] {
            border-radius: 0.85rem !important;
            background: transparent !important;
            color: #172033 !important;
            padding: 0.65rem 1.25rem !important;
            border: 1px solid #D5DDD8 !important;
            font-family: 'Manrope', sans-serif !important;
            font-weight: 700 !important;
        }


        button[kind="tertiary"] p,
        button[kind="tertiary"] span,
        button[kind="tertiary"] div {
            color: #172033 !important;
        }


        button[kind="tertiary"]:hover {
            background: #E8F5EF !important;
            color: #12845A !important;
            border-color: #19A974 !important;
            transform: translateY(-2px);
            box-shadow: none !important;
        }


        button[kind="tertiary"]:hover p,
        button[kind="tertiary"]:hover span,
        button[kind="tertiary"]:hover div {
            color: #12845A !important;
        }


        /* =========================================================
           INPUTS
           ========================================================= */

        input,
        textarea {
            border-radius: 0.8rem !important;
            border: 1px solid #D5DDD8 !important;
            background: #FFFFFF !important;
            color: #172033 !important;
            font-family: 'Manrope', sans-serif !important;
        }


        input:focus,
        textarea:focus {
            border-color: #19A974 !important;
            box-shadow: 0 0 0 2px rgba(25, 169, 116, 0.12) !important;
        }


        /* =========================================================
           SELECTBOX
           ========================================================= */

        div[data-baseweb="select"] > div {
            border-radius: 0.8rem !important;
            border-color: #D5DDD8 !important;
            background: #FFFFFF !important;
        }


        /* =========================================================
           CHECKBOXES / RADIO
           ========================================================= */

        div[data-testid="stCheckbox"] label,
        div[data-testid="stRadio"] label {
            font-family: 'Manrope', sans-serif !important;
            color: #263247 !important;
        }


        /* =========================================================
           DATAFRAMES / TABLES
           ========================================================= */

        div[data-testid="stDataFrame"] {
            border-radius: 1rem !important;
            overflow: hidden !important;
            border: 1px solid #DCE4DF !important;
        }


        /* =========================================================
           ALERTS
           ========================================================= */

        div[data-testid="stAlert"] {
            border-radius: 0.9rem !important;
            font-family: 'Manrope', sans-serif !important;
        }


        /* =========================================================
           DIVIDERS
           ========================================================= */

        hr {
            border-color: #DCE4DF !important;
            margin: 1.2rem 0 !important;
        }


        /* =========================================================
           MOBILE RESPONSIVE
           ========================================================= */

        @media (max-width: 768px) {

            .block-container {
                padding-top: 1rem !important;
                padding-left: 1rem !important;
                padding-right: 1rem !important;
                padding-bottom: 1.5rem !important;
            }


            h1 {
                font-size: 2.35rem !important;
                line-height: 1.08 !important;
            }


            h2 {
                font-size: 1.7rem !important;
                line-height: 1.15 !important;
            }


            h3 {
                font-size: 1.3rem !important;
            }


            h4 {
                font-size: 1.1rem !important;
            }


            p {
                font-size: 0.95rem !important;
            }


            button {
                padding: 0.6rem 1rem !important;
            }


            button:hover {
                transform: none;
                box-shadow: none !important;
            }

        }


        /* =========================================================
           VERY SMALL PHONES
           ========================================================= */

        @media (max-width: 480px) {

            .block-container {
                padding-left: 0.7rem !important;
                padding-right: 0.7rem !important;
            }


            h1 {
                font-size: 2rem !important;
            }


            h2 {
                font-size: 1.45rem !important;
            }

        }

        </style>
    """, unsafe_allow_html=True)