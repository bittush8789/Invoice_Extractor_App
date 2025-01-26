# Import required libraries and modules
# Load environment variables from .env file
from dotenv import load_dotenv
load_dotenv()  

# Import Streamlit for building the web app
import streamlit as st

# Import OS and pathlib for file handling
import os
import pathlib

# Import textwrap for text formatting
import textwrap

# Import PIL (Python Imaging Library) for image handling
from PIL import Image

# Import Google Generative AI library
import google.generativeai as genai

# Get the Google API key from environment variables
os.getenv("GOOGLE_API_KEY")

# Configure Google Generative AI with the API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

## Function to load OpenAI model and get responses
# This function takes input, image, and prompt as parameters
# and returns the response from the Gemini 1.5 Flash model
def get_gemini_response(input, image, prompt):
    # Create an instance of the Gemini 1.5 Flash model
    model = genai.GenerativeModel('gemini-1.5-flash')
    # Generate content using the model with input, image, and prompt
    response = model.generate_content([input, image[0], prompt])
    # Return the text response
    return response.text

## Function to set up input image
def input_image_setup(uploaded_file):
    # Check if a file has been uploaded
    if uploaded_file is not None:
        # Read the file into bytes
        bytes_data = uploaded_file.getvalue()

        # Create an image_part dictionary with mime type and data
        image_parts = [
            {
                "mime_type": uploaded_file.type,  # Get the mime type of the uploaded file
                "data": bytes_data
            }
        ]
        # Return the image parts
        return image_parts
    else:
        # Raise a FileNotFoundError if no file is uploaded
        raise FileNotFoundError("No file uploaded")

# Configure Streamlit page settings
st.set_page_config(
    page_title="Invoice-Extractor App!",  # Set the page title
    page_icon=":brain:",  # Set the favicon emoji
    layout="centered",  # Set the page layout option
)

# Set the header of the Streamlit page
st.header(" 🤖 Invoice-Extractor App ")

# Create a text input field for the user prompt
input = st.text_input("Input Prompt: ", key="input")

# Create a file uploader for the user to upload an image
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

# Initialize an empty string for the image
image = ""   

# If an image is uploaded, open and display it
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_column_width=True)

# Create a button for the user to submit their input
submit = st.button("Tell me about the image")

# Define a prompt for the Gemini model
input_prompt = """
               You are an expert in understanding invoices.
               You will receive input images as invoices &
               you will have to answer questions based on the input image
               """

## If the submit button is clicked
if submit:
    # Set up the input image
    image_data = input_image_setup(uploaded_file)
    # Get the response from the Gemini model
    response = get_gemini_response(input_prompt, image_data, input)
    # Display the response as a subheader
    st.subheader("The Response is")
    st.write(response)