import streamlit as st
import requests
from dotenv import load_dotenv
import os
import time

# Load variables from .env file
load_dotenv()

avatarlist = {
    "Male": "https://www.thesun.co.uk/wp-content/uploads/2021/10/2394f46a-c64f-4019-80bd-445dacda2880.jpg?w=670",
    "Female": "https://create-images-results.d-id.com/DefaultPresenters/Noelle_f/image.jpeg"
}


# Function to generate video based on the prompt and avatar selection
def generate_video(prompt, avatar_url, gender):
    url = "https://api.d-id.com/talks"
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "Authorization": os.getenv("API_KEY_DID")
    }
    if gender == "Female":
        payload = {
            "script": {
                "type": "text",
                "subtitles": "false",
                "provider": {
                    "type": "microsoft",
                    "voice_id": "en-US-JennyNeural"
                },
                "ssml": "false",
                "input": prompt
            },
            "config": {
                "fluent": "false",
                "pad_audio": "0.0"
            },
            "source_url": avatar_url
        }

    if gender == "Male":
        payload = {
            "script": {
                "type": "text",
                "subtitles": "false",
                "provider": {
                    "type": "microsoft",
                    "voice_id": "en-US-BrandonNeural"
                },
                "ssml": "false",
                "input": prompt
            },
            "config": {
                "fluent": "false",
                "pad_audio": "0.0"
            },
            "source_url": avatar_url
        }

    try:
        response = requests.post(url, json=payload, headers=headers)

        print("url", url)
        print("payload", payload)
        print("headers", headers)

        if response.status_code == 201:
            print(response.text)
            res = response.json()
            id = res["id"]
            status = "created"
            while status == "created":
                getresponse = requests.get(f"{url}/{id}", headers=headers)
                print(getresponse)
                if getresponse.status_code == 200:
                    status = res["status"]
                    res = getresponse.json()
                    print(res)
                    if res["status"] == "done":
                        video_url = res["result_url"]
                    else:
                        time.sleep(10)
                else:
                    status = "error"
                    video_url = "error"
        else:
            video_url = "error"
    except Exception as e:
        print(e)
        video_url = "error"

    return video_url


def main():
    st.set_page_config(page_title="Avatar Video Generator", page_icon=":movie_camera:")

    st.title("Generate Video")

    # Text prompt input
    prompt = st.text_area("Enter Text Prompt", "Biology is the scientific study of life. It is a natural science with a broad scope but has several unifying themes that tie it together as a single, coherent field. For instance, all organisms are made up of cells that process hereditary information encoded in genes, which can be transmitted to future generations.")

    # Dropdown box for avatar selection
    # avatar_options = ["Male", "Female"]
    # avatar_selection = st.selectbox("Choose Avatar", avatar_options)
    avatar_url = avatarlist["Female"]

    # Generate video button
    if st.button("Generate Video"):
        st.text("Generating video...")
        try:
            video_url = generate_video(prompt, avatar_url, "Female")  # Call your video generation function here
            print("----", video_url)
            if video_url != "error":
                st.text("Video generated!")

                # Placeholder for displaying generated video
                st.subheader("Generated Video")
                st.video(video_url)  # Replace with the actual path
            else:
                st.text("Sorry... Try again")
        except Exception as e:
            print(e)
            st.text("Sorry... Try again")


if __name__ == "__main__":
    main()
