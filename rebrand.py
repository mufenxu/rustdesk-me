import os
import shutil

REPLACEMENTS = {
    'com.greatwall.remote': 'com.greatwall.remote',
    'com.greatwall.remote': 'com.greatwall.remote',
    '<string name="app_name">长城远控</string>': '<string name="app_name">长城远控</string>',
    'android:label="长城远控"': 'android:label="长城远控"',
    'android:scheme="gwremote"': 'android:scheme="gwremote"',
    'name: greatwall_remote': 'name: greatwall_remote',
    '长城远控': '长城远控'
}

def replace_in_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            
        modified = False
        new_content = content
        for k, v in REPLACEMENTS.items():
            if k in new_content:
                new_content = new_content.replace(k, v)
                modified = True
                
        if modified:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"Modified: {filepath}")
    except (UnicodeDecodeError, PermissionError, FileNotFoundError):
        pass

def process_directory(directory):
    for root, dirs, files in os.walk(directory):
        if '.git' in root or '.cargo' in root:
            continue
        for file in files:
            # Only process files that may contain strings
            if file.endswith(('.kt', '.java', '.xml', '.gradle', '.yaml', '.plist', '.pbxproj', '.rs', '.toml', '.dart', '.md', '.json', '.sh', '.py')):
                filepath = os.path.join(root, file)
                replace_in_file(filepath)

# Directory restructuring for android kotlin source
def rename_package_dirs(base_path):
    old_dir = os.path.join(base_path, 'com', 'carriez', 'flutter_hbb')
    new_dir = os.path.join(base_path, 'com', 'greatwall', 'remote')
    
    if os.path.exists(old_dir):
        # Create intermediate directories
        os.makedirs(os.path.join(base_path, 'com', 'greatwall'), exist_ok=True)
        # Move flutter_hbb to remote
        shutil.move(old_dir, new_dir)
        print(f"Moved directory {old_dir} to {new_dir}")
        # Clean up empty carriez if needed
        carriez_dir = os.path.join(base_path, 'com', 'carriez')
        if not os.listdir(carriez_dir):
            os.rmdir(carriez_dir)

if __name__ == "__main__":
    pwd = os.getcwd()
    print("Starting text replacement...")
    process_directory(pwd)
    
    print("Starting directory restructuring...")
    # main
    main_kotlin = os.path.join(pwd, 'flutter', 'android', 'app', 'src', 'main', 'kotlin')
    if os.path.exists(main_kotlin):
        rename_package_dirs(main_kotlin)
        
    # maybe debug / profile / test exist?
    for variant in ['debug', 'profile', 'test', 'androidTest']:
        variant_dir = os.path.join(pwd, 'flutter', 'android', 'app', 'src', variant, 'kotlin')
        if os.path.exists(variant_dir):
            rename_package_dirs(variant_dir)
    print("Done!")
