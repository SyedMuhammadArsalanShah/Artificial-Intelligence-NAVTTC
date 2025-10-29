import os 
import subprocess

files= os.listdir("videos")

# print(files)

for file in files:
    number=file.split("_")[0]
    name=file.split("_")[1]
    print(number, name)
    subprocess.run(["ffmpeg","-i",f"videos/{file}",
                   f"audio/{number}_{name}.mp3" ])