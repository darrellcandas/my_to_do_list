import gradio as gr
from db import add_user

iface = gr.Interface(
    fn=add_user,
    inputs=["text", "text"],
    outputs="text",
    live=True
)

iface.launch(share=True)
