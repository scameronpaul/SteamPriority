import os
import regex as re

default_steam_directory = "C:\\Program Files (x86)\\Steam"
library_folders = default_steam_directory + "\\steamapps\\libraryfolders.vdf"

if not os.path.exists(library_folders):
    print("Unable to locate default libraries file...")
    os._exit(1)

steam_folders = []
with open(library_folders, "r") as f:
    file_text = f.read().replace('\t', '').replace('\\\\', '\\')
    for iter in re.finditer("path", file_text):
        path = file_text[iter.end()+1:]
        path = path[path.find('"')+1:path.find('\n')-1] + "\\steamapps"
        if os.path.exists(path):
            steam_folders.append(path)

def set_priority(file, level=2):
    file_text = open(file, 'r').read()
    with open(file, 'w') as f:
        f.write(re.sub(r"(?<=AutoUpdateBehavior\D*)(\d+)", str(level), file_text))
    print(f"Set priority to level {level} for {file}")

for folder in steam_folders:
    for filename in os.listdir(folder):
        f = os.path.join(folder, filename)
        if os.path.isfile(f):
            if filename.split('.')[1] == 'acf':
                set_priority(f, 2)