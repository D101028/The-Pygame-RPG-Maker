import cv2
import numpy as np

def create_numbered_images(width, height, num, output_file='output.png'):
    # Create a list to store individual number images
    images = []
    
    for i in range(0, num + 1):
        # Create a black image
        img = np.zeros((height, width, 3), dtype=np.uint8)
        
        # Set the font and scale
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = min(width, height) / 50  # Adjust font scale based on the size
        font_thickness = 2
        
        # Get the size of the text box
        text = str(i)
        text_size = cv2.getTextSize(text, font, font_scale, font_thickness)[0]
        
        # Calculate the position to center the text
        text_x = (img.shape[1] - text_size[0]) // 2
        text_y = (img.shape[0] + text_size[1]) // 2
        
        # Put the text on the image
        cv2.putText(img, text, (text_x, text_y), font, font_scale, (255, 255, 255), font_thickness)
        
        # Add the image to the list
        images.append(img)
    
    # Calculate the dimensions for the final image
    num_images = len(images)
    rows = (num_images + 9) // 10  # Ceiling division to determine the number of rows
    final_image_height = rows * height
    final_image_width = 10 * width
    
    # Create the final image
    final_image = np.zeros((final_image_height, final_image_width, 3), dtype=np.uint8)
    
    # Place each small image in the final image
    for idx, img in enumerate(images):
        row = idx // 10
        col = idx % 10
        start_y = row * height
        start_x = col * width
        final_image[start_y:start_y+height, start_x:start_x+width] = img
    
    # Save the final image
    cv2.imwrite(output_file, final_image)
    print(f"Image saved as {output_file}")

# Example usage
create_numbered_images(64, 64, 99, 'numbered_images.png')
