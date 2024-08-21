import os

for root, dirs, files in os.walk("./output"):
    for file in files:
        sp = file.split(".")
        filename = ".".join(sp[:-1])
        basename = sp[-1]
        cmd = f"ffmpeg -i \"{os.path.join(root, file)}\" -vf \"scale=iw*2:ih*2\" \"{os.path.join(root, filename + '_resized.' + basename)}\""
        os.system(cmd)
