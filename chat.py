import gradio as gr
from agent import ask

demo = gr.Interface(
    fn=ask,
    inputs=gr.Textbox(label="Ask a question"),
    outputs=gr.Textbox(label="Answer"),
    title="RAG Agent Memory"
)

demo.launch()