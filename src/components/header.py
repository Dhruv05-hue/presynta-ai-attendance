import streamlit as st
import base64
from pathlib import Path

def get_logo_base64():

    logo_path = (
        Path(__file__).resolve().parents[2]
        / "assets"
        / "presynta_logo_icon.png"
    )

    with open(logo_path, "rb") as image_file:
        return base64.b64encode(
            image_file.read()
        ).decode()

def header_home():

    logo_base64 = get_logo_base64()

    st.html(
        f"""
        <div class="presynta-home-header">

            <div class="presynta-logo-wrapper">
                <img
                    src="data:image/png;base64,{logo_base64}"
                    class="presynta-home-logo"
                />
            </div>

            <div class="presynta-brand">

                <div class="presynta-home-title">
                    PRESYNTA
                </div>

                <div class="presynta-home-subtitle">
                    INTELLIGENT PRESENCE MANAGEMENT
                </div>

            </div>

        </div>


        <style>

        .presynta-home-header {{
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            text-align: center;

            margin-top: 10px;
            margin-bottom: 20px;
        }}


        .presynta-logo-wrapper {{
            width: 105px;
            height: 105px;

            display: flex;
            align-items: center;
            justify-content: center;

            background: #E8F5EF;
            border: 1px solid #CDE8DB;
            border-radius: 2rem;

            padding: 10px;

            box-sizing: border-box;

            margin-bottom: 8px;
        }}


        .presynta-home-logo {{
            width: 100%;
            height: 100%;

            object-fit: contain;

            display: block;
        }}


        .presynta-brand {{
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;

            margin: 0;
            padding: 0;
        }}


        .presynta-home-title {{
            display: block;

            margin: 0;
            padding: 0;

            color: #FFFFFF;

            font-family: 'Manrope', sans-serif;

            font-size: 3.2rem;
            font-weight: 800;

            letter-spacing: 0.04em;
            line-height: 1;
        }}


        .presynta-home-subtitle {{
            display: block;

            margin: 7px 0 0;
            padding: 0;

            color: #19A974;

            font-family: 'Manrope', sans-serif;

            font-size: 0.75rem;
            font-weight: 800;

            letter-spacing: 0.16em;
            line-height: 1.2;
        }}


        @media (max-width: 768px) {{

            .presynta-home-header {{
                margin-top: 8px;
                margin-bottom: 16px;
            }}


            .presynta-logo-wrapper {{
                width: 80px;
                height: 80px;

                border-radius: 1.4rem;

                margin-bottom: 7px;
            }}


            .presynta-home-title {{
                font-size: 2.35rem;
            }}


            .presynta-home-subtitle {{
                font-size: 0.62rem;
                letter-spacing: 0.1em;

                margin-top: 6px;
            }}

        }}


        @media (max-width: 480px) {{

            .presynta-home-header {{
                margin-top: 6px;
                margin-bottom: 14px;
            }}


            .presynta-logo-wrapper {{
                width: 70px;
                height: 70px;

                border-radius: 1.2rem;

                margin-bottom: 6px;
            }}


            .presynta-home-title {{
                font-size: 2rem;
            }}


            .presynta-home-subtitle {{
                font-size: 0.55rem;
                letter-spacing: 0.08em;

                margin-top: 5px;
            }}

        }}

        </style>
        """
    )


def header_dashboard():

    logo_base64 = get_logo_base64()

    st.html(
        f"""
        <div class="presynta-dashboard-header">

            <div class="presynta-dashboard-logo-wrapper">

                <img
                    src="data:image/png;base64,{logo_base64}"
                    class="presynta-dashboard-logo"
                />

            </div>

            <div class="presynta-dashboard-brand">

                <div class="presynta-dashboard-title">
                    PRESYNTA
                </div>

                <div class="presynta-dashboard-subtitle">
                    SMART ATTENDANCE
                </div>

            </div>

        </div>


        <style>

        .presynta-dashboard-header {{
            display: flex;
            align-items: center;
            justify-content: center;

            gap: 12px;

            margin-bottom: 24px;
        }}


        .presynta-dashboard-logo-wrapper {{
            width: 72px;
            height: 72px;

            display: flex;
            align-items: center;
            justify-content: center;

            background: #E8F5EF;
            border: 1px solid #CDE8DB;

            border-radius: 1.25rem;

            padding: 8px;

            box-sizing: border-box;
        }}


        .presynta-dashboard-logo {{
            width: 100%;
            height: 100%;

            object-fit: contain;

            display: block;
        }}


        .presynta-dashboard-brand {{
            display: flex;
            flex-direction: column;
            align-items: flex-start;
            justify-content: center;

            margin: 0;
            padding: 0;
        }}


        .presynta-dashboard-title {{
            display: block;

            margin: 0;
            padding: 0;

            color: #0B1220;

            font-family: 'Space Grotesk', sans-serif;

            font-size: 1.9rem;
            font-weight: 700;

            letter-spacing: 0.02em;
            line-height: 1;
        }}


        .presynta-dashboard-subtitle {{
            display: block;

            margin: 6px 0 0;
            padding: 0;

            color: #19A974;

            font-family: 'Manrope', sans-serif;

            font-size: 0.62rem;
            font-weight: 800;

            letter-spacing: 0.12em;
            line-height: 1.2;
        }}


        @media (max-width: 768px) {{

            .presynta-dashboard-header {{
                gap: 10px;
                margin-bottom: 20px;
            }}


            .presynta-dashboard-logo-wrapper {{
                width: 58px;
                height: 58px;

                border-radius: 1rem;
            }}


            .presynta-dashboard-title {{
                font-size: 1.45rem;
            }}


            .presynta-dashboard-subtitle {{
                font-size: 0.5rem;
            }}

        }}


        @media (max-width: 480px) {{

            .presynta-dashboard-header {{
                gap: 8px;
                margin-bottom: 18px;
            }}


            .presynta-dashboard-logo-wrapper {{
                width: 50px;
                height: 50px;

                border-radius: 0.85rem;
            }}


            .presynta-dashboard-title {{
                font-size: 1.25rem;
            }}


            .presynta-dashboard-subtitle {{
                font-size: 0.46rem;
            }}

        }}

        </style>
        """
    )