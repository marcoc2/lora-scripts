import os
from PIL import Image

def convert_images(input_folder, output_folder, input_format, output_format):
    # Supported formats
    supported_formats = ['jpg', 'jpeg', 'png', 'webp']

    # Normalize extensions to lowercase and remove the leading dot
    input_format = input_format.lower().lstrip('.')
    output_format = output_format.lower().lstrip('.')

    if input_format not in supported_formats or output_format not in supported_formats:
        print(f"Error: Supported formats are: {', '.join(supported_formats)}")
        return

    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for file in os.listdir(input_folder):
        if file.lower().endswith(f".{input_format}"):
            input_path = os.path.join(input_folder, file)
            base_name = os.path.splitext(file)[0]
            new_name = f"{base_name}.{output_format}"
            output_path = os.path.join(output_folder, new_name)

            # Open the image and convert it to the output format
            with Image.open(input_path) as img:
                img.save(output_path, format=output_format.upper())

            print(f"Converted: {input_path} -> {output_path}")

# Example usage:
input_folder = "path/to/your/input_folder"
output_folder = "path/to/your/output_folder"
input_format = "jpg"
output_format = "png"
convert_images(input_folder, output_folder, input_format, output_format)
