
import gradio as gr
from modules import script_callbacks
import os
import subprocess

def preprocess_video(master_folder, video_file):
    # Define paths for the scripts and video
    script_path = "scripts/preprocess_video_square.py"
    video_path = os.path.join(master_folder, "input_video", video_file.name)
    
    # Save the uploaded video to the specified path
    video_file.save(video_path)
    
    # Execute the preprocess_video_square.py script
    subprocess.run(["python", script_path, master_folder], check=True)
    return "Video preprocessing completed!"

def split_tiled_image(master_folder):
    # Define path for the script
    script_path = "scripts/split_aged_tiled_image_square.py"
    
    # Execute the split_aged_tiled_image_square.py script
    subprocess.run(["python", script_path, master_folder], check=True)
    return "Tiled image split into individual frames!"

def on_ui_tabs():
    with gr.Blocks(analytics_enabled=False) as face_aging_interface:
        with gr.Row().style(equal_height=False):
            with gr.Column(variant='panel'):
                gr.Textbox(label='Welcome to Face Aging Plugin', lines=3)
                gr.HTML(value="<p style='margin-bottom: 1.2em'>This plugin automates the aging of faces using Stable Diffusion.</p>")
                
                # GUI for preprocess_video_square.py
                gr.File(label="Select Source Video", type="video/mp4", name="video_file")
                gr.Textbox(label="Master Folder Path (for preprocessing)", name="master_folder_preprocess")
                gr.Button(label="Execute Preprocessing", action=preprocess_video_square)
                
                # GUI for split_aged_tiled_image_square.py
                gr.Textbox(label="Master Folder Path (for split image)", name="master_folder_split")
                gr.Button(label="Execute Image Splitting", action=split_tiled_image)

    return (face_aging_interface, "Face Aging", "face_aging_interface"),

script_callbacks.on_ui_tabs(on_ui_tabs)
