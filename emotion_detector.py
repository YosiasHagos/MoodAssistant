import os
import cv2
import base64
import time

from dotenv import load_dotenv
from openai import OpenAI


MODEL_NAME = "gpt-4o-mini"   
N_FRAMES   = 1               
FRAME_DELAY = 0.3           


load_dotenv()
client = OpenAI()


def encode_image(image) -> str:
    """
    Convert a CV2 image (numpy array) to a base64-encoded JPG string.
    """
    success, buffer = cv2.imencode(".jpg", image)
    if not success:
        raise RuntimeError("Failed to encode image to JPEG.")
    return base64.b64encode(buffer).decode("utf-8")


def _capture_frames(n_frames: int = 1):
    """
    Capture 1 or more frames from the default webcam.
    Returns a list of frames (BGR numpy arrays).
    """
    frames = []
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("[ERROR] Webcam not accessible.")
        return []

    try:
        for i in range(n_frames):
            ret, frame = cap.read()
            if not ret:
                print(f"[ERROR] Failed to capture frame {i+1}.")
                break
            frames.append(frame)
            if i < n_frames - 1:
                time.sleep(FRAME_DELAY)
    finally:
        cap.release()

    return frames


def detect_mood() -> str | None:
    """
    Capture frame(s), send to GPT-4o-mini with a detailed
    prompt using your custom rules, and return one of:
        'focused', 'happy', 'sad', 'stressed'
    Returns None if something fails.
    """

    frames = _capture_frames(N_FRAMES)
    if not frames:
        return None

    images_b64 = [encode_image(f) for f in frames]

    content_blocks = [
        {
            "type": "text",
            "text": (
                "You are a specialised mood classifier for a productivity assistant. "
                "You must classify the user into ONLY one of these moods: focused, happy, sad, stressed.\n\n"

                "STRICT RULES:\n"
                "FOCUSED:\n"
                "- User is looking at the computer monitor.\n"
                "- Face looks serious or concentrating.\n"
                "- User is typing on keyboard, using a mouse, or holding a pen.\n"
                "- A smiling or obviously happy face means the user is NOT focused.\n\n"

                "HAPPY:\n"
                "- User is looking at their phone.\n"
                "- User shows a happy or smiling expression.\n"
                "- User is NOT actively using keyboard or mouse.\n\n"

                "SAD:\n"
                "- Sad facial expression OR visible tears.\n"
                "- (Looking at phone + sad face) → sad.\n"
                "- (Looking at monitor + tears) → sad.\n"
                "- Neutral or serious working face alone does NOT count as sad.\n\n"

                "STRESSED:\n"
                "- Serious face between sad and angry (frustrated, tense, overwhelmed).\n"
                "- Can occur when looking at monitor OR phone.\n"
                "- Must not be smiling.\n\n"

                "CONTEXT RULES:\n"
                "- If the user is looking at the monitor, assume they are studying or working.\n"
                "- If the user is looking at their phone, assume personal time.\n"
                "- If no hand interaction (typing, mouse, pen) is visible, the user CANNOT be 'focused'.\n"
                "- The environment is the user's study desk: looking at the monitor means study mode.\n\n"

                "OUTPUT FORMAT:\n"
                "- Respond with exactly ONE word: focused, happy, sad, or stressed.\n"
                "- Do NOT output anything else.\n"
            )
        }
    ]

    for img_b64 in images_b64:
        content_blocks.append(
            {
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/jpeg;base64,{img_b64}"
                }
            }
        )

    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {
                    "role": "user",
                    "content": content_blocks,
                }
            ],
        )
    except Exception as e:
        print(f"[ERROR] OpenAI request failed: {e}")
        return None

    try:
        content = response.choices[0].message.content.strip().lower()
    except Exception as e:
        print(f"[ERROR] Unexpected response format: {e}")
        return None

    first_word = content.split()[0]

    allowed = {"focused", "happy", "sad", "stressed"}

    if first_word not in allowed:

        if "focus" in content:
            mood = "focused"
        elif "smile" in content or "happy" in content or "joy" in content:
            mood = "happy"
        elif "tear" in content or "cry" in content or "upset" in content or "sad" in content:
            mood = "sad"
        else:
            mood = "stressed"
    else:
        mood = first_word
    print(f"[EMOTION DETECTOR] Model raw: '{content}' → mood: {mood}")
    return mood
