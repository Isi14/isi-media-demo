import io
import tempfile
from pathlib import Path

import cv2
import streamlit as st
from PIL import Image, ImageEnhance, ImageFilter, UnidentifiedImageError

st.set_page_config(page_title="Isi Media", page_icon="🎬", layout="wide")

st.title("🎬 Isi Media")
st.subheader("A Simple Multimedia Viewer and Editor")
st.write(
    "Upload an image or video to preview it, inspect basic media information, "
    "and try simple image-editing tools."
)
st.caption("Supported images: PNG, JPG/JPEG, BMP, WEBP · Supported videos: MP4, MOV, AVI, MKV")

media = st.file_uploader(
    "Choose an image or video",
    type=["png", "jpg", "jpeg", "bmp", "webp", "mp4", "mov", "avi", "mkv"],
    help="Maximum upload size: 100 MB.",
)

if media is None:
    st.info("Upload an image or video to get started.")
    st.markdown(
        """
        **What you can do with Isi Media**
        - View images and videos.
        - See basic media information.
        - Adjust image brightness and contrast.
        - Convert an image to black and white.
        - Apply a simple blur effect.
        - Download your edited image or a video's first frame.
        """
    )
    st.stop()

media_bytes = media.getvalue()
extension = Path(media.name).suffix.lower()
image_types = {".png", ".jpg", ".jpeg", ".bmp", ".webp"}
video_types = {".mp4", ".mov", ".avi", ".mkv"}

st.success(f"Uploaded: {media.name}")

if extension in image_types:
    try:
        image = Image.open(io.BytesIO(media_bytes)).convert("RGB")
        width, height = image.size

        left, right = st.columns(2)
        with left:
            st.subheader("Original image")
            st.image(image, use_container_width=True)

        st.subheader("Image information")
        info1, info2, info3 = st.columns(3)
        info1.metric("Width", f"{width} px")
        info2.metric("Height", f"{height} px")
        info3.metric("File size", f"{len(media_bytes) / 1024:.1f} KB")

        st.subheader("Edit your image")
        brightness = st.slider("Brightness", 0.5, 2.0, 1.0, 0.1)
        contrast = st.slider("Contrast", 0.5, 2.0, 1.0, 0.1)
        effect = st.selectbox("Choose an effect", ["Original", "Black and white", "Blur"])

        edited = ImageEnhance.Brightness(image).enhance(brightness)
        edited = ImageEnhance.Contrast(edited).enhance(contrast)
        if effect == "Black and white":
            edited = edited.convert("L").convert("RGB")
        elif effect == "Blur":
            edited = edited.filter(ImageFilter.GaussianBlur(radius=2))

        with right:
            st.subheader("Edited image")
            st.image(edited, use_container_width=True)

        output = io.BytesIO()
        edited.save(output, format="PNG")
        st.download_button(
            "Download edited image",
            data=output.getvalue(),
            file_name="isi_media_edited.png",
            mime="image/png",
        )
    except (UnidentifiedImageError, OSError, ValueError) as error:
        st.error(f"The uploaded file could not be read as a valid image: {error}")

elif extension in video_types:
    st.subheader("Video preview")
    st.video(media_bytes)
    st.subheader("Video information")
    st.write(f"**File name:** {media.name}")
    st.write(f"**File size:** {len(media_bytes) / (1024 * 1024):.2f} MB")

    if st.button("Show video properties and capture a frame"):
        temp_path = None
        capture = None
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix=extension) as temp:
                temp.write(media_bytes)
                temp_path = temp.name

            capture = cv2.VideoCapture(temp_path)
            if not capture.isOpened():
                st.error("The video could not be opened. Try a standard MP4 video.")
            else:
                fps = capture.get(cv2.CAP_PROP_FPS) or 0
                frames = int(capture.get(cv2.CAP_PROP_FRAME_COUNT) or 0)
                width = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH) or 0)
                height = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT) or 0)
                duration = frames / fps if fps else 0

                a, b, c = st.columns(3)
                a.metric("Resolution", f"{width} × {height}")
                b.metric("Frame rate", f"{fps:.1f} FPS")
                c.metric("Duration", f"{duration:.1f} seconds")

                success, frame = capture.read()
                if success:
                    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    st.image(frame, caption="First frame of the video", use_container_width=True)
                    frame_image = Image.fromarray(frame)
                    frame_output = io.BytesIO()
                    frame_image.save(frame_output, format="PNG")
                    st.download_button(
                        "Download first frame",
                        data=frame_output.getvalue(),
                        file_name="isi_media_video_frame.png",
                        mime="image/png",
                    )
                else:
                    st.warning("The video opened, but its first frame could not be decoded.")
        except Exception as error:
            st.error(f"Something went wrong while reading the video: {error}")
        finally:
            if capture is not None:
                capture.release()
            if temp_path and Path(temp_path).exists():
                Path(temp_path).unlink()
else:
    st.error("This file type is not supported.")

st.divider()
st.caption("Isi Media — built with Python, Streamlit, Pillow and OpenCV.")
st.caption("Privacy note: files are processed for your active app session. Do not upload confidential or sensitive media to a public demo.")
