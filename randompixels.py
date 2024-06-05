import random
from PIL import Image

def randomize_image_pixels(input_path, output_path):
    # Open the input image
    image = Image.open(input_path)
    pixels = list(image.getdata())
    
    # Randomize the pixels
    random.shuffle(pixels)
    
    # Create a new image with the randomized pixels
    randomized_image = Image.new(image.mode, image.size)
    randomized_image.putdata(pixels)
    
    # Save the randomized image
    randomized_image.save(output_path)
    print(f"Randomized image saved to {output_path}")

input_image_path = 'original.jpg' 
output_image_path = 'new.jpg' 

randomize_image_pixels(input_image_path, output_image_path)

