# For Image background remove
from rembg import remove
from PIL import Image

meriInputImage = 'Profile.jpeg'
meriOutputImage = 'SMAS.png'

input = Image.open(meriInputImage)
output = remove(input)
output.save(meriOutputImage)

# For audio play 
from playsound import playsound
print("audio is playing ")
playsound("001.mp3")
print("audio is stopped ")