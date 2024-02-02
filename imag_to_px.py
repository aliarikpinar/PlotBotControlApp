import PIL 
from PIL import Image
from numpy import asarray
image_path = "seksek.png"

image = Image.open(image_path)
width, height = image.size
print(width)
#print(height)
pixel_path = []
with open('readme.txt', 'w') as f:
    for y in range(height):
        for x in range(width):
            pixel = image.getpixel((x, y))
            pixel_path.append(f"{x},{y}: {pixel}")
            #print(pixel)
            if  pixel == (0,0,0):
                f.write(f"{x},{y}\n: {pixel}")
            #print({x},{y}: {pixel})
    #print(pixel_path)

# Örnek kullanım

#path = image_to_path(image_path)

#print(path)

