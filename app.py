import io
import cv2
import time
import base64
import tempfile
from PIL import Image
import streamlit as st

def main():

    # Custom CSS to style placeholder text
    st.markdown(
        """
        <style>
        input::placeholder {
            color: grey;
            opacity: 0.6; 
        }
        .stButton { 
            display: flex;
            justify-content: center;
        }
        .centered-image {
            display: block;
            margin-left: auto;
            margin-right: auto;
            width: 50%; 
        }
        </style>
        """,
        unsafe_allow_html=True
    ) 

    st.title("Avensz.Ai Homework Assignment")
    st.write("Hello World!")
    
    with st.form("video-upload"):
        st.write("Upload a file or enter a URL:")
        uploaded_file = st.file_uploader("Choose a video to upload! 🎞️", type=["mp4", "webm", "mov", "avi", "wmv"])
        url_input = st.text_input("Copy & Paste the URL of the video you wish to upload 👇", placeholder="https://www.youtube.com/shorts/1rx8k6kdRRg")
        submit_button = st.form_submit_button(label='Submit')

        if submit_button:
            if uploaded_file and url_input:
                st.error("Please provide either a file or a URL, not both.")
            elif not uploaded_file and not url_input:
                st.error("Please provide either a file or a URL.")
            else:
                if uploaded_file:
                    st.success(f"File '{uploaded_file.name}' uploaded successfully!")
                    video_processor_file(uploaded_file)
                else:
                    st.success(f"URL '{url_input}' submitted successfully!")
                    # You can add more processing logic for the URL here

    return None

def video_processor_file(video_file):
    
    tfile = tempfile.NamedTemporaryFile(delete=False)
    tfile.write(video_file.read())

    # Step 3: Capture a frame from the video to use as a thumbnail
    vidcap = cv2.VideoCapture(tfile.name)
    success, image = vidcap.read()
    
    if success:
        # Convert the captured frame to an image that Streamlit can display
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        pil_image = Image.fromarray(image)
        
        # Convert image to base64 for embedding
        buffered = io.BytesIO()
        pil_image.save(buffered, format="PNG")
        img_base64 = base64.b64encode(buffered.getvalue()).decode()

        # HTML for displaying the thumbnail with custom styling
        image_html = f"""
        <div>
            <img src="data:image/png;base64,{img_base64}" class="centered-image" alt="Video Thumbnail"/>
        </div>
        """
        st.markdown(image_html, unsafe_allow_html=True)

    # Step 4: Simulate a video processing task with a progress bar
    st.info("Processing video...")
    progress_bar = st.progress(0)

    for percent_complete in range(100):
        time.sleep(0.05)  # Simulate some processing time
        progress_bar.progress(percent_complete + 1)

    with open(tfile.name, "rb") as video_file:
        video_bytes = video_file.read()
        video_base64 = base64.b64encode(video_bytes).decode()

    # Step 4: Embed the video using HTML and base64
    video_html = f"""
    <div style="display: flex; justify-content: center;">
        <video width="500" controls>
            <source src="data:video/mp4;base64,{video_base64}" type="video/mp4">
            Your browser does not support the video tag.
        </video>
    </div>
    """
    st.markdown(video_html, unsafe_allow_html=True)

    return None

def video_processor_link(video_link):
    
    return None

if __name__ == '__main__':
    
    main()
    