import time
import os
from dotenv import load_dotenv

from emotion_detector import detect_mood
from mood_logic import get_mood_settings
from lighting_control import LightController
from audio_control import AudioController


load_dotenv()



UPDATE_INTERVAL = 60  


AUDIO_VOLUME = 0.5 


def main():
    """Main control loop."""
    
    print("=" * 60)
    print("MOOD-BASED SMART ENVIRONMENT CONTROLLER")
    print("=" * 60)
    print()
    

    print("[INIT] Initializing controllers.")
    

    try:
        light_controller = LightController()
    except Exception as e:
        print(f"[ERROR] Failed to initialize light controller: {e}")
        print("[INFO] Continuing without light control.")
        light_controller = None
    

    try:
        audio_controller = AudioController(audio_folder="audio")
        audio_controller.set_volume(AUDIO_VOLUME)
    except Exception as e:
        print(f"[ERROR] Failed to initialize audio controller: {e}")
        print("[INFO] Continuing without audio control.")
        audio_controller = None
    
    print()
    print("[INIT] Initialization complete!")
    print(f"[INFO] Will check mood every {UPDATE_INTERVAL} seconds")
    print("[INFO] Press Ctrl+C to stop")
    print()
    
    last_mood = None
    
    try:
        while True:
            print("-" * 60)
            print(f"[{time.strftime('%H:%M:%S')}] Checking mood...")
            

            try:
                mood = detect_mood()
                
                if mood is None:
                    print("[ERROR] Failed to detect mood. Retrying next cycle.")
                    time.sleep(UPDATE_INTERVAL)
                    continue
                
                print(f"[MOOD] Detected: {mood.upper()}")
                

                if mood == last_mood:
                    print("[INFO] Mood unchanged, skipping update")
                    time.sleep(UPDATE_INTERVAL)
                    continue
                

                settings = get_mood_settings(mood)
                

                if light_controller:
                    success = light_controller.set_light(
                        settings["color"],
                        settings["brightness"]
                    )
                    if success is False:
                        print("[WARNING] Light update failed")
                else:
                    print("[INFO] Light controller not available")
                

                if audio_controller:
                    if settings["sound"] != "none":
                        audio_controller.play_sound(settings["sound"])
                    else:
                        audio_controller.stop_audio()
                else:
                    print("[INFO] Audio controller not available")
                

                last_mood = mood
                print(f"[SUCCESS] Environment updated for '{mood}' mood")
                
            except Exception as e:
                print(f"[ERROR] Error in mood detection/update cycle: {e}")
            

            print(f"[INFO] Next check in {UPDATE_INTERVAL} seconds.")
            print()
            time.sleep(UPDATE_INTERVAL)
            
    except KeyboardInterrupt:
        print()
        print("=" * 60)
        print("[SHUTDOWN] Stopping system.")
        

        if audio_controller:
            audio_controller.cleanup()
        
        print("[SHUTDOWN] System stopped. Goodbye!")
        print("=" * 60)


if __name__ == "__main__":

    if not os.getenv("OPENAI_API_KEY"):
        print("[ERROR] OPENAI_API_KEY environment variable not set!")
        print("[INFO] Make sure your .env file contains OPENAI_API_KEY=...")
        exit(1)
    
    main()
