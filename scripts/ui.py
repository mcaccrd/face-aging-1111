
import gradio as gr
import os
import subprocess

import os
import shutil
import subprocess
import uuid
from PIL import Image

def create_directory_structure(master_folder):
    print("Creating directory structure...")
    assets_folder = os.path.join(master_folder, "Assets")
    working_folder = os.path.join(master_folder, "Working")
    final_renders_folder = os.path.join(master_folder, "Final Renders")

    os.makedirs(assets_folder, exist_ok=True)
    os.makedirs(working_folder, exist_ok=True)
    os.makedirs(final_renders_folder, exist_ok=True)

    input_video_folder = os.path.join(assets_folder, "input_video")
    keys_original_folder = os.path.join(assets_folder, "keys-original")
    keys_aged_folder = os.path.join(assets_folder, "keys-aged")
    video_frames_folder = os.path.join(assets_folder, "video_frames")

    os.makedirs(input_video_folder, exist_ok=True)
    os.makedirs(keys_original_folder, exist_ok=True)
    os.makedirs(keys_aged_folder, exist_ok=True)
    os.makedirs(video_frames_folder, exist_ok=True)

    return input_video_folder, keys_original_folder, keys_aged_folder, video_frames_folder

def process_video(input_video, output_folder):
    print("Processing input video...")
    # Make video square
    command = [
        "ffmpeg",
        "-i", input_video,
        "-vf", "crop=min(iw\,ih):min(iw\,ih)",
        "-c:a", "copy",
        os.path.join(output_folder, "processed_video.mp4")
    ]
    subprocess.run(command, check=True)

def extract_frames_from_video(video_path, output_folder):
    print("Extracting frames from video...")
    command = [
        "ffmpeg",
        "-i", video_path,
        os.path.join(output_folder, "image%04d.jpg")
    ]
    subprocess.run(command, check=True)

def select_and_copy_keyframes(video_frames_folder, keys_original_folder):
    print("Selecting and copying keyframes...")
    frame_files = sorted(os.listdir(video_frames_folder))
    total_frames = len(frame_files)
    
    if total_frames < 4:
        print("Error: The video is too short to extract 4 frames.")
        sys.exit(1)

    # Choose the first, last, and two equidistant frames
    keyframe_indices = [0, total_frames // 3, (2 * total_frames) // 3, total_frames - 1]

    for idx in keyframe_indices:
        frame_file = frame_files[idx]
        shutil.copy(os.path.join(video_frames_folder, frame_file), keys_original_folder)
    print("Keyframes selected and copied.")

def create_tiled_image(keys_original_folder, master_id):
    print("Creating tiled image from keyframes...")
    images = [Image.open(os.path.join(keys_original_folder, img)) for img in sorted(os.listdir(keys_original_folder))]
    
    # Determine the dimensions for the final image
    img_width, img_height = images[0].size
    total_width = img_width * 2
    total_height = img_height * 2

    # Create an empty image with the determined dimensions
    tiled_image = Image.new("RGB", (total_width, total_height))

    # Place each image in the tiled image
    for i in range(2):
        for j in range(2):
            tiled_image.paste(images[i*2 + j], (img_width*j, img_height*i))

    # Save the tiled image
    tiled_image_path = os.path.join(keys_original_folder, f"{master_id}-tiled-original.jpg")
    tiled_image.save(tiled_image_path)

    # Create a 1024x1024 version
    small_tiled = tiled_image.resize((1024, 1024))
    small_tiled_path = os.path.join(keys_original_folder, f"{master_id}-tiled-original-small.jpg")
    small_tiled.save(small_tiled_path)
    print("Tiled images created.")

def main(input_video_path):
    master_id = str(uuid.uuid4())
    input_video_folder, keys_original_folder, keys_aged_folder, video_frames_folder = create_directory_structure(master_id)

    shutil.copy(input_video_path, input_video_folder)
    processed_video = os.path.join(input_video_folder, "processed_video.mp4")
    process_video(input_video_path, input_video_folder)
    extract_frames_from_video(processed_video, video_frames_folder)

    select_and_copy_keyframes(video_frames_folder, keys_original_folder)
    create_tiled_image(keys_original_folder, master_id)

    print(f"Processing complete. Check the master folder: {master_id}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python preprocess_video.py <path_to_input_video>")
        sys.exit(1)
    
    input_video_path = sys.argv[1]
    main(input_video_path)

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


def on_ui_tabs():
    with gr.Blocks(analytics_enabled=False) as face_aging_interface:
        with gr.Row().style(equal_height=False):
            with gr.Column(variant='panel'):
                gr.Textbox(label='Welcome to Face Aging Plugin', lines=3)
                gr.HTML(value="<p style='margin-bottom: 1.2em'>This plugin automates the aging of faces using Stable Diffusion.</p>")
                
                # GUI for preprocess_video_square.py
                gr.File(label="Select Source Video", type="video/mp4", name="video_file")
                gr.Textbox(label="Master Folder Path (for preprocessing)", name="master_folder_preprocess")
                gr.Button(label="Execute Preprocessing", action=preprocess_video)
                
                # GUI for split_aged_tiled_image_square.py
                gr.Textbox(label="Master Folder Path (for split image)", name="master_folder_split")
                gr.Button(label="Execute Image Splitting", action=split_tiled_image)

    return (face_aging_interface, "Face Aging", "face_aging_interface"),

script_callbacks.on_ui_tabs(on_ui_tabs)
