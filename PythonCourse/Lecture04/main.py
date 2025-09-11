# For Image background remove
# pip install rembg
from rembg import remove
from PIL import Image

meriInputImage = 'images/Profile.jpeg'
meriOutputImage = 'images/SMAS.png'

input = Image.open(meriInputImage)
output = remove(input)
output.save(meriOutputImage)

# For audio play 
# pip install playsound == 1.2.2
from playsound import playsound
print("audio is playing ")
playsound("audio/001.mp3")
print("audio is stopped ")