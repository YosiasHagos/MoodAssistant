# mood_logic.py

def get_mood_settings(mood):
    mood = mood.lower()

    mood_map = {
        "happy": {
            "color": "#FFA500",     # warm orange
            "brightness": 90,
            "sound": "happy"
        },
        "sad": {
            "color": "#FFD700",     # warm yellow
            "brightness": 50,
            "sound": "sad"
        },
        "stressed": {
            "color": "#4169E1",     # royal blue
            "brightness": 60,
            "sound": "stressed"
        },
        "neutral": {
            "color": "#FFFFFF",     # pure white
            "brightness": 70,
            "sound": "none"
        },
        "focused": {
            "color": "#F0F8FF",     # alice blue
            "brightness": 85,
            "sound": "focused"
        }
    }

    settings = mood_map.get(mood, mood_map["neutral"])

    print(
        f"[MOOD LOGIC] Mood '{mood}' → "
        f"Color {settings['color']} | Brightness {settings['brightness']} | "
        f"Sound '{settings['sound']}'"
    )

    return settings
