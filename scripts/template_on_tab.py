
import modules.scripts as scripts
import gradio as gr
import os
from modules import script_callbacks

# Import the functionalities from the provided scripts
from preprocess_video_square import create_directory_structure
from split_aged_tiled_image_square import split_tiled_image

def on_ui_tabs():
    with gr.Blocks(analytics_enabled=False) as ui_component:
        with gr.Row():
            video_input = gr.Filebox(label="Select Video")
            master_folder_input_preprocess = gr.Directory(label="Select Directory for Master Folder")
            chop_video_btn = gr.Button("Chop Video to Frames")
            
        with gr.Row():
            master_folder_input_split = gr.Directory(label="Select Master Folder")
            master_id_input = gr.Textbox(label="Master ID")
            split_image_btn = gr.Button("Split Tiled Image")

        # Bind the functionalities to the UI components
        def chop_video_action(video_file, master_directory):
            create_directory_structure(master_directory)
            # TODO: Additional code to process the video file if needed

        def split_image_action(master_directory, master_id):
            split_tiled_image(master_directory, master_id)

        chop_video_btn.click(chop_video_action, inputs=[video_input, master_folder_input_preprocess])
        split_image_btn.click(split_image_action, inputs=[master_folder_input_split, master_id_input])

        return [(ui_component, "Extension Integration", "extension_integration_tab")]

script_callbacks.on_ui_tabs(on_ui_tabs)
