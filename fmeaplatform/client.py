import google.generativeai as genai
from PIL import Image
import streamlit as st
from dotenv import load_dotenv
import os
from time import sleep
import datetime
import folder
import json



def prompting(history_chat):
    prompt_template=f'''

###Context: You are an automotive expert working in client service in maintenance named "Saîd" and you're supposed to communicate with clients about their real word car problems, and in doing so you're supposed to be very supportive and communicative by asking the user questions and guiding them in order to gather the following necessary data while in the same place providing the user with help regarding their problem, keep in mind that the conversation might have already started and you're supposed to complete it.

###Previous conversation to complete :
{history_chat}


###Question tree: (keep in mind you can be flexible with the questions and their ranks as long as you get all the necessary information)


- Present yourself to the user as an automotive service advisor here to help him troubleshoot his car troubles
- Ask him to provide details about his car. (name, model, year, mileage ,all if not previously provided)
- ask him to tell you about the specific problem they're experiencing with their car Is there a particular part of the car that seems to be causing the issue, like the engine, brakes, or electrical system?
- ask him When did you first notice this problem start happening? Was it recently, or has it been going on for a while?
- provoke him to describe the problem in detail.
- ask him about how would you rate the severity of this problem? (on a scale of 1 to 5 per example ), and How often does this issue occur? 
- ask him If you have any pictures or videos that might help show the problem you're describing, feel free to upload them here (if your platform supports it).  A visual reference can be very helpful!
- finnaly you can thank him and tell him that the data you've provided is valuable in understanding common car problems and how to better assist drivers in the future (Optional: Briefly explain how the data will be used for DFMEA analysis, if applicable).

###Things to take in consideration: Only one question per answer and the answer should be a short one and only introduce yourself in the first message.

###Task: Complete the conversation

    '''
    return prompt_template

with open("current.txt", "r") as file:
    history_chat = file.read()

print(history_chat)

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


with st.sidebar:
    button_text = "New Car"
    button_text2 = "New Ticket"

      # Customize this with your desired button text
    button_clicked1 = st.button(button_text)
    
    Cars = folder.get_folder_names('user')


    if button_clicked1 or Cars==[]:
        now = datetime.datetime.now()
        formatted_datetime = now.strftime("%Y%m%d%H%M%S%f")        
        folder_name = "CAR" + formatted_datetime
        folder.create_folder(path= "user", name=folder_name)
        tickets_path= 'user/' + folder_name
    



    selected_car = st.selectbox("Select a car:", Cars)
    tickets_path= 'user/' + str(selected_car) +'/'
    print(tickets_path)
    button_clicked2= st.button(button_text2)
    Tickets = folder.get_folder_names(tickets_path)

    if button_clicked2 or Tickets==[]:
        now = datetime.datetime.now()
        formatted_datetime = now.strftime("%Y%m%d%H%M%S%f")        
        folder_name = "TICKET" + formatted_datetime
        folder.create_folder(path= tickets_path , name=folder_name)
        file_path = os.path.join(tickets_path+'/'+folder_name , folder_name)

# Open the file in write mode ("w")
        try:
            with open(file_path, "w") as file:
                file.write("History chat:\n")
        except FileNotFoundError:
            print(f"Error: Path '{file_path}' does not exist. Please create the folder structure first.")
                
    Tickets = folder.get_folder_names(tickets_path)
    
    selected_ticket = st.selectbox("Select a ticket:", Tickets)

# to ADD Chat History Uncomment this
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])


st.image('logof.png', use_column_width=True)

# Input field for user's message
user_prompt = st.chat_input("Give me the review...")
# create file uploader button at the left of the send button of the chat input


img = st.file_uploader("Upload an image for the model to generate content from: ", type=["jpg", "png", "jpeg"])

history_chat=""

if user_prompt:
    # Display Image
    folder_name= 'user/' + selected_car+'/' + selected_ticket

    for message in st.session_state.chat_session.history:
        with st.chat_message(message[1]):
            st.markdown(message[0])
    st.chat_message("user").markdown(user_prompt)
    st.session_state.chat_session.history.append([user_prompt, "User"])
    history_chat+= "\n User:" + user_prompt
    




    # Generate response
    with st.spinner('Analyzing...'):
        gemini_response = model_text.generate_content([prompting(history_chat)])
    with st.chat_message("assistant"):
        st.markdown(gemini_response.text)
    st.session_state.chat_session.history.append([gemini_response.text, "Assistant"])
    history_chat+="\n AI:" + gemini_response.text
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
    history_chat+="\n User:" + user_prompt



    with st.spinner('Analyzing...'):
        gemini_response = model.generate_content([prompting(history_chat),image])
    with st.chat_message("assistant"):
        st.markdown(gemini_response.text)
    st.session_state.chat_session.history.append([gemini_response.text, "Assistant"])
    history_chat+="\n AI:" + gemini_response.text


with open("current.txt", "a") as file:
    file.write(history_chat)