import random
from PIL import Image, ImageOps

def randomize_image_pixels_within_shape(input_path, mask_path, output_path):
    # Open the input image and mask image
    image = Image.open(input_path).convert("RGB")
    mask = Image.open(mask_path).convert("L")  # Convert mask to grayscale
    
    # Ensure the mask is the same size as the image
    mask = mask.resize(image.size)
    
    # Get pixels and mask data
    pixels = list(image.getdata())
    mask_data = list(mask.getdata())
    
    # Extract pixels within the shape defined by the mask
    shape_pixels = [pixel for pixel, mask_value in zip(pixels, mask_data) if mask_value > 128]
    
    # Randomize the shape pixels
    random.shuffle(shape_pixels)
    
    # Create a new list of pixels for the output image
    new_pixels = []
    shape_pixel_index = 0
    for pixel, mask_value in zip(pixels, mask_data):
        if mask_value > 128:
            new_pixels.append(shape_pixels[shape_pixel_index])
            shape_pixel_index += 1
        else:
            new_pixels.append(pixel)
    
    # Create a new image with the randomized pixels within the shape
    randomized_image = Image.new(image.mode, image.size)
    randomized_image.putdata(new_pixels)
    
    # Save the randomized image
    randomized_image.save(output_path)
    print(f"Randomized image saved to {output_path}")

# Example usage
input_image_path = 'original.jpg'  # Replace with your input image path
mask_image_path = 'mask.png'  # Replace with your mask image path
output_image_path = 'randomized_output.jpg'  # Replace with your desired output image path

randomize_image_pixels_within_shape(input_image_path, mask_image_path, output_image_path)

