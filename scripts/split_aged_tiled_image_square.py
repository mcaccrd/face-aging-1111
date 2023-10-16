import os
from PIL import Image

def split_tiled_image(master_folder, master_id):
    print("Splitting tiled image into individual frames...")
    
    assets_folder = os.path.join(master_folder, "Assets")
    keys_aged_folder = os.path.join(assets_folder, "keys-aged")
    keys_original_folder = os.path.join(assets_folder, "keys-original")
    
    # Find the tiled aged image
    for img in os.listdir(keys_aged_folder):
        if f"{master_id}-tiled-aged" in img:
            tiled_aged_image_path = os.path.join(keys_aged_folder, img)
            break
    else:
        print(f"No tiled aged image found in {keys_aged_folder}. Exiting.")
        return

    # Load the tiled aged image
    tiled_aged_image = Image.open(tiled_aged_image_path)
    img_width, img_height = tiled_aged_image.size

    # Filter the filenames of individual frames from keys-original
    original_frame_names = [name for name in sorted(os.listdir(keys_original_folder)) if name.startswith('image') and name.endswith('.jpg')]

    # Split the image into individual frames
    frame_width = img_width // 2
    frame_height = img_height // 2

    for i in range(2):
        for j in range(2):
            left = j * frame_width
            upper = i * frame_height
            right = left + frame_width
            lower = upper + frame_height

            frame_image = tiled_aged_image.crop((left, upper, right, lower))

            frame_image_path = os.path.join(keys_aged_folder, original_frame_names[i*2 + j])
            frame_image.save(frame_image_path)

    print("Tiled image split into individual frames.")

def main(master_folder):
    master_id = os.path.basename(master_folder)
    split_tiled_image(master_folder, master_id)

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python split_tiled_image.py <path_to_master_folder>")
        sys.exit(1)
    
    master_folder_path = sys.argv[1]
    main(master_folder_path)
