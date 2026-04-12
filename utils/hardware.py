import board
import neopixel

# FORCE PI MODE: Skip all checks to ensure physical LEDs fire!
ON_PI = True

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
print("✅ Hardware: Raspberry Pi mode FORCE ENABLED.")

def update_physical_led(r, g, b):
    try:
        # Cast RGB values to integers
        pixels.fill((int(r), int(g), int(b)))
        pixels.show()
        print(f"✨ [Hardware] Physical NeoPixel -> RGB({int(r)}, {int(g)}, {int(b)})")
    except Exception as e:
        print(f"❌ [Hardware] Error updating NeoPixel: {e}")