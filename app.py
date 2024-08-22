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
        </style>
        """,
        unsafe_allow_html=True
    ) 

    st.title("Avensz.Ai Homework Assignment")
    st.write("Hello World!")
    st.write("This is the assignment Shaheer has given me!!")
    
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
                    # You can add more processing logic for the file here
                else:
                    st.success(f"URL '{url_input}' submitted successfully!")
                    # You can add more processing logic for the URL here

    return None

if __name__ == '__main__':
    main()