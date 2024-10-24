import sqlite3
from flask import Flask, render_template_string
import gradio as gr
from interface import greet

app = Flask(__name__)

@app.route('/')
def home():
    return 'Hello, World!'  # Return a string

@app.route('/gradio')
def gradio_interface():
    return render_template_string("""
        <!doctype html>
        <html>
        <head>
            <title>Gradio Interface</title>
        </head>
        <body>
            <div id="gradio-interface"></div>
            <script type="module">
                import { mount } from "https://cdn.jsdelivr.net/npm/gradio@latest";
                mount("gradio-interface", "{{ gradio_url }}");
            </script>
        </body>
        </html>
    """, gradio_url=demo.local_url)

demo = gr.Interface(fn=greet, inputs="text", outputs="text")
demo.launch(share=True, inline=False, inbrowser=False, prevent_thread_lock=True)

if __name__ == '__main__':
    app.run(debug=True)
    