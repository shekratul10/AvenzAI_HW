import time
import requests
import streamlit as st
from supabase import create_client, Client


def upload_to_supabase(video_file, audio_file):
    
    SUPABASE_URL = "supabase_url"
    SUPABASE_KEY = "supabase_api_key"

    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
    
    # Upload video file to Supabase storage
    # video_upload = supabase.storage.from_('test').upload(video_file.name, video_file.read(),file_options={"content-type": video_file.type})
    video_file.seek(0)
    try:
        video_upload = supabase.storage.from_('test').upload(video_file.name, video_file.read(), file_options={"content-type": video_file.type})
    except Exception as e:
        st.error(f"Error uploading video: {e}")
        video_upload = None
        
    audio_upload = supabase.storage.from_('test').upload(audio_file.name, audio_file.read(),file_options={"content-type": audio_file.type})
    
    if video_upload.status_code == 200 and audio_upload.status_code == 200:
        # Get public URL of uploaded files
        video_url = supabase.storage.from_('test').get_public_url(video_file.name)
        audio_url = supabase.storage.from_('test').get_public_url(audio_file.name)
        
    else:
        st.error("Error uploading files to Supabase.")
    
    return video_url, audio_url
    

def post_lipsync(video_url, audio_url):
    url = "https://api.synclabs.so/lipsync"
    

    payload = {
        "videoUrl": f"{video_url}",
        "audioUrl": f"{audio_url}",
        "model": "wav2lip++",
        "synergize": True
    }
    headers = {
        "x-api-key": "synclabs_api_key",
        "Content-Type": "application/json"
    }

    response = requests.request("POST", url, json=payload, headers=headers)

    print(response.text)
    
    if response.status_code == 201:
        st.success("Lip-synced video uploaded successfully!")
        time.sleep(5)
        id = response.json().get("id")
        result_url = get_lipsync(id)
        return result_url
    else:
        st.error("Failed to generate lip-synced video.")
        st.error(response.status_code)

def get_lipsync(id):
    url = f"https://api.synclabs.so/lipsync/{id}"
    headers = {"x-api-key": "synclabs_api_key"}

    response = requests.request("GET", url, headers=headers)
    
    while True:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            status = response.json().get("status")
            if status == "COMPLETED":
                result_url = response.json().get("videoUrl")
                print("Lip-synced video generated successfully!")
                return result_url
            else:
                # Status is still processing, so wait and then poll again
                st.info(f"Current status: {status}. Waiting for completion...")
                time.sleep(5)  # Wait for 5 seconds before polling again
        else:
            st.error(f"Error retrieving lip-synced video status: {response.text}")
            return None
        