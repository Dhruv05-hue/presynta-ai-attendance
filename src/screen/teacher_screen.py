import streamlit as st

from src.components.header import header_dashboard, header_home
from src.ui.base_layout import style_background_dashboard, style_base_layout
from src.components.footer import footer_dashboard
from src.database.db import (
    create_teacher,
    check_teacher_exists,
    teacher_login,
    get_teacher_subject,
    get_attendance_for_teacher
)
from src.components.dialog_create_subject import create_subject_dialog
from src.components.subject_card import subject_card
from src.components.dialog_share_subject import share_subject_dialog
from src.components.dialog_add_photo import add_photos_dialog
from src.database.config import supabase
from src.pipelines.face_pipeline import predict_attendance
from src.components.dialog_attendance_result import attendance_result_dialog
from src.components.dialog_voice_attendance import voice_attendance_dialog

from datetime import datetime
import pandas as pd
import numpy as np


# =============================================================
# TEACHER SCREEN
# =============================================================

def teacher_screen():

    style_base_layout()
    style_background_dashboard()

    if "teacher_data" in st.session_state:
        teacher_dashboard()

    elif (
        "teacher_login_type" not in st.session_state
        or st.session_state.teacher_login_type == "login"
    ):
        teacher_screen_login()

    elif st.session_state.teacher_login_type == "register":
        teacher_screen_register()


# =============================================================
# TEACHER LOGIN FUNCTION
# =============================================================

def login_teacher(username, password):

    if not username or not password:
        return False

    teacher = teacher_login(username, password)

    if teacher:

        st.session_state.user_role = "teacher"
        st.session_state.teacher_data = teacher
        st.session_state.is_logged_in = True

        return True

    return False


# =============================================================
# TEACHER DASHBOARD
# =============================================================

def teacher_dashboard():

    teacher_data = st.session_state.teacher_data

    # ---------------------------------------------------------
    # Dashboard header
    # ---------------------------------------------------------

    c1, c2 = st.columns(
        [2.2, 1],
        vertical_alignment="center",
        gap="large"
    )

    with c1:
        header_dashboard()

    with c2:

        st.markdown(
            f"""
            <div class="presynta-teacher-welcome">
                <span>WELCOME BACK</span>
                <strong>{teacher_data["name"]}</strong>
            </div>
            """,
            unsafe_allow_html=True
        )

        if st.button(
            "Logout",
            type="secondary",
            key="loginbackbtn",
            shortcut="control+backspace",
            width="stretch"
        ):

            st.session_state["is_logged_in"] = False

            del st.session_state.teacher_data

            st.rerun()

    # ---------------------------------------------------------
    # Dashboard introduction
    # ---------------------------------------------------------

    st.html(
        """<div class="presynta-teacher-intro">

            <div class="presynta-teacher-label">
                TEACHER DASHBOARD
            </div>

            <h2>Manage your classroom</h2>

            <p>
                Take intelligent attendance, manage your subjects,
                and review student attendance records from one place.
            </p>

        </div>
        """
    )

    # ---------------------------------------------------------
    # Dashboard navigation
    # ---------------------------------------------------------

    if "current_teacher_tab" not in st.session_state:
        st.session_state.current_teacher_tab = "take_attendence"

    tab1, tab2, tab3 = st.columns(3, gap="small")

    with tab1:

        type1 = (
            "primary"
            if st.session_state.current_teacher_tab == "take_attendence"
            else "tertiary"
        )

        if st.button(
            "Take Attendance",
            type=type1,
            width="stretch",
            icon=":material/face:"
        ):

            st.session_state.current_teacher_tab = "take_attendence"
            st.rerun()

    with tab2:

        type2 = (
            "primary"
            if st.session_state.current_teacher_tab == "manage_subjects"
            else "tertiary"
        )

        if st.button(
            "Manage Subjects",
            type=type2,
            width="stretch",
            icon=":material/menu_book:"
        ):

            st.session_state.current_teacher_tab = "manage_subjects"
            st.rerun()

    with tab3:

        type3 = (
            "primary"
            if st.session_state.current_teacher_tab == "attendence_record"
            else "tertiary"
        )

        if st.button(
            "Attendance Records",
            type=type3,
            width="stretch",
            icon=":material/analytics:"
        ):

            st.session_state.current_teacher_tab = "attendence_record"
            st.rerun()

    st.divider()

    # ---------------------------------------------------------
    # Selected tab
    # ---------------------------------------------------------

    if st.session_state.current_teacher_tab == "take_attendence":

        teacher_tab_take_attendance()

    if st.session_state.current_teacher_tab == "manage_subjects":

        teacher_tab_manage_subjects()

    if st.session_state.current_teacher_tab == "attendence_record":

        teacher_tab_attendance_records()

    footer_dashboard()


# =============================================================
# TEACHER - TAKE ATTENDANCE
# =============================================================

def teacher_tab_take_attendance():

    teacher_id = st.session_state.teacher_data["teacher_id"]

    st.html(
        """<div class="presynta-section-heading">

            <div class="presynta-section-label">
                AI ATTENDANCE
            </div>

            <h2>Take classroom attendance</h2>

            <p>
                Select a subject, add classroom photos, and let
                Presynta recognize enrolled students automatically.
            </p>

        </div>
        """
    )

    # ---------------------------------------------------------
    # Initialize attendance images
    # ---------------------------------------------------------

    if "attendance_images" not in st.session_state:
        st.session_state.attendance_images = []

    # ---------------------------------------------------------
    # Get teacher subjects
    # ---------------------------------------------------------

    subjects = get_teacher_subject(teacher_id)

    if not subjects:

        st.markdown(
            """
            <div class="presynta-empty-state">

                <div class="presynta-empty-icon">
                    +
                </div>

                <h3>No subjects yet</h3>

                <p>
                    Create your first subject before taking attendance.
                </p>

            </div>
            """,
            unsafe_allow_html=True
        )

        return

    # ---------------------------------------------------------
    # Subject options
    # ---------------------------------------------------------

    subject_options = {
        f"{s['name']} · {s['subject_code']}": s["subject_id"]
        for s in subjects
    }

    # ---------------------------------------------------------
    # Subject selection + add photos
    # ---------------------------------------------------------

    col1, col2 = st.columns(
        [3, 1],
        vertical_alignment="bottom"
    )

    with col1:

        selected_subject_label = st.selectbox(
            "Select Subject",
            options=list(subject_options.keys())
        )

    with col2:

        if st.button(
            "Add Photos",
            type="primary",
            icon=":material/add_photo_alternate:",
            width="stretch"
        ):

            add_photos_dialog()

    selected_subject_id = subject_options[selected_subject_label]

    st.divider()

    # ---------------------------------------------------------
    # Added photos
    # ---------------------------------------------------------

    if st.session_state.attendance_images:

        st.html(
            """<div class="presynta-content-heading">

                <h3>Added Photos</h3>

                <span>
                    Review your classroom images before scanning.
                </span>

            </div>
            """
        )

        gallery_cols = st.columns(4, gap="small")

        for idx, img in enumerate(
            st.session_state.attendance_images
        ):

            with gallery_cols[idx % 4]:

                st.image(
                    img,
                    width="stretch",
                    caption=f"Photo {idx + 1}"
                )

        st.divider()

    # ---------------------------------------------------------
    # Attendance actions
    # ---------------------------------------------------------

    has_photos = bool(
        st.session_state.attendance_images
    )

    c1, c2, c3 = st.columns(
        3,
        gap="small"
    )

    # ---------------------------------------------------------
    # Clear photos
    # ---------------------------------------------------------

    with c1:

        if st.button(
            "Clear Photos",
            width="stretch",
            type="tertiary",
            icon=":material/delete:",
            key="clear_all_photos",
            disabled=not has_photos
        ):

            st.session_state.attendance_images = []

            st.rerun()

    # ---------------------------------------------------------
    # Face analysis
    # ---------------------------------------------------------

    with c2:

        if st.button(
            "Run Face Analysis",
            width="stretch",
            type="secondary",
            icon=":material/face_retouching_natural:",
            key="run_face_analysis",
            disabled=not has_photos
        ):

            with st.spinner(
                "Analyzing classroom photos..."
            ):

                all_detected_ids = {}

                # Analyze every photo
                for idx, img in enumerate(
                    st.session_state.attendance_images
                ):

                    img_np = np.array(
                        img.convert("RGB")
                    )

                    detected, _, _ = predict_attendance(
                        img_np
                    )

                    if detected:

                        for sid in detected.keys():

                            student_id = int(sid)

                            all_detected_ids.setdefault(
                                student_id,
                                []
                            ).append(
                                f"Photo {idx + 1}"
                            )

                # Get enrolled students
                enrolled_res = (
                    supabase
                    .table("subject_students")
                    .select("*,students(*)")
                    .eq(
                        "subject_id",
                        selected_subject_id
                    )
                    .execute()
                )

                enrolled_students = enrolled_res.data

                if not enrolled_students:

                    st.warning(
                        "No students enrolled in this course"
                    )

                else:

                    result = []
                    attendance_to_log = []

                    current_timestamp = (
                        datetime.now()
                        .strftime(
                            "%Y-%m-%dT%H:%M:%S"
                        )
                    )

                    # Check every enrolled student
                    for node in enrolled_students:

                        student = node["students"]

                        sources = all_detected_ids.get(
                            int(student["student_id"]),
                            []
                        )

                        is_present = len(sources) > 0

                        result.append(
                            {
                                "Name": student["name"],
                                "ID": student["student_id"],
                                "Source": (
                                    ",".join(sources)
                                    if is_present
                                    else "-"
                                ),
                                "Status": (
                                    "✅ Present"
                                    if is_present
                                    else "❌ Absent"
                                )
                            }
                        )

                        attendance_to_log.append(
                            {
                                "student_id": student["student_id"],
                                "subject_id": selected_subject_id,
                                "timestamp": current_timestamp,
                                "is_present": bool(
                                    is_present
                                )
                            }
                        )

                    attendance_result_dialog(
                        pd.DataFrame(result),
                        attendance_to_log
                    )

    # ---------------------------------------------------------
    # Voice attendance
    # ---------------------------------------------------------

    with c3:

        if st.button(
            "Voice Attendance",
            type="primary",
            width="stretch",
            icon=":material/mic:",
            key="voice_attendance"
        ):

            voice_attendance_dialog(
                selected_subject_id
            )


# =============================================================
# TEACHER - MANAGE SUBJECTS
# =============================================================

def teacher_tab_manage_subjects():

    teacher_id = st.session_state.teacher_data["teacher_id"]

    st.html(
        """<div class="presynta-section-heading">

            <div class="presynta-section-label">
                CLASSROOM MANAGEMENT
            </div>

            <h2>Manage your subjects</h2>

            <p>
                Create subjects, invite students, and manage
                your classroom enrollment.
            </p>

        </div>
        """
    )

    col1, col2 = st.columns(
        [1.6, 1],
        vertical_alignment="center"
    )

    with col1:

        st.html(
            """<div class="presynta-subject-helper">
                <strong>Your Subjects</strong>
                <span>
                    Share enrollment codes with your students.
                </span>
            </div>
            """
        )

    with col2:

        if st.button(
            "Create New Subject",
            width="stretch",
            type="primary",
            icon=":material/add:"
        ):

            create_subject_dialog(
                teacher_id
            )

    st.divider()

    # ---------------------------------------------------------
    # List subjects
    # ---------------------------------------------------------

    subjects = get_teacher_subject(teacher_id)

    if subjects:

        for sub in subjects:

            stats = [
                (
                    "👥",
                    "Students",
                    sub["total_students"]
                ),
                (
                    "📅",
                    "Classes",
                    sub["total_classes"]
                )
            ]

            def share_btn():

                if st.button(
                    f"Share {sub['name']}",
                    key=f"share_{sub['subject_code']}",
                    icon=":material/share:",
                    type="primary",
                    width=250
                ):

                    share_subject_dialog(
                        sub["name"],
                        sub["subject_code"]
                    )

            subject_card(
                name=sub["name"],
                code=sub["subject_code"],
                section=sub["section"],
                stats=stats,
                footer_callback=share_btn
            )

    else:

        st.markdown(
            """<div class="presynta-empty-state">

                <div class="presynta-empty-icon">
                    +
                </div>

                <h3>No subjects found</h3>

                <p>
                    Create a subject to start building your classroom.
                </p>

            </div>
            """
        )


# =============================================================
# TEACHER - ATTENDANCE RECORDS
# =============================================================

def teacher_tab_attendance_records():

    # =========================================================
    # SECTION HEADER
    # =========================================================

    st.html(
        """
        <div class="presynta-section-heading">

            <div class="presynta-section-label">
                ATTENDANCE ANALYTICS
            </div>

            <h2>Attendance records</h2>

            <p>
                Review attendance by subject and class session.
                Select a subject to view detailed student records.
            </p>

        </div>
        """
    )

    teacher_id = st.session_state.teacher_data["teacher_id"]

    # =========================================================
    # LOAD RECORDS
    # =========================================================

    records = get_attendance_for_teacher(
        teacher_id
    )

    # =========================================================
    # EMPTY STATE
    # =========================================================

    if not records:

        st.html(
            """
            <div class="presynta-empty-state">

                <div class="presynta-empty-icon">
                    —
                </div>

                <h3>No attendance records</h3>

                <p>
                    Attendance sessions will appear here
                    after you record your first class.
                </p>

            </div>
            """
        )

        return

    # =========================================================
    # PREPARE DATA
    # =========================================================

    attendance_data = []

    for record in records:

        timestamp = record.get("timestamp")

        subject = record.get("subjects")

        student = record.get("students")

        if not timestamp or not subject:
            continue

        # -----------------------------------------------------
        # STUDENT INFORMATION
        # -----------------------------------------------------

        if isinstance(student, dict):

            student_id = student.get(
                "student_id"
            )

            student_name = student.get(
                "name",
                "Unknown Student"
            )

        else:

            student_id = record.get(
                "student_id"
            )

            student_name = "Unknown Student"

        # -----------------------------------------------------
        # TIMESTAMP
        # -----------------------------------------------------

        try:

            session_datetime = datetime.fromisoformat(
                timestamp.replace(
                    "Z",
                    "+00:00"
                )
            )

            display_time = session_datetime.strftime(
                "%d %B %Y • %I:%M %p"
            )

        except Exception:

            session_datetime = None

            display_time = timestamp

        # -----------------------------------------------------
        # SESSION KEY
        # -----------------------------------------------------

        session_key = (
            f"{subject.get('subject_id')}_"
            f"{timestamp.split('.')[0]}"
        )

        # -----------------------------------------------------
        # STORE DATA
        # -----------------------------------------------------

        attendance_data.append(
            {
                "session_key": session_key,

                "timestamp": timestamp,

                "datetime": session_datetime,

                "display_time": display_time,

                "subject_id": subject.get(
                    "subject_id"
                ),

                "subject_name": subject.get(
                    "name",
                    "Unknown Subject"
                ),

                "subject_code": subject.get(
                    "subject_code",
                    "N/A"
                ),

                "student_id": student_id,

                "student_name": student_name,

                "is_present": bool(
                    record.get(
                        "is_present",
                        False
                    )
                )
            }
        )

    # =========================================================
    # CHECK VALID DATA
    # =========================================================

    if not attendance_data:

        st.warning(
            "Attendance records could not be displayed."
        )

        return

    # =========================================================
    # DATAFRAME
    # =========================================================

    df = pd.DataFrame(
        attendance_data
    )

    # =========================================================
    # SUBJECTS
    # =========================================================

    subjects = (
        df[
            [
                "subject_id",
                "subject_name",
                "subject_code"
            ]
        ]
        .drop_duplicates()
        .sort_values(
            "subject_name"
        )
    )

    # =========================================================
    # SESSION STATE
    # =========================================================

    if "attendance_selected_subject" not in st.session_state:

        st.session_state.attendance_selected_subject = None

    if "attendance_selected_session" not in st.session_state:

        st.session_state.attendance_selected_session = None

    # =========================================================
    # CSS
    # =========================================================

    st.html(
        """
        <style>

        /* =====================================================
           SUBJECT SECTION
           ===================================================== */

        .presynta-attendance-section {
            margin-top: 1.5rem;
        }


        .presynta-attendance-section-label {

            color: #12845A;

            font-family: 'Manrope', sans-serif;

            font-size: 0.7rem;

            font-weight: 800;

            letter-spacing: 0.12em;

            margin-bottom: 0.45rem;
        }


        .presynta-attendance-section-title {

            color: #0B1220;

            font-family: 'Space Grotesk', sans-serif;

            font-size: 1.55rem;

            font-weight: 700;

            margin-bottom: 1rem;
        }


        /* =====================================================
           SUBJECT CARD
           ===================================================== */

        .presynta-attendance-subject-card {

            background: #FFFFFF;

            border: 1px solid #DCE4DF;

            border-left: 4px solid #19A974;

            border-radius: 1.2rem;

            padding: 1.35rem;

            margin-bottom: 0.55rem;

            transition:
                border-color 0.2s ease,
                box-shadow 0.2s ease;
        }


        .presynta-attendance-subject-card:hover {

            border-color: #B9DCCB;

            box-shadow:
                0 8px 22px
                rgba(11, 18, 32, 0.06);
        }


        .presynta-attendance-subject-name {

            color: #0B1220;

            font-family: 'Space Grotesk', sans-serif;

            font-size: 1.35rem;

            font-weight: 700;

            margin-bottom: 0.35rem;
        }


        .presynta-attendance-subject-meta {

            color: #697586;

            font-family: 'Manrope', sans-serif;

            font-size: 0.78rem;
        }


        .presynta-attendance-subject-meta strong {

            color: #263247;

            background: #F0F5F2;

            padding: 3px 8px;

            border-radius: 6px;

            font-weight: 700;
        }


        .presynta-attendance-subject-stats {

            display: flex;

            gap: 8px;

            margin-top: 0.9rem;

            flex-wrap: wrap;
        }


        .presynta-attendance-stat {

            background: #F7F9F8;

            border: 1px solid #E8EDE9;

            border-radius: 0.65rem;

            padding: 6px 10px;

            color: #596579;

            font-family: 'Manrope', sans-serif;

            font-size: 0.7rem;
        }


        .presynta-attendance-stat strong {

            color: #172033;

            font-weight: 800;
        }


        /* =====================================================
           SESSION
           ===================================================== */

        .presynta-session-header {

            margin-top: 1.5rem;

            margin-bottom: 1rem;
        }


        .presynta-session-label {

            color: #12845A;

            font-family: 'Manrope', sans-serif;

            font-size: 0.68rem;

            font-weight: 800;

            letter-spacing: 0.1em;
        }


        .presynta-session-title {

            color: #0B1220;

            font-family: 'Space Grotesk', sans-serif;

            font-size: 1.5rem;

            font-weight: 700;

            margin-top: 4px;
        }


        .presynta-session-subtitle {

            color: #697586;

            font-family: 'Manrope', sans-serif;

            font-size: 0.8rem;

            margin-top: 4px;
        }


        .presynta-session-card {

            background: #FFFFFF;

            border: 1px solid #DCE4DF;

            border-radius: 1rem;

            padding: 1.15rem;

            margin-bottom: 0.45rem;
        }


        .presynta-session-date {

            color: #172033;

            font-family: 'Space Grotesk', sans-serif;

            font-size: 1rem;

            font-weight: 700;
        }


        .presynta-session-stats {

            display: flex;

            gap: 7px;

            flex-wrap: wrap;

            margin-top: 0.65rem;
        }


        .presynta-session-present {

            color: #12845A;

            background: #E8F5EF;

            border: 1px solid #CDE8DB;

            border-radius: 999px;

            padding: 4px 9px;

            font-family: 'Manrope', sans-serif;

            font-size: 0.68rem;

            font-weight: 800;
        }


        .presynta-session-absent {

            color: #B42318;

            background: #FFF1F1;

            border: 1px solid #F2CACA;

            border-radius: 999px;

            padding: 4px 9px;

            font-family: 'Manrope', sans-serif;

            font-size: 0.68rem;

            font-weight: 800;
        }


        /* =====================================================
           CLASS ATTENDANCE
           ===================================================== */

        .presynta-class-summary {

            display: grid;

            grid-template-columns:
                repeat(3, 1fr);

            gap: 10px;

            margin: 1rem 0;
        }


        .presynta-class-summary-item {

            background: #FFFFFF;

            border: 1px solid #DCE4DF;

            border-radius: 0.9rem;

            padding: 0.9rem;
        }


        .presynta-class-summary-item span {

            display: block;

            color: #697586;

            font-family: 'Manrope', sans-serif;

            font-size: 0.68rem;
        }


        .presynta-class-summary-item strong {

            display: block;

            color: #172033;

            font-family: 'Space Grotesk', sans-serif;

            font-size: 1.2rem;

            margin-top: 3px;
        }


        /* =====================================================
           DETAIL TABLE CONTAINER
           ===================================================== */

        .presynta-class-detail {

            background: #F7F9F8;

            border: 1px solid #DCE4DF;

            border-radius: 1rem;

            padding: 1rem;

            margin-top: 0.7rem;

            margin-bottom: 1rem;
        }


        /* =====================================================
           MOBILE
           ===================================================== */

        @media (max-width: 768px) {

            .presynta-class-summary {

                grid-template-columns:
                    repeat(3, 1fr);

                gap: 7px;
            }

        }


        @media (max-width: 480px) {

            .presynta-class-summary {

                grid-template-columns: 1fr;
            }


            .presynta-attendance-subject-card {

                padding: 1rem;
            }


            .presynta-attendance-subject-name {

                font-size: 1.2rem;
            }

        }

        </style>
        """
    )

    # =========================================================
    # SUBJECT DETAIL VIEW
    # =========================================================

    selected_subject_id = (
        st.session_state.attendance_selected_subject
    )

    if selected_subject_id is not None:

        selected_subject_rows = df[
            df["subject_id"] == selected_subject_id
        ]

        if selected_subject_rows.empty:

            st.session_state.attendance_selected_subject = None

            st.session_state.attendance_selected_session = None

            st.rerun()

        subject_name = (
            selected_subject_rows[
                "subject_name"
            ].iloc[0]
        )

        subject_code = (
            selected_subject_rows[
                "subject_code"
            ].iloc[0]
        )

        # =====================================================
        # BACK TO SUBJECTS
        # =====================================================

        if st.button(
            "Back to Subjects",
            type="tertiary",
            icon=":material/arrow_back:"
        ):

            st.session_state.attendance_selected_subject = None

            st.session_state.attendance_selected_session = None

            st.rerun()

        # =====================================================
        # SUBJECT HEADER
        # =====================================================

        st.html(
            f"""
            <div class="presynta-session-header">

                <div class="presynta-session-label">
                    SUBJECT ATTENDANCE
                </div>

                <div class="presynta-session-title">
                    {subject_name}
                </div>

                <div class="presynta-session-subtitle">
                    Subject Code:
                    <strong>{subject_code}</strong>
                </div>

            </div>
            """
        )

        # =====================================================
        # GET ALL SESSIONS
        # =====================================================

        subject_sessions = (
            selected_subject_rows[
                [
                    "session_key",
                    "timestamp",
                    "display_time",
                    "datetime"
                ]
            ]
            .drop_duplicates(
                subset=["session_key"]
            )
            .sort_values(
                by="timestamp",
                ascending=False
            )
        )

        st.html(
            """
            <div class="presynta-attendance-section-title">
                Attendance Sessions
            </div>
            """
        )

        # =====================================================
        # SESSION LOOP
        # =====================================================

        for index, session in (
            subject_sessions.iterrows()
        ):

            session_key = session[
                "session_key"
            ]

            session_rows = df[
                df["session_key"] == session_key
            ].copy()

            total_students = len(
                session_rows
            )

            present_students = int(
                session_rows[
                    "is_present"
                ].sum()
            )

            absent_students = (
                total_students
                - present_students
            )

            # =================================================
            # SESSION CARD
            # =================================================

            st.html(
                f"""
                <div class="presynta-session-card">

                    <div class="presynta-session-date">
                        {session["display_time"]}
                    </div>

                    <div class="presynta-session-stats">

                        <span class="presynta-session-present">
                            ✓ {present_students} Present
                        </span>

                        <span class="presynta-session-absent">
                            ✕ {absent_students} Absent
                        </span>

                    </div>

                </div>
                """
            )

            # =================================================
            # VIEW CLASS ATTENDANCE BUTTON
            # =================================================

            if st.button(
                "View Class Attendance",
                key=f"view_session_{session_key}",
                type="primary",
                icon=":material/visibility:"
            ):

                st.session_state.attendance_selected_session = (
                    session_key
                )

                st.rerun()

            # =================================================
            # IMPORTANT:
            # SHOW DETAILS IMMEDIATELY BELOW THIS SESSION
            # =================================================

            selected_session = (
                st.session_state
                .attendance_selected_session
            )

            if selected_session == session_key:

                # ---------------------------------------------
                # CLASS DETAIL CONTAINER
                # ---------------------------------------------

                st.html(
                    """
                    <div class="presynta-class-detail">
                    """
                )

                # ---------------------------------------------
                # CLASS HEADER
                # ---------------------------------------------

                st.html(
                    f"""
                    <div class="presynta-session-header">

                        <div class="presynta-session-label">
                            CLASS ATTENDANCE
                        </div>

                        <div class="presynta-session-title">
                            {subject_name}
                        </div>

                        <div class="presynta-session-subtitle">
                            {session["display_time"]}
                        </div>

                    </div>
                    """
                )

                # ---------------------------------------------
                # SUMMARY
                # ---------------------------------------------

                st.html(
                    f"""
                    <div class="presynta-class-summary">

                        <div class="presynta-class-summary-item">

                            <span>
                                Total Students
                            </span>

                            <strong>
                                {total_students}
                            </strong>

                        </div>


                        <div class="presynta-class-summary-item">

                            <span>
                                Present
                            </span>

                            <strong>
                                {present_students}
                            </strong>

                        </div>


                        <div class="presynta-class-summary-item">

                            <span>
                                Absent
                            </span>

                            <strong>
                                {absent_students}
                            </strong>

                        </div>

                    </div>
                    """
                )

                # ---------------------------------------------
                # STUDENT TABLE
                # ---------------------------------------------

                table_data = []

                sorted_students = (
                    session_rows
                    .sort_values(
                        "student_name"
                    )
                )

                for _, row in (
                    sorted_students.iterrows()
                ):

                    table_data.append(
                        {
                            "Student Name":
                                row[
                                    "student_name"
                                ],

                            "Student ID":
                                row[
                                    "student_id"
                                ],

                            "Date & Time":
                                row[
                                    "display_time"
                                ],

                            "Attendance":
                                (
                                    "✅ Present"
                                    if row[
                                        "is_present"
                                    ]
                                    else
                                    "❌ Absent"
                                )
                        }
                    )

                student_df = pd.DataFrame(
                    table_data
                )

                st.dataframe(
                    student_df,
                    width="stretch",
                    hide_index=True
                )

                # ---------------------------------------------
                # CLOSE DETAIL
                # ---------------------------------------------

                if st.button(
                    "Close Class Attendance",
                    key=f"close_session_{session_key}",
                    type="tertiary",
                    icon=":material/close:"
                ):

                    st.session_state.attendance_selected_session = None

                    st.rerun()

                st.html(
                    """
                    </div>
                    """
                )

        return

    # =========================================================
    # SUBJECT VIEW
    # =========================================================

    st.html(
        """
        <div class="presynta-attendance-section">

            <div class="presynta-attendance-section-label">
                YOUR SUBJECTS
            </div>

            <div class="presynta-attendance-section-title">
                Attendance by subject
            </div>

        </div>
        """
    )

    # =========================================================
    # SUBJECT CARDS
    # =========================================================

    for _, subject in subjects.iterrows():

        subject_id = subject[
            "subject_id"
        ]

        subject_name = subject[
            "subject_name"
        ]

        subject_code = subject[
            "subject_code"
        ]

        subject_df = df[
            df["subject_id"] == subject_id
        ]

        session_count = (
            subject_df[
                "session_key"
            ]
            .nunique()
        )

        student_count = (
            subject_df[
                "student_id"
            ]
            .nunique()
        )

        # =====================================================
        # SUBJECT CARD
        # =====================================================

        st.html(
            f"""
            <div class="presynta-attendance-subject-card">

                <div class="presynta-attendance-subject-name">
                    {subject_name}
                </div>

                <div class="presynta-attendance-subject-meta">

                    Code

                    <strong>
                        {subject_code}
                    </strong>

                </div>

                <div class="presynta-attendance-subject-stats">

                    <span class="presynta-attendance-stat">

                        <strong>
                            {session_count}
                        </strong>

                        Classes

                    </span>


                    <span class="presynta-attendance-stat">

                        <strong>
                            {student_count}
                        </strong>

                        Students

                    </span>

                </div>

            </div>
            """
        )

        # =====================================================
        # VIEW SUBJECT ATTENDANCE
        # =====================================================

        if st.button(
            f"View {subject_name} Attendance",
            key=f"view_subject_{subject_id}",
            type="primary",
            icon=":material/arrow_forward:"
        ):

            st.session_state.attendance_selected_subject = (
                subject_id
            )

            st.session_state.attendance_selected_session = None

            st.rerun()

# =============================================================
# TEACHER REGISTRATION
# =============================================================

def register_teacher(
    teacher_username,
    teacher_name,
    teacher_pass,
    teacher_pass_confirm
):

    if (
        not teacher_username
        or not teacher_name
        or not teacher_pass
    ):

        return False, "All fields are required!"

    if check_teacher_exists(
        teacher_username
    ):

        return False, "Username already taken"

    if teacher_pass != teacher_pass_confirm:

        return False, "Password doesn't match"

    try:

        create_teacher(
            teacher_username,
            teacher_pass,
            teacher_name
        )

        return True, "Successfully Created! Login Now"

    except Exception:

        return False, "Unexpected Error!"


# =============================================================
# TEACHER LOGIN SCREEN
# =============================================================

def teacher_screen_login():

    c1, c2 = st.columns(
        [2.2, 1],
        vertical_alignment="center",
        gap="large"
    )

    with c1:

        header_dashboard()

    with c2:

        if st.button(
            "Go back to Home",
            type="secondary",
            key="loginbackbtn",
            shortcut="control+backspace",
            width="stretch"
        ):

            st.session_state["login_type"] = None

            st.rerun()

    # ---------------------------------------------------------
    # Login introduction
    # ---------------------------------------------------------

    st.html(
        """<div class="presynta-auth-section">

            <div class="presynta-auth-badge">
                <span></span>
                TEACHER ACCESS
            </div>

            <h2>Welcome back</h2>

            <p>
                Sign in to manage your subjects, take
                AI-powered attendance, and view reports.
            </p>

        </div>
        """
    )

    # ---------------------------------------------------------
    # Login form
    # ---------------------------------------------------------

    teacher_username = st.text_input(
        "Username",
        placeholder="Enter your username"
    )

    teacher_password = st.text_input(
        "Password",
        type="password",
        placeholder="Enter your password"
    )

    st.divider()

    btncol1, btncol2 = st.columns(
        2,
        gap="small"
    )

    with btncol1:

        if st.button(
            "Login",
            icon=":material/login:",
            shortcut="control+enter",
            width="stretch",
            type="primary"
        ):

            if login_teacher(
                teacher_username,
                teacher_password
            ):

                st.toast(
                    "Welcome back!",
                    icon="👋"
                )

                import time

                time.sleep(1)

                st.rerun()

            else:

                st.error(
                    "Invalid username and password combination"
                )

    with btncol2:

        if st.button(
            "Create Teacher Account",
            type="tertiary",
            icon=":material/person_add:",
            width="stretch"
        ):

            st.session_state.teacher_login_type = "register"

            st.rerun()

    footer_dashboard()


# =============================================================
# TEACHER REGISTRATION SCREEN
# =============================================================

def teacher_screen_register():

    c1, c2 = st.columns(
        [2.2, 1],
        vertical_alignment="center",
        gap="large"
    )

    with c1:

        header_dashboard()

    with c2:

        if st.button(
            "Go back to Home",
            type="secondary",
            key="loginbackbtn",
            shortcut="control+backspace",
            width="stretch"
        ):

            st.session_state["login_type"] = None

            st.rerun()

    # ---------------------------------------------------------
    # Registration introduction
    # ---------------------------------------------------------

    st.html(
        """<div class="presynta-auth-section">

            <div class="presynta-auth-badge">
                <span></span>
                TEACHER REGISTRATION
            </div>

            <h2>Create your profile</h2>

            <p>
                Set up your teacher account to create subjects,
                invite students, and manage attendance.
            </p>

        </div>
        """
    )

    # ---------------------------------------------------------
    # Registration fields
    # ---------------------------------------------------------

    teacher_username = st.text_input(
        "Username",
        placeholder="Choose a username"
    )

    teacher_name = st.text_input(
        "Full name",
        placeholder="e.g. Ananya Roy"
    )

    teacher_pass = st.text_input(
        "Password",
        type="password",
        placeholder="Create a password"
    )

    teacher_pass_confirm = st.text_input(
        "Confirm password",
        type="password",
        placeholder="Re-enter your password"
    )

    st.divider()

    btncol1, btncol2 = st.columns(
        2,
        gap="small"
    )

    with btncol1:

        if st.button(
            "Create Account",
            icon=":material/person_add:",
            shortcut="control+enter",
            width="stretch",
            type="primary"
        ):

            success, message = register_teacher(
                teacher_username,
                teacher_name,
                teacher_pass,
                teacher_pass_confirm
            )

            if success:

                st.success(message)

                import time

                time.sleep(1)

                st.session_state.teacher_login_type = "login"

                st.rerun()

            else:

                st.error(message)

    with btncol2:

        if st.button(
            "Login Instead",
            type="tertiary",
            icon=":material/login:",
            width="stretch"
        ):

            st.session_state.teacher_login_type = "login"

            st.rerun()

    footer_dashboard()


# =============================================================
# PRESYNTA TEACHER UI
# =============================================================

def _teacher_ui_styles():

    st.html(
        """<style>

        /* =====================================================
           TEACHER DASHBOARD INTRO
           ===================================================== */

        .presynta-teacher-welcome {
            display: flex;
            flex-direction: column;
            align-items: flex-end;
            gap: 3px;
            margin-bottom: 8px;
        }


        .presynta-teacher-welcome span {
            color: #7A8494;
            font-family: 'Manrope', sans-serif;
            font-size: 0.6rem;
            font-weight: 800;
            letter-spacing: 0.1em;
        }


        .presynta-teacher-welcome strong {
            color: #0B1220;
            font-family: 'Space Grotesk', sans-serif;
            font-size: 1rem;
            font-weight: 700;
        }


        .presynta-teacher-intro {
            margin: 1rem 0 1.5rem;
        }


        .presynta-teacher-label,
        .presynta-section-label {
            display: inline-block;

            color: #12845A;
            background: #E8F5EF;

            border: 1px solid #CDE8DB;

            border-radius: 999px;

            padding: 5px 10px;

            font-family: 'Manrope', sans-serif;
            font-size: 0.62rem;
            font-weight: 800;

            letter-spacing: 0.1em;
        }


        .presynta-teacher-intro h2,
        .presynta-section-heading h2 {
            margin-top: 0.75rem !important;
            margin-bottom: 0.4rem !important;

            color: #0B1220 !important;

            font-family: 'Space Grotesk', sans-serif !important;
            font-size: 2rem !important;
            font-weight: 700 !important;
        }


        .presynta-teacher-intro p,
        .presynta-section-heading p {
            max-width: 700px;

            margin: 0;

            color: #697586;

            font-family: 'Manrope', sans-serif;

            font-size: 0.9rem;

            line-height: 1.7;
        }


        /* =====================================================
           SECTION HEADINGS
           ===================================================== */

        .presynta-section-heading {
            margin: 0 0 1.4rem;
        }


        .presynta-content-heading {
            display: flex;
            align-items: baseline;
            justify-content: space-between;
            gap: 1rem;

            margin-bottom: 1rem;
        }


        .presynta-content-heading h3 {
            margin: 0;

            color: #0B1220;

            font-family: 'Space Grotesk', sans-serif;

            font-size: 1.3rem;
            font-weight: 700;
        }


        .presynta-content-heading span {
            color: #7A8494;

            font-family: 'Manrope', sans-serif;

            font-size: 0.72rem;
        }


        /* =====================================================
           SUBJECT HELPER
           ===================================================== */

        .presynta-subject-helper {
            display: flex;
            flex-direction: column;
            gap: 3px;
        }


        .presynta-subject-helper strong {
            color: #0B1220;

            font-family: 'Space Grotesk', sans-serif;

            font-size: 1.1rem;
        }


        .presynta-subject-helper span {
            color: #7A8494;

            font-family: 'Manrope', sans-serif;

            font-size: 0.75rem;
        }


        /* =====================================================
           EMPTY STATES
           ===================================================== */

        .presynta-empty-state {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;

            text-align: center;

            background: #FFFFFF;

            border: 1px dashed #C9D5CE;

            border-radius: 1.25rem;

            padding: 2.5rem 1.5rem;

            margin: 1rem 0;
        }


        .presynta-empty-icon {
            width: 46px;
            height: 46px;

            display: flex;
            align-items: center;
            justify-content: center;

            border-radius: 50%;

            background: #E8F5EF;

            color: #19A974;

            font-family: 'Space Grotesk', sans-serif;

            font-size: 1.5rem;
            font-weight: 700;
        }


        .presynta-empty-state h3 {
            margin: 0.8rem 0 0.3rem;

            color: #0B1220;

            font-family: 'Space Grotesk', sans-serif;

            font-size: 1.15rem;
        }


        .presynta-empty-state p {
            max-width: 420px;

            margin: 0;

            color: #7A8494;

            font-family: 'Manrope', sans-serif;

            font-size: 0.8rem;

            line-height: 1.6;
        }


        /* =====================================================
           RECORD SUMMARY
           ===================================================== */

        .presynta-record-summary {
            display: flex;
            gap: 10px;

            margin: 0 0 1rem;
        }


        .presynta-record-summary > div {
            min-width: 145px;

            display: flex;
            flex-direction: column;
            gap: 3px;

            background: #FFFFFF;

            border: 1px solid #DCE4DF;

            border-radius: 0.9rem;

            padding: 11px 14px;
        }


        .presynta-record-summary span {
            color: #7A8494;

            font-family: 'Manrope', sans-serif;

            font-size: 0.58rem;
            font-weight: 800;

            letter-spacing: 0.08em;
        }


        .presynta-record-summary strong {
            color: #0B1220;

            font-family: 'Space Grotesk', sans-serif;

            font-size: 1.1rem;
        }


        /* =====================================================
           CAMERA / PHOTO AREA
           ===================================================== */

        div[data-testid="stImage"] {
            border-radius: 0.8rem;
            overflow: hidden;
        }


        /* =====================================================
           RESPONSIVE
           ===================================================== */

        @media (max-width: 768px) {

            .presynta-teacher-welcome {
                align-items: center;
                margin-bottom: 15px;
            }


            .presynta-teacher-intro h2,
            .presynta-section-heading h2 {
                font-size: 1.65rem !important;
            }


            .presynta-teacher-intro p,
            .presynta-section-heading p {
                font-size: 0.84rem;
            }


            .presynta-content-heading {
                flex-direction: column;
                gap: 3px;
            }


            .presynta-record-summary > div {
                min-width: 0;
                flex: 1;
            }

        }


        @media (max-width: 480px) {

            .presynta-teacher-intro h2,
            .presynta-section-heading h2 {
                font-size: 1.45rem !important;
            }


            .presynta-teacher-intro p,
            .presynta-section-heading p {
                font-size: 0.8rem;
            }


            .presynta-record-summary {
                gap: 6px;
            }


            .presynta-record-summary > div {
                padding: 9px 10px;
            }


            .presynta-record-summary span {
                font-size: 0.5rem;
            }


            .presynta-record-summary strong {
                font-size: 0.95rem;
            }


            .presynta-empty-state {
                padding: 2rem 1rem;
            }

        }

        </style>
        """
    )


# Apply teacher-specific styles
_teacher_ui_styles()