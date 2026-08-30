import streamlit as st

from PIL import Image


@st.dialog("Add Attendance Photos")
def add_photos_dialog():

    st.html(
        """<div class="presynta-photo-header">

            <div class="presynta-photo-icon">
                ◉
            </div>

            <div>
                <h3>Add classroom photos</h3>
                <p>
                    Capture or upload classroom images for
                    AI-powered attendance recognition.
                </p>
            </div>

        </div>

        <div class="presynta-photo-tip">
            <span>TIP</span>
            Make sure students' faces are clearly visible
            for better recognition.
        </div>

        <style>

            .presynta-photo-header {
                display: flex;
                align-items: center;
                gap: 12px;

                margin-bottom: 1rem;
            }


            .presynta-photo-icon {
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

                font-size: 1.25rem;
                font-weight: 700;
            }


            .presynta-photo-header h3 {
                margin: 0;

                color: #0B1220;

                font-family: 'Space Grotesk', sans-serif;

                font-size: 1.2rem;
                font-weight: 700;
            }


            .presynta-photo-header p {
                margin: 3px 0 0;

                color: #7A8494;

                font-family: 'Manrope', sans-serif;

                font-size: 0.74rem;

                line-height: 1.5;
            }


            .presynta-photo-tip {
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


            .presynta-photo-tip span {
                flex-shrink: 0;

                color: #19A974;

                font-size: 0.58rem;

                font-weight: 800;

                letter-spacing: 0.08em;
            }


            .presynta-photo-tabs {
                margin-bottom: 0.8rem;
            }


            @media (max-width: 480px) {

                .presynta-photo-header {
                    gap: 9px;
                }


                .presynta-photo-icon {
                    width: 36px;
                    height: 36px;

                    font-size: 1rem;
                }


                .presynta-photo-header h3 {
                    font-size: 1.05rem;
                }


                .presynta-photo-header p {
                    font-size: 0.68rem;
                }


                .presynta-photo-tip {
                    font-size: 0.65rem;
                }

            }

        </style>
        """
    )

    if "photo_tab" not in st.session_state:
        st.session_state.photo_tab = "camera"

    # =========================================================
    # PHOTO SOURCE TABS
    # =========================================================

    t1, t2 = st.columns(
        2,
        gap="small"
    )

    with t1:

        type_camera = (
            "primary"
            if st.session_state.photo_tab == "camera"
            else "tertiary"
        )

        if st.button(
            "Camera",
            type=type_camera,
            width="stretch",
            icon=":material/photo_camera:"
        ):

            st.session_state.photo_tab = "camera"
            st.rerun()

    with t2:

        type_upload = (
            "primary"
            if st.session_state.photo_tab == "upload"
            else "tertiary"
        )

        if st.button(
            "Upload",
            type=type_upload,
            width="stretch",
            icon=":material/upload:"
        ):

            st.session_state.photo_tab = "upload"
            st.rerun()

    # =========================================================
    # CAMERA
    # =========================================================

    if st.session_state.photo_tab == "camera":

        cam_photo = st.camera_input(
            "Take a classroom snapshot",
            key="dialog_cam"
        )

        if cam_photo:

            st.session_state.attendance_images.append(
                Image.open(cam_photo)
            )

            st.toast(
                "Photo captured successfully",
                icon="📸"
            )

            st.rerun()

    # =========================================================
    # UPLOAD
    # =========================================================

    if st.session_state.photo_tab == "upload":

        uploaded_files = st.file_uploader(
            "Choose classroom image files",
            type=[
                "jpg",
                "png",
                "jpeg"
            ],
            accept_multiple_files=True,
            key="dialog_upload"
        )

        if uploaded_files:

            for f in uploaded_files:

                st.session_state.attendance_images.append(
                    Image.open(f)
                )

            st.toast(
                "Photos uploaded successfully",
                icon="📷"
            )

            st.rerun()

    st.divider()

    # =========================================================
    # DONE
    # =========================================================

    if st.button(
        "Done",
        type="primary",
        width="stretch",
        icon=":material/check:"
    ):

        st.rerun()