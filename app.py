import pandas as pd
import streamlit as st
from streamlit_extras.add_vertical_space import add_vertical_space
import openai
import smtplib
from email.message import EmailMessage
from config import settings
 
# Sidebar contents
with st.sidebar:
    st.title('AI Email Writer')
    st.markdown('''
    ## About
    This app takes in user's detail and preference and creates a user-tailored sales email using:
    - [Streamlit](https://streamlit.io/)
    - [OpenAI](https://platform.openai.com/docs/models) LLM model
 
    ''')
    add_vertical_space(5)
    
 
def main():
    '''Main function containing all the logic of the app. The conversation memory is defined,
    and used to trigger the GPT model.'''

    st.header("AI Email Writer 💬")

    openai.api_key = settings.openai_key #API Key for accessing the GPT model.

    messages = [
         {"role": "system", "content": "You are a kind helpful sales assistant."},
        ] #The conversation memory is created and the GPT context is defined.
    
    prompt = "Using the user's details and user's preference, write an email to recommend products they'd most likely be interested in."

    with st.form("form_1"):
        st.write("Inside the form")

        #The User details and preference are extracted.
        user_details = st.text_area("User's Detail", "", placeholder="Insert text here")
        user_preference = st.text_area("User's Preference", "", placeholder="Insert text here")

        # Every form must have a submit button.
        submitted = st.form_submit_button("Submit")
        if submitted:
            
            #Once submit button is clicked The user details and preference are added to the conversation memory
            user_details = "User's Detail: "+ user_details
            user_preference = "User's Preference: "+ user_preference

            if user_details:
                messages.append(
                    {"role": "user", "content": user_details},
                )
            if user_preference:
                messages.append(
                    {"role": "user", "content": user_preference},
                )
            
            #Finally the prompt to trigger the GPT model to create an email write up is added to the conversation.
            messages.append(
                    {"role": "user", "content": prompt},
            )
            chat = openai.ChatCompletion.create(
                model="gpt-3.5-turbo", messages=messages
            ) #GPT model is triggered.

            email = chat.choices[0].message.content
            st.write(f'{email}')
            msg = EmailMessage() #GPT response is gotten.

            #GPT response is sent to the target email.
            msg['Subject'] = 'Sales Email to Customer'
            msg['From'] = settings.email_address
            msg['To'] = "michaeligbomezie@gmail.com"
            
            msg.set_content(email)

            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                smtp.login(settings.email_address, settings.email_password)
                smtp.send_message(msg)
            st.write('Email Sent!')
            st.stop()
 
if __name__ == '__main__':
    main()