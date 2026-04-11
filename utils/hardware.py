import sys

# --- Flexible Environment Check ---
try:
    import board
    import neopixel
    # Loose check: If these libraries are imported, assume we are on a Raspberry Pi.
    ON_PI = True
except (ImportError, RuntimeError):
    # If libraries are missing (e.g., on Mac/Windows), switch to simulation mode.
    ON_PI = False

if ON_PI:
    try:
        # --- Raspberry Pi Hardware Configuration ---
        pixel_pin = board.D18
        num_pixels = 16
        ORDER = neopixel.GRB
        pixels = neopixel.NeoPixel(
            pixel_pin, 
            num_pixels, 
            brightness=0.3, 
            auto_write=False, 
            pixel_order=ORDER
        )
        print("✅ Hardware: Raspberry Pi mode enabled (Loose check passed).")
    except Exception as e:
        # Fallback to simulation if initialization fails despite library presence.
        print(f"⚠️ Hardware: Board detected but failed to init LEDs ({e}). Switching to simulation.")
        ON_PI = False

else:
    # --- Development Environment Configuration (Mac/Windows) ---
    print("🖥️ Hardware: Running on Non-Pi environment. Simulation mode active.")

def update_physical_led(r, g, b):
    """
    Updates the LED state.
    Sends data to physical LEDs on Raspberry Pi, or logs to console on other platforms.
    """
    if ON_PI:
        try:
            # Cast RGB values to integers as required by NeoPixel
            pixels.fill((int(r), int(g), int(b)))
            pixels.show()
            print(f"✨ [Hardware] Physical NeoPixel -> RGB({int(r)}, {int(g)}, {int(b)})")
        except Exception as e:
            print(f"❌ [Hardware] Error updating NeoPixel: {e}")
    else:
        # Console output for debugging on Mac
        print(f"🖥️ [Simulated LED] Setting RGB to ({int(r)}, {int(g)}, {int(b)})")