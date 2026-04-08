import sys

# Environment Check: Detect if running on an actual Raspberry Pi
try:
    import board
    import neopixel
    # Check for hardware-specific attribute to ensure it's not a dummy module
    if not hasattr(board, 'D18'):
        raise ImportError
    ON_PI = True
except (ImportError, RuntimeError, AttributeError):
    ON_PI = False

if ON_PI:
    # --- Raspberry Pi Hardware Configuration ---
    pixel_pin = board.D18
    num_pixels = 16
    ORDER = neopixel.GRB
    pixels = neopixel.NeoPixel(
        pixel_pin, 
        num_pixels, 
        brightness=1.0, 
        auto_write=False, 
        pixel_order=ORDER
    )
    print("✅ Hardware: Raspberry Pi detected. LED output enabled.")
else:
    # --- Development Environment Configuration (Mac/Windows) ---
    print("⚠️ Hardware: Running on Non-Pi environment. LED output will be simulated in console.")

def update_physical_led(r, g, b):
    """
    Updates the LED state.
    Sends data to physical LEDs on Raspberry Pi, or logs to console on other platforms.
    """
    if ON_PI:
        try:
            pixels.fill((r, g, b))
            pixels.show()
            print(f"✨ [Hardware] Physical NeoPixel -> RGB({r}, {g}, {b})")
        except Exception as e:
            print(f"❌ [Hardware] Error updating NeoPixel: {e}")
    else:
        # Simulate LED output in terminal for development on Mac
        print(f"🖥️ [Simulated LED] Setting RGB to ({r}, {g}, {b})")