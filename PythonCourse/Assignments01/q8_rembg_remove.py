# Q8: Remove background using rembg
from rembg import remove
from PIL import Image

input_path = "photo.jpg"
output_path = "photo_no_bg.png"

input_image = Image.open(input_path)
output_image = remove(input_image)
output_image.save(output_path)

print("Background removed and saved as", output_path)
