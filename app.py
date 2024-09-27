import pytesseract
from PIL import Image
import gradio as gr
import re
import streamlit as st

# Set the path to the Tesseract executable
pytesseract.pytesseract.tesseract_cmd = r'C:/Program Files/Tesseract-OCR/tesseract.exe'

# Function to perform OCR
def perform_ocr(image):
    text = pytesseract.image_to_string(image, lang='hin+eng')
    return text

# Function to search for the first keyword in the extracted text
def search_first_keyword_in_text(text, keyword):
    if keyword:
        text = text.replace('\n', ' ')
        sentences = re.split(r'(?<=[.!?]) +', text)
        for sentence in sentences:
            if re.search(keyword, sentence, re.IGNORECASE):
                highlighted_sentence = re.sub(f'({re.escape(keyword)})', r'<b>\1</b>', sentence, flags=re.IGNORECASE)
                return highlighted_sentence.strip()
        return "No matching sentence found."
    else:
        return "Please enter a keyword to search."

# Main function to perform OCR and search
def ocr_and_search(image, keyword):
    try:
        extracted_text = perform_ocr(image)
        search_result = search_first_keyword_in_text(extracted_text, keyword)
        return extracted_text, search_result
    except Exception as e:
        return str(e), str(e)

# Define the web app with Streamlit and Gradio
def web_app():
    st.title("OCR and Keyword Search Application")

    # Create a Gradio interface inside Streamlit
    with gr.Blocks() as interface:
        image_input = gr.Image(type="pil", label="Upload Image")
        keyword_input = gr.Textbox(placeholder="Enter keyword to search", label="Keyword Search")
        extracted_text_output = gr.Textbox(label="Extracted Text", lines=10)
        search_result_output = gr.HTML(label="Search Result (First Matching Sentence)")

        # Button to trigger the function
        submit_button = gr.Button("Submit")
        submit_button.click(
            fn=ocr_and_search,
            inputs=[image_input, keyword_input],
            outputs=[extracted_text_output, search_result_output]
        )

    # Launch the Gradio interface
    interface.launch(share=True)

# Run the web app
if __name__ == "__main__":
    web_app()
