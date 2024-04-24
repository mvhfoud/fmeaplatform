import google.generativeai as genai
from PIL import Image
import streamlit as st
from dotenv import load_dotenv
import os
from time import sleep

def prompting(user_prompt):
    prompt_template=f'''
    Objective: Conduct a detailed analysis of the user's negative review and the attached image, focusing on the problem with the car. The output should be concise, using bullet points, and now also include FMEA factors to assess the risk associated with the identified failure mode.

    User Review Input:

    User's Review Text: {user_prompt}
    Required Analysis Output:

    Car Information:

    Model: Specify the model and year.
    Car Components Mentioned:

    List specific car parts involved in the issue.
    Potential Failure Modes:

    Identify the failure type for each mentioned component.
    Potential Effects:

    Describe the impact of these failures.
    Potential Causes:

    Summarize likely reasons behind these failures.
    Current Controls:

    Mention existing preventive measures.
    FMEA Assessment:

    Severity (S): Estimate the seriousness of the failure's potential impact (1-10 scale).
    Occurrence (O): Estimate the likelihood of the failure occurring (1-10 scale).
    Detection (D): Estimate the probability of detecting the failure before it occurs (1-10 scale).
    RPN Calculation: Provide the RPN = S x O x D, to prioritize the risk.
    Instructions for Analysis:

    Ensure the analysis is clear and succinct, with each point presented in bullet points.
    Focus on precise, actionable insights from both the review and the image.
    Clearly assess and estimate FMEA factors for a comprehensive risk evaluation.
    Expected Output:
    A concise report that includes the identified issues, their potential impacts and causes, current controls, and a detailed FMEA assessment to quantify the risk level associated with the failure mode.

    '''
    return prompt_template


# Load GOOGLE_API_KEY from .env file
load_dotenv()
# Configure Streamlit page settings
st.set_page_config(
    page_title="Car review",
    page_icon="🟡",  # Favicon emoji
    layout="centered",
      # Page layout option
)


# Set up Google Gemini-Pro AI model gemini-pro for chat and gemini-pro-vision for vision
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel('gemini-pro-vision')
model_text= genai.GenerativeModel('gemini-pro')

# to ADD Chat History Uncomment this
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])


st.image('logof.png', use_column_width=True)

# Input field for user's message
user_prompt = st.chat_input("Give me the review...")
# create file uploader button at the left of the send button of the chat input
st.markdown(
    """
    <style>
    /* Change button color to yellow when hovered */
    .stFileUploader>div:hover {
        background-color: yellow !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

img = st.file_uploader("Upload an image for the model to generate content from: ", type=["jpg", "png", "jpeg"])

history=""

if user_prompt:
    # Display Image

    for message in st.session_state.chat_session.history:
        with st.chat_message(message[1]):
            st.markdown(message[0])
    st.chat_message("user").markdown(user_prompt)
    st.session_state.chat_session.history.append([user_prompt, "User"])
    history+= "\n User:" + user_prompt

    # Generate response
    with st.spinner('Analyzing...'):
        gemini_response = model_text.generate_content([prompting(user_prompt)])
    with st.chat_message("assistant"):
        st.markdown(gemini_response.text)
    st.session_state.chat_session.history.append([gemini_response.text, "Assistant"])
    history+= "\n Ai:" + user_prompt
    # Add user's message to chat and display it

elif (user_prompt and img) or img:
    
    image =Image.open(img)
    with st.chat_message("user"):
        st.image(image, use_column_width=True)
    for message in st.session_state.chat_session.history:
        with st.chat_message(message[1]):
            st.markdown(message[0])
    st.chat_message("user").markdown(user_prompt)
    st.session_state.chat_session.history.append([user_prompt, "User"])
    history+= "\n User:" + user_prompt

    with st.spinner('Analyzing...'):
        gemini_response = model.generate_content([prompting(user_prompt),image])
    with st.chat_message("assistant"):
        st.markdown(gemini_response.text)
    st.session_state.chat_session.history.append([gemini_response.text, "Assistant"])
    history+= "\n Ai:" + user_prompt

print(history)