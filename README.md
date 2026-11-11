# Isi Media — Public Demo Deployment

A browser-based multimedia viewer and basic image editor built with Python, Streamlit, Pillow and OpenCV.

## Features
- Upload and preview PNG, JPG/JPEG, BMP and WEBP images.
- Upload and preview MP4, MOV, AVI and MKV videos.
- Display image dimensions and file size.
- Adjust image brightness and contrast.
- Apply black-and-white conversion or Gaussian blur.
- Download edited images as PNG.
- Display video resolution, frame rate and calculated duration.
- Extract and download a video's first frame as PNG.

## Deploy free with Streamlit Community Cloud

1. Create or sign in to a GitHub account at https://github.com.
2. Create a **new public repository** named `isi-media-demo`.
3. Extract this ZIP file on your computer or phone.
4. Upload the contents of this folder to the root of that GitHub repository. Make sure `app.py` and `requirements.txt` are at the repository root, and include the `.streamlit` folder.
5. Visit https://share.streamlit.io/ and sign in with GitHub.
6. Choose **Create app** → **Yup, I have an app**.
7. Select your repository and branch (`main`), and set the main file path to `app.py`.
8. In Advanced settings, choose Python 3.12 if the option is available, then deploy.
9. Wait for the build to finish. Streamlit will provide a shareable address ending in `streamlit.app`.
10. Open the public link in a private/incognito browser window and test image upload, image edits, downloads, video preview, video properties and first-frame download.

Official instructions: https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/deploy

## Important
- This ZIP prepares the app for deployment; it does not itself publish the app or create a live URL.
- A GitHub account and an authenticated Streamlit Community Cloud session are required to publish it.
- The repository is public in these instructions, so the source code will be visible. Do not upload private files, API keys, passwords or confidential media.
- The app accepts uploads up to 100 MB. Free hosting resources are limited; very large videos may be slow or fail.
- The source was syntax-checked during packaging, but the hosted app still needs end-to-end browser testing after deployment.
- Uploaded media should be treated as untrusted. Avoid using this public demo for confidential or sensitive files.

## Run locally

```bash
python -m venv .venv
# Windows: .venv\\Scripts\\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

The local app normally opens at http://localhost:8501.
