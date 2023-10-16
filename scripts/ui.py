
import gradio as gr
from modules import script_callbacks

def on_ui_tabs():
    with gr.Blocks(analytics_enabled=False) as face_aging_interface:
        with gr.Row().style(equal_height=False):
            with gr.Column(variant='panel'):
                gr.Textbox(label='Welcome to Face Aging Plugin', lines=3)
                gr.HTML(value="<p style='margin-bottom: 1.2em'>This plugin automates the aging of faces using Stable Diffusion.</p>")
    return (face_aging_interface, "Face Aging", "face_aging_interface"),

script_callbacks.on_ui_tabs(on_ui_tabs)
