# MoodAssistant 

A mood-adaptive study assistant that uses a webcam, the OpenAI API and a Tapo L530E smart bulb to detect whether I'm focused, happy, sad or stressed. It automatically adjusts lighting and audio using custom mood logic to reduce decision fatigue and strengthen state-dependent learning during revision.

---

##  What it does

- Captures a frame from the webcam at regular intervals  
- Sends the image to an OpenAI vision model (e.g. `gpt-4o-mini`)  
- Interprets:
  - whether I'm looking at my monitor or my phone  
  - what my facial expression looks like  
  - whether I'm typing / using the mouse / holding a pen  
- Maps that to one of four moods using **hard rules**:
  - `focused`
  - `happy`
  - `sad`
  - `stressed`
- Updates the environment:
  - changes Tapo smart bulb colour + brightness  
  - plays mood-appropriate audio (rain, calm, happy, etc.)

The goal is not “flashy RGB”, but a calm, repeatable study environment that supports focus and emotional regulation in a noisy household.

---

##  Mood logic (custom rules)

Generic emotion detection wasn’t accurate enough, so the system uses explicit rules that define what each mood means **for me**:

**FOCUSED**

- Looking at the monitor  
- Serious / concentrating face (not smiling)  
- Typing on the keyboard, using the mouse, or holding a pen  
- No tears or obvious sadness  

**HAPPY**

- Looking at my phone  
- Smiling or clearly positive expression  
- Not interacting with keyboard or mouse  

**SAD**

- Sad facial expression or tears  
- Either:
  - looking at phone with a sad face, or  
  - looking at the monitor with visible tears  
- Does **not** trigger when I’m simply serious and working  

**STRESSED**

- Face looks between sad and angry (frustrated, tense, overwhelmed)  
- Can occur when looking at monitor **or** phone  
- Must not be smiling  

The OpenAI vision model is used purely to **interpret the scene** (eyes, hands, expression). The actual decision logic is rule-based in Python.

---

## Tech stack

- **Python 3.11**
- **OpenCV** – capture frames from webcam  
- **OpenAI API** – image input to models like `gpt-4o-mini` / `gpt-4o`  
- **pygame** – audio playback  
- **pytapo / PyP100** – control TP-Link Tapo L530E smart bulb over Wi-Fi  
- **dotenv** – load environment variables from `.env`

---

## Project structure

```text
MoodAssistant/
├── main.py               # Main control loop (scheduler + orchestration)
├── emotion_detector.py   # Webcam capture + OpenAI vision call
├── mood_logic.py         # Maps moods → colour, brightness, sound
├── lighting_control.py   # Wrapper around Tapo API (set colour/brightness)
├── audio_control.py      # Audio playback (pygame)
├── lighting_debug.py     # Standalone test script for the bulb (optional)
├── audio/
│   ├── happy.mp3
│   ├── rain.mp3
│   ├── calm.mp3
│   └── stressed.mp3      # (or whatever filenames you use)
└── .env.example          # Example environment variables (no real secrets)
