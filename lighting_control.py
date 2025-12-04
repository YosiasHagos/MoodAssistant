# lighting_control.py
# Control Tapo L530E bulb using the `tapo` library

import os
import asyncio
import colorsys
from dotenv import load_dotenv
from tapo import ApiClient  # pip install tapo

load_dotenv()  # load TAPO_* from .env


class LightController:
    def __init__(self):
        self.ip = os.getenv("TAPO_IP")
        self.email = os.getenv("TAPO_EMAIL")
        self.password = os.getenv("TAPO_PASSWORD")

        if not self.ip or not self.email or not self.password:
            raise ValueError(
                "TAPO_IP, TAPO_EMAIL and TAPO_PASSWORD must be set in your .env file."
            )

        print(f"[LIGHT] LightController using Tapo at {self.ip}")

    async def _apply_light_async(self, hex_color: str, brightness: int):
        """
        Async part: connect to the bulb and apply settings.
        - Turn bulb ON
        - Set brightness
        - Set colour using hue & saturation from the hex code
        """
        client = ApiClient(self.email, self.password)
        device = await client.l530(self.ip)

        # Ensure the bulb is ON
        await device.on()

        # Clamp brightness to 1–100
        brightness = max(1, min(100, int(brightness)))
        await device.set_brightness(brightness)

        # --- Set colour based on hex_color ---
        try:
            # Clean and parse hex colour
            hex_str = hex_color.lstrip("#")
            if len(hex_str) != 6:
                raise ValueError(f"Invalid hex colour: {hex_color}")

            r = int(hex_str[0:2], 16) / 255.0
            g = int(hex_str[2:4], 16) / 255.0
            b = int(hex_str[4:6], 16) / 255.0

            # Convert RGB → HSV, then to Tapo ranges
            h, s, v = colorsys.rgb_to_hsv(r, g, b)
            hue = int(h * 360)       # 0–360
            sat = int(s * 100)       # 0–100

            # Use the hue/saturation API (Python tapo mirrors the Rust API)
            await device.set_hue_saturation(hue, sat)

            print(
                f"[LIGHT] Applied color {hex_color} "
                f"(hue={hue}, sat={sat}) brightness={brightness}%"
            )
        except Exception as e:
            # If colour fails for any reason, brightness still works
            print(f"[LIGHT WARNING] Failed to set colour for {hex_color}: {e}")

    def set_light(self, hex_color: str, brightness: int) -> bool:
        """
        Public sync method used by main.py.
        Wraps the async function with asyncio.run().
        Returns True on success, False on failure.
        """
        try:
            asyncio.run(self._apply_light_async(hex_color, brightness))
            return True
        except Exception as e:
            print(f"[LIGHT ERROR] Failed to set light via tapo: {e}")
            return False
