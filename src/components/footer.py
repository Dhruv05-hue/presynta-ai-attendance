import streamlit as st


def footer_home():

    st.markdown(
        """
<div class="presynta-home-footer">

<div class="presynta-footer-line"></div>

<div class="presynta-footer-content">
<span>Powered by</span>
<strong>PRESYNTA</strong>
</div>

<div class="presynta-footer-line"></div>

<img
src="https://i.ibb.co/QzX7NZt/Dhruv-pawar-4.png"
alt="Developer"
class="presynta-footer-image"
/>

</div>

<style>

.presynta-home-footer {
margin-top: 2.5rem;
padding: 1rem 0 0.5rem;

display: flex;
flex-direction: column;
align-items: center;
justify-content: center;

gap: 10px;
}


.presynta-footer-line {
width: min(420px, 75%);
height: 1px;

background: #263247;
}


.presynta-footer-content {
display: flex;
align-items: center;

gap: 7px;

font-family: 'Manrope', sans-serif;
font-size: 0.75rem;

letter-spacing: 0.03em;
}


.presynta-footer-content span {
color: #8F9AAF;
}


.presynta-footer-content strong {
color: #19A974;

font-family: 'Space Grotesk', sans-serif;

font-weight: 700;

letter-spacing: 0.08em;
}


.presynta-footer-image {
max-width: 150px;
height: auto;

margin-top: 3px;

opacity: 0.85;
}


@media (max-width: 768px) {

.presynta-home-footer {
margin-top: 2rem;
}

.presynta-footer-line {
width: 70%;
}

.presynta-footer-content {
font-size: 0.7rem;
}

.presynta-footer-image {
max-width: 130px;
}

}


@media (max-width: 480px) {

.presynta-home-footer {
margin-top: 1.5rem;
}

.presynta-footer-line {
width: 80%;
}

.presynta-footer-content {
font-size: 0.65rem;
}

.presynta-footer-image {
max-width: 115px;
}

}

</style>
        """,
        unsafe_allow_html=True,
    )


def footer_dashboard():

    st.markdown(
        """
<div class="presynta-dashboard-footer">

<div class="presynta-dashboard-footer-content">
<strong> © 2026 PRESYNTA · AI Powered Attendance System </strong>
</div>

<img
src="https://i.ibb.co/QzX7NZt/Dhruv-pawar-4.png"
alt="Developer"
class="presynta-dashboard-footer-image"
/>

</div>

<style>

.presynta-dashboard-footer {
margin-top: 2.5rem;
padding: 1rem 0;

display: flex;
flex-direction: column;
align-items: center;
justify-content: center;

gap: 7px;
}


.presynta-dashboard-footer-content {
display: flex;
align-items: center;

gap: 6px;

font-family: 'Manrope', sans-serif;
font-size: 0.68rem;
}


.presynta-dashboard-footer-content span {
color: #8A93A1;
}


.presynta-dashboard-footer-content strong {
color: #19A974;

font-family: 'Space Grotesk', sans-serif;

font-weight: 700;

letter-spacing: 0.07em;
}


.presynta-dashboard-footer-image {
max-width: 95px;
height: auto;

opacity: 0.75;
}


@media (max-width: 768px) {

.presynta-dashboard-footer {
margin-top: 2rem;
}

.presynta-dashboard-footer-image {
max-width: 85px;
}

}


@media (max-width: 480px) {

.presynta-dashboard-footer {
margin-top: 1.5rem;
}

.presynta-dashboard-footer-image {
max-width: 75px;
}

}

</style>
        """,
        unsafe_allow_html=True,
    )