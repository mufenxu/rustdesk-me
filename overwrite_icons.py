import os
import shutil

source_icon = r"C:\Users\25912\Desktop\rustdesk-me\res\icon.png"
flutter_android_res = r"C:\Users\25912\Desktop\rustdesk-me\flutter\android\app\src\main\res"
flutter_ios_icons = r"C:\Users\25912\Desktop\rustdesk-me\flutter\ios\Runner\Assets.xcassets\AppIcon.appiconset"
pc_res = r"C:\Users\25912\Desktop\rustdesk-me\res"

if not os.path.exists(source_icon):
    print(f"Source icon not found at {source_icon}")
    exit(1)

# Overwrite Android icons
if os.path.exists(flutter_android_res):
    for dirpath, dirnames, filenames in os.walk(flutter_android_res):
        if 'mipmap' in dirpath:
            for file in filenames:
                if file.endswith('.png'):
                    target = os.path.join(dirpath, file)
                    shutil.copy(source_icon, target)
                    print(f"Overwrote {target}")

# Overwrite iOS icons
if os.path.exists(flutter_ios_icons):
    for file in os.listdir(flutter_ios_icons):
        if file.endswith('.png'):
            target = os.path.join(flutter_ios_icons, file)
            shutil.copy(source_icon, target)
            print(f"Overwrote {target}")

# Overwrite Mac/PC icons
pc_icons = ['mac-icon.png', 'icon.png', 'logo.png']
if os.path.exists(pc_res):
    for icon in pc_icons:
        target = os.path.join(pc_res, icon)
        if os.path.exists(target):
            shutil.copy(source_icon, target)
            print(f"Overwrote PC/Mac icon at {target}")

print("Done overwriting icons!")
