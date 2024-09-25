from __future__ import annotations
from typing import Iterable
import gradio as gr
from gradio.themes.base import Base
from gradio.themes.utils import colors, fonts, sizes
from h2ogpte import H2OGPTE


# Initialize OpenAI client
API_KEY = "sk-vT6ijlDsPcLb3YQBLGf4mfF7FvcAurPhmI8DGFtZpJ8GM173"
REMOTE_ADDRESS = "https://h2ogpte.genai.h2o.ai"
client = H2OGPTE(address=REMOTE_ADDRESS, api_key=API_KEY)
llm_selected = 'gpt-35-turbo-1106'

# # Define available LLMs
# llms_available = [x["base_model"] for x in client.get_llms()]
# print(llms_available)

llm_selected = 'gpt-35-turbo-1106'

greeting_message = """Hello! I am YogaBuddy, your Yoga and Diet Assistant. How can I help you today? You can 
ask me about yoga poses, routines, or diet plans for your health condition."""

greetings = ["hi", "hello", "hey", "good morning", "good afternoon", "good evening"]

def yoga_diet_consultant(history, input_text):
    if input_text.lower() in greetings:
        initial_response = "🧘‍♂️ " + greeting_message + "\n\n"
        history.append([input_text, initial_response])
        return history, history
    
    user_prompt = f"""
    Act as a Yoga and Diet consultant. Analyze the following input: '{input_text}' 
    and based on that provide relevant information. If the user has asked for yoga, then give yoga exercises 
    Don't give link that dose not exists.Don't provide yoga and diet both at a time.If the user is asking for a diet,
    then provide a diet for their health condition, else provide only yoga.Also if user is asking for some recipes for 
    suggested diet then only provide recipes. Also if user is asking for details for any yoga then provide details for that yoga. 
    Also if user is asking for details for any pranayama then provide details for that pranayama.
    """
    response = client.answer_question(question=user_prompt, llm=llm_selected)
    output = response.content
    print(output)
    history.append([input_text, output])
    return history, history

class Seafoam(Base):
    def __init__(
        self,
        *,
        primary_hue: colors.Color | str = colors.purple, 
        secondary_hue: colors.Color | str = colors.purple,  
        neutral_hue: colors.Color | str = colors.gray,
        spacing_size: sizes.Size | str = sizes.spacing_md,
        radius_size: sizes.Size | str = sizes.radius_md,
        text_size: sizes.Size | str = sizes.text_lg,
        font: fonts.Font
        | str
        | Iterable[fonts.Font | str] = (
            fonts.GoogleFont("Quicksand"),
            "ui-sans-serif",
            "sans-serif",
        ),
        font_mono: fonts.Font
        | str
        | Iterable[fonts.Font | str] = (
            fonts.GoogleFont("IBM Plex Mono"),
            "ui-monospace",
            "monospace",
        ),
    ):
        super().__init__(
            primary_hue=primary_hue,
            secondary_hue=secondary_hue,
            neutral_hue=neutral_hue,
            spacing_size=spacing_size,
            radius_size=radius_size,
            text_size=text_size,
            font=font,
            font_mono=font_mono,
        )
        super().set(
            body_background_fill="url('https://i.pinimg.com/originals/a3/4a/3a/a34a3a1ff5f03e76a3e83503e627e3ae.jpg') no-repeat center center fixed",  # Change background image
            block_background_fill='rgba(128,128,128, 0.7)',
            block_border_color="black",
            block_label_border_color="black",
            block_label_border_width="2px",
            button_secondary_background_fill="rgba(128,128,128, 0.7)",  # Purple transparent button color
            button_secondary_text_color="white",  # Change secondary button text color
            block_title_text_weight="600",
            block_border_width="2px",
            block_shadow="*shadow_drop_lg",
            button_shadow="*shadow_drop_lg",
            button_large_padding="32px",
        )

seafoam = Seafoam()

with gr.Blocks(theme=seafoam) as demo:
    chatbot = gr.Chatbot(label="YogaBuddy")
    state = gr.State([])  # To keep track of chat history
    with gr.Row():
        with gr.Column(scale=15):
            txt = gr.Textbox(show_label=False, placeholder="Type your message here...")
        with gr.Column(scale=2):
            send = gr.Button("Send")
    
    def respond(history, input_text):
        return yoga_diet_consultant(history, input_text)
    
    send.click(respond, [state, txt], [chatbot, state])
    txt.submit(respond, [state, txt], [chatbot, state])

# Launch the Gradio app
demo.launch(share=True)

print("Model Running")
