import streamlit as st


def subject_card(name, code, section, stats=None, footer_callback=None):

    html = f"""<div class="presynta-subject-card">

    <div class="presynta-subject-header">

        <div class="presynta-subject-title">
            <h3>{name}</h3>

            <p class="presynta-subject-info">
                <span>Code</span>
                <strong>{code}</strong>
                <span class="presynta-section-divider">•</span>
                <span>Section</span>
                <strong>{section}</strong>
            </p>
        </div>

        <div class="presynta-subject-indicator">
            <span></span>
            ACTIVE
        </div>

    </div>
"""

    if stats:
        html += """
    <div class="presynta-subject-stats">
"""

        for icon, label, value in stats:
            html += f"""
        <div class="presynta-subject-stat">

            <span class="presynta-stat-icon">
                {icon}
            </span>

            <div class="presynta-stat-content">
                <b>{value}</b>
                <span>{label}</span>
            </div>

        </div>
"""

        html += """
    </div>
"""

    html += """
</div>

<style>

    /* =========================================================
       SUBJECT CARD
       ========================================================= */

    .presynta-subject-card {
        width: 100%;
        box-sizing: border-box;

        background: #FFFFFF;

        border: 1px solid #DCE4DF;
        border-radius: 1.25rem;

        padding: 1.5rem;

        margin-bottom: 0rem;

        position: relative;
        overflow: hidden;

        transition:
            transform 0.2s ease,
            border-color 0.2s ease,
            box-shadow 0.2s ease;
    }


    .presynta-subject-card::before {
        content: "";

        position: absolute;
        left: 0;
        top: 0;
        bottom: 0;

        width: 4px;

        background: #19A974;
    }


    .presynta-subject-card:hover {
        transform: translateY(-3px);

        border-color: #B9DCCB;

        box-shadow: 0 10px 25px rgba(11, 18, 32, 0.07);
    }


    /* =========================================================
       HEADER
       ========================================================= */

    .presynta-subject-header {
        display: flex;
        align-items: flex-start;
        justify-content: space-between;

        gap: 1rem;
    }


    .presynta-subject-title {
        min-width: 0;
    }


    .presynta-subject-card h3 {
        margin: 0;

        color: #0B1220;

        font-family: 'Space Grotesk', sans-serif;

        font-size: 1.45rem;
        font-weight: 700;

        line-height: 1.2;
    }


    .presynta-subject-info {
        display: flex;
        align-items: center;
        flex-wrap: wrap;

        gap: 6px;

        margin: 9px 0 0;

        color: #475569;

        font-family: 'Manrope', sans-serif;

        font-size: 0.85rem;

        line-height: 1.5;
    }


    .presynta-subject-info strong {
        color: #263247;

        font-weight: 700;

        background: #F0F5F2;

        padding: 3px 8px;

        border-radius: 6px;
    }


    .presynta-section-divider {
        color: #94A3B8;

        margin: 0 2px;
    }


    /* =========================================================
       ACTIVE INDICATOR
       ========================================================= */

    .presynta-subject-indicator {
        flex-shrink: 0;

        display: flex;
        align-items: center;

        gap: 6px;

        padding: 5px 9px;

        background: #E8F5EF;

        color: #12845A;

        border-radius: 999px;

        font-family: 'Manrope', sans-serif;

        font-size: 0.65rem;

        font-weight: 800;

        letter-spacing: 0.05em;
    }


    .presynta-subject-indicator span {
        width: 6px;
        height: 6px;

        border-radius: 50%;

        background: #19A974;
    }


    /* =========================================================
       STATISTICS
       ========================================================= */

    .presynta-subject-stats {
        display: grid;

        grid-template-columns: repeat(
            auto-fit,
            minmax(130px, 1fr)
        );

        gap: 10px;

        margin-top: 1.25rem;

        padding-top: 1.15rem;

        border-top: 1px solid #EDF1EE;
    }


    .presynta-subject-stat {
        display: flex;
        align-items: center;

        gap: 9px;

        background: #F7F9F8;

        border: 1px solid #E8EDE9;

        padding: 9px 11px;

        border-radius: 0.8rem;

        box-sizing: border-box;
    }


    .presynta-stat-icon {
        width: 30px;
        height: 30px;

        display: flex;
        align-items: center;
        justify-content: center;

        background: #E8F5EF;

        color: #19A974;

        border-radius: 0.6rem;

        font-size: 0.9rem;

        flex-shrink: 0;
    }


    .presynta-stat-content {
        display: flex;
        flex-direction: column;

        min-width: 0;
    }


    .presynta-stat-content b {
        color: #172033;

        font-family: 'Space Grotesk', sans-serif;

        font-size: 1rem;

        line-height: 1.2;
    }


    .presynta-stat-content span {
        color: #475569;

        font-family: 'Manrope', sans-serif;

        font-size: 0.7rem;

        margin-top: 2px;
    }


    /* =========================================================
       MOBILE
       ========================================================= */

    @media (max-width: 768px) {

        .presynta-subject-card {
            padding: 1.2rem;

            border-radius: 1rem;

            margin-bottom: 0.85rem;
        }


        .presynta-subject-header {
            gap: 0.7rem;
        }


        .presynta-subject-card h3 {
            font-size: 1.25rem;
        }


        .presynta-subject-info {
            font-size: 0.8rem;
        }


        .presynta-subject-indicator {
            padding: 4px 7px;

            font-size: 0.58rem;
        }


        .presynta-subject-stats {
            grid-template-columns: repeat(2, 1fr);

            gap: 7px;

            margin-top: 1rem;

            padding-top: 1rem;
        }


        .presynta-subject-stat {
            padding: 8px;
        }


        .presynta-stat-icon {
            width: 27px;
            height: 27px;
        }

    }


    /* =========================================================
       VERY SMALL PHONES
       ========================================================= */

    @media (max-width: 480px) {

        .presynta-subject-card {
            padding: 1rem;

            border-radius: 0.9rem;
        }


        .presynta-subject-header {
            flex-direction: column;
        }


        .presynta-subject-card h3 {
            font-size: 1.15rem;
        }


        .presynta-subject-info {
            font-size: 0.75rem;
        }


        .presynta-subject-indicator {
            align-self: flex-start;
        }


        .presynta-subject-stats {
            grid-template-columns: 1fr;
        }


        .presynta-subject-stat {
            padding: 8px 10px;
        }

    }

</style>
"""

    st.html(html)

    if footer_callback:
        footer_callback()