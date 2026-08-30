import streamlit as st

from src.components.header import header_home
from src.ui.base_layout import style_base_layout, style_background_home
from src.components.footer import footer_home


def home_screen():

    style_base_layout()
    style_background_home()
    header_home()

    # =========================================================
    # HOME INTRO
    # =========================================================

    st.markdown(
        """
<div class="presynta-home-intro">

<div class="presynta-home-badge">
<span class="presynta-badge-dot"></span>
AI-POWERED ATTENDANCE
</div>

<h2>Choose your portal</h2>

<p>
Smart attendance powered by face and voice recognition.
Select your role to continue.
</p>

</div>

<style>

.presynta-home-intro {
text-align: center;
margin: 0 auto 2rem;
max-width: 650px;
}


.presynta-home-badge {
display: inline-flex;
align-items: center;
gap: 7px;

padding: 6px 11px;

background: #E8F5EF;
border: 1px solid #CDE8DB;
border-radius: 999px;

color: #12845A;

font-family: 'Manrope', sans-serif;
font-size: 0.65rem;
font-weight: 800;

letter-spacing: 0.1em;
}


.presynta-badge-dot {
width: 6px;
height: 6px;

background: #19A974;

border-radius: 50%;
}


.presynta-home-intro h2 {
margin-top: 1rem !important;
margin-bottom: 0.6rem !important;

color: #FFFFFF !important;

font-family: 'Manrope', sans-serif !important;
font-size: 2.2rem !important;
font-weight: 800 !important;

letter-spacing: -0.04em !important;
}


.presynta-home-intro p {
margin: 0 auto;

max-width: 540px;

color: #AAB4C5;

font-family: 'Manrope', sans-serif;

font-size: 0.95rem;

line-height: 1.7;
}


/* =========================================================
   PORTAL CONTAINERS
   ========================================================= */

div[data-testid="stVerticalBlockBorderWrapper"] {
border: 1px solid #263247 !important;
border-radius: 1.5rem !important;

background: #111A2B !important;

padding: 1.8rem !important;

transition:
transform 0.2s ease,
border-color 0.2s ease,
box-shadow 0.2s ease;
}


/* =========================================================
   PORTAL HEADINGS
   ========================================================= */

div[data-testid="stVerticalBlockBorderWrapper"] h2,
div[data-testid="stVerticalBlockBorderWrapper"] h3 {
color: #FFFFFF !important;

font-family: 'Manrope', sans-serif !important;

font-weight: 800 !important;

text-align: center;
}


/* =========================================================
   PORTAL IMAGES
   ========================================================= */

div[data-testid="stVerticalBlockBorderWrapper"] img {
display: block;

margin: 0.8rem auto 1.2rem;

object-fit: contain;

filter: drop-shadow(
0 8px 12px rgba(0, 0, 0, 0.18)
);
}


/* =========================================================
   PORTAL DESCRIPTION
   ========================================================= */

.presynta-portal-description {
text-align: center;

color: #475569;

font-family: 'Manrope', sans-serif;

font-size: 0.85rem;

line-height: 1.6;

margin-bottom: 1rem;
}


/* =========================================================
   PORTAL BUTTONS
   ========================================================= */

div[data-testid="stVerticalBlockBorderWrapper"] button {
background: #19A974 !important;

color: #FFFFFF !important;

border: none !important;

font-family: 'Manrope', sans-serif !important;

font-weight: 700 !important;
}


div[data-testid="stVerticalBlockBorderWrapper"] button:hover {
background: #159462 !important;

color: #FFFFFF !important;
}


/* =========================================================
   MOBILE
   ========================================================= */

@media (max-width: 768px) {

.presynta-home-intro {
margin-bottom: 1.5rem;
}


.presynta-home-intro h2 {
font-size: 1.75rem !important;
}


.presynta-home-intro p {
font-size: 0.9rem;
}


div[data-testid="stVerticalBlockBorderWrapper"] {
padding: 1.3rem !important;

border-radius: 1.2rem !important;
}

}


/* =========================================================
   VERY SMALL PHONES
   ========================================================= */

@media (max-width: 480px) {

.presynta-home-intro {
margin-bottom: 1.2rem;
}


.presynta-home-intro h2 {
font-size: 1.5rem !important;
}


.presynta-home-intro p {
font-size: 0.82rem;

line-height: 1.6;
}


.presynta-home-badge {
font-size: 0.55rem;

padding: 5px 9px;
}


div[data-testid="stVerticalBlockBorderWrapper"] {
padding: 1rem !important;

border-radius: 1rem !important;
}

}

</style>
        """,
        unsafe_allow_html=True,
    )


    # =========================================================
    # PORTAL CARDS
    # =========================================================

    col1, col2 = st.columns(
        2,
        gap="medium"
    )


    # =========================================================
    # STUDENT PORTAL
    # =========================================================

    with col1:

        with st.container(border=True):

            st.header(
                "I'm a Student",
                text_alignment="center"
            )

            st.image(
                "https://i.ibb.co/844D9Lrt/mascot-student.png",
                width=120
            )

            st.markdown(
                """
<div class="presynta-portal-description">
Access your subjects and manage your attendance.
</div>
                """,
                unsafe_allow_html=True,
            )

            if st.button(
                "Student Portal",
                type="primary",
                icon=":material/arrow_outward:",
                icon_position="right",
                width="stretch",
                key="student_portal_btn"
            ):

                st.session_state["login_type"] = "student"
                st.rerun()


    # =========================================================
    # TEACHER PORTAL
    # =========================================================

    with col2:

        with st.container(border=True):

            st.header(
                "I'm a Teacher",
                text_alignment="center"
            )

            st.image(
                "https://i.ibb.co/CsmQQV6X/mascot-prof.png",
                width=145
            )

            st.markdown(
                """
<div class="presynta-portal-description">
Create subjects, take attendance and view reports.
</div>
                """,
                unsafe_allow_html=True,
            )

            if st.button(
                "Teacher Portal",
                type="primary",
                icon=":material/arrow_outward:",
                icon_position="right",
                width="stretch",
                key="teacher_portal_btn"
            ):

                st.session_state["login_type"] = "teacher"
                st.rerun()


    footer_home()