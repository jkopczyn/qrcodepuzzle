from PIL import Image
import io

def open_png_file(file_path):
    try:
        # Open the file in binary read mode
        with open(file_path, 'rb') as file:
            return file.read()
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        return None
    except Exception as e:
        print(f"Error: {str(e)}")
        return None


def qrcode_to_boolean_grid(qrcode_image):   
    # Convert binary data to image using PIL
    image = Image.open(io.BytesIO(qrcode_image))

    # Convert to grayscale
    image = image.convert('L')
    width, height = image.size
    bool_grid = []
    threshold = 128
    
    # Iterate through pixels and convert to boolean values
    for y in range(height):
        row = []
        for x in range(width):
            pixel_value = image.getpixel((x, y))
            # True for black (pixel value < threshold), False for white
            row.append(pixel_value < threshold)
        bool_grid.append(row)
    
    return bool_grid

def shrink_boolean_grid(bool_grid):
    # Get dimensions of input grid
    height = len(bool_grid)
    width = len(bool_grid[0]) if height > 0 else 0
    
    # Check dimensions are divisible by 3
    if width % 3 != 0 or height % 3 != 0:
        raise ValueError("Grid dimensions must be divisible by 3")
        
    # Initialize smaller grid
    shrunk_height = height // 3
    shrunk_width = width // 3
    shrunk_grid = []
    
    # Process grid in 3x3 blocks
    for y in range(0, height, 3):
        shrunk_row = []
        for x in range(0, width, 3):
            # Get all values in 3x3 block
            block = [
                bool_grid[y+i][x+j] 
                for i in range(3)
                for j in range(3)
            ]
            
            # Check if all values in block match
            if not all(v == block[0] for v in block):
                raise ValueError(f"Inconsistent 3x3 block at position ({x}, {y})")
                
            # Add single value for this block
            shrunk_row.append(block[0])
            
        shrunk_grid.append(shrunk_row)
        
    return shrunk_grid


# test

def print_boolean_grid(bool_grid):
    for row in bool_grid:
        print(''.join(['#' if pixel else '.' for pixel in row]))

qrcode_image = open_png_file('smaller_mosaic.png')
bool_grid = shrink_boolean_grid(qrcode_to_boolean_grid(qrcode_image))
print_boolean_grid(bool_grid)