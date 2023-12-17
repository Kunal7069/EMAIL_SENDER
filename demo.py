import streamlit as st
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Streamlit app title
st.title("Email Sender App")

# Get user input
recipient_email = st.text_input("Recipient Email:")
subject = "HII"
body ="DAY 2 CONCLUDED FINALLY TODAY"

# Gmail credentials (replace with your own)
sender_email = "teamryuks@gmail.com"
sender_password = "lokw ofym loze wupx"

# Function to send email
def send_email(recipient, subject, body):
    try:
        # Create the MIME object
        message = MIMEMultipart()
        message['From'] = sender_email
        message['To'] = recipient
        message['Subject'] = subject

        # Attach the body to the email
        message.attach(MIMEText(body, 'plain'))

        # Connect to Gmail's SMTP server
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            # Login to the sender's email account
            server.login(sender_email, sender_password)

            # Send the email
            server.sendmail(sender_email, recipient, message.as_string())

        st.success("Email sent successfully!")

    except Exception as e:
        st.error(f"An error occurred: {e}")

# Button to send email
if st.button("Send Email"):
    send_email(recipient_email, subject, body)


