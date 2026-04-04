import os
import sys

try:
    from PIL import Image
except ImportError:
    print("Pillow is required. Install it with: pip install Pillow")
    sys.exit(1)

source_icon = os.path.join(os.path.dirname(os.path.abspath(__file__)), "res", "icon.png")
flutter_android_res = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                    "flutter", "android", "app", "src", "main", "res")

if not os.path.exists(source_icon):
    print(f"Source icon not found at {source_icon}")
    sys.exit(1)

# Load source image and convert to RGBA (PNG needs alpha support)
img = Image.open(source_icon)
if img.mode != "RGBA":
    img = img.convert("RGBA")
print(f"Source icon loaded: {img.size[0]}x{img.size[1]}, format={img.format}, mode={img.mode}")

# First, save the source as proper PNG to avoid future confusion
source_png = source_icon  # overwrite in-place
img.save(source_png, "PNG")
print(f"Saved source as proper PNG: {source_png}")

# Android mipmap density -> launcher icon size (px)
# Standard Android launcher icon sizes
LAUNCHER_SIZES = {
    "mipmap-mdpi": 48,
    "mipmap-hdpi": 72,
    "mipmap-xhdpi": 96,
    "mipmap-xxhdpi": 144,
    "mipmap-xxxhdpi": 192,
}

# Adaptive icon foreground size (with padding for safe zone)
FOREGROUND_SIZES = {
    "mipmap-mdpi": 108,
    "mipmap-hdpi": 162,
    "mipmap-xhdpi": 216,
    "mipmap-xxhdpi": 324,
    "mipmap-xxxhdpi": 432,
}

# Notification icon (ic_stat_logo) sizes - smaller
NOTIFICATION_SIZES = {
    "mipmap-mdpi": 24,
    "mipmap-hdpi": 36,
    "mipmap-xhdpi": 48,
    "mipmap-xxhdpi": 72,
    "mipmap-xxxhdpi": 96,
}


def save_resized_png(source_img, target_path, size):
    """Resize image and save as proper PNG."""
    resized = source_img.resize((size, size), Image.LANCZOS)
    resized.save(target_path, "PNG")
    print(f"  -> {target_path} ({size}x{size})")


if os.path.exists(flutter_android_res):
    for density, launcher_size in LAUNCHER_SIZES.items():
        density_dir = os.path.join(flutter_android_res, density)
        if not os.path.exists(density_dir):
            os.makedirs(density_dir, exist_ok=True)

        foreground_size = FOREGROUND_SIZES[density]
        notif_size = NOTIFICATION_SIZES[density]

        # ic_launcher.png - standard launcher icon
        target = os.path.join(density_dir, "ic_launcher.png")
        save_resized_png(img, target, launcher_size)

        # ic_launcher_round.png - round launcher icon (same as launcher)
        target = os.path.join(density_dir, "ic_launcher_round.png")
        save_resized_png(img, target, launcher_size)

        # ic_launcher_foreground.png - adaptive icon foreground (larger, with safe zone)
        target = os.path.join(density_dir, "ic_launcher_foreground.png")
        save_resized_png(img, target, foreground_size)

        # ic_stat_logo.png - notification icon (smaller)
        target = os.path.join(density_dir, "ic_stat_logo.png")
        save_resized_png(img, target, notif_size)

print("\nDone overwriting Android icons!")
