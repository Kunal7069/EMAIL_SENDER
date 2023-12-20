import streamlit as st
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import os

# Streamlit app title
st.title("Data Fetching App")

# Get user input
password = st.text_input("Password:")
recipient_email = st.text_input("Recipient Email:")
send_date = st.date_input("Select Date")
# body = "The data for asked date is: "
subject = "DATA"
# body = "formatted_date4"

# Gmail credentials (replace with your own)
sender_email = "k63814776@gmail.com"
sender_password = "bnyc enyb ekxt cwii"



from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from datetime import datetime,date
import numpy as np

# from mysite.tasks import add


def sheet(formatted_date):
    # entriesadded=EntriesAdded.objects.filter(name='LadleUpdateRoomWise')
    # count=entriesadded[0].count
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
    SPREADSHEET_ID = '1AQ6TgA_hm2bocR8eEwC9WLBDc7vScjg2ZhKAwAvIIBQ'
    SAMPLE_RANGE_NAME = 'Sheet1'
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json",SCOPES)
    if not creds or not creds.valid:
    
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json",SCOPES)
            creds = flow.run_local_server(port=0)
        with open("token.json","w") as token:
            token.write(creds.to_json())
    service = build("sheets","v4", credentials=creds)
    sheet = service.spreadsheets().get(spreadsheetId=SPREADSHEET_ID).execute()
    sheets = sheet['sheets']
    # today = date.today()
    today = str(formatted_date)
    # Print sheet names
    for sheet in sheets:
        sheet_title = sheet['properties']['title']
        if sheet_title == today:
            break
    else:
        
    # Create a new sheet with today's date as the name
        request_body = {
            'requests': [
                {
                    'addSheet': {
                        'properties': {
                            'title': today
                        }
                    }
                }
            ]
        }
        service.spreadsheets().batchUpdate(spreadsheetId= SPREADSHEET_ID , body=request_body).execute()
    # 

    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SPREADSHEET_ID,range=f'{today}!A:G').execute()
    value = result.get('values',[])
    value = np.array(value)
    return value
    

# Function to send email
def send_email(recipient, subject):
    try:
        # Create the MIME object
        formatted_date = send_date.strftime("%Y-%m-%d")

        # Concatenate the date with the existing body
        # body = f"{body} {formatted_date}"
        # print(body) 
        body = sheet(formatted_date)
        print(body) 
        numpy_array = body
        numpy_array = numpy_array[1:]
        numpy_array = numpy_array[:,[0,1,2,5]]
        headings = ["Laddle number","Location","Entry time","Exit time"]
        numpy_array = np.vstack((headings, numpy_array))
        from prettytable import PrettyTable
        data = numpy_array

# Create a PrettyTable instance
        table = PrettyTable()

        # Set the column names
        table.field_names = data[0]

        # Add rows to the table
        for row in data[1:]:
            table.add_row(row)
        body = table
        print(body) 
        message = MIMEMultipart()
        message['From'] = sender_email
        message['To'] = recipient
        message['Subject'] = subject
        message.attach(MIMEText(f"Your required data is \n {body}", 'plain'))

        # Connect to Gmail's SMTP server
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            # Login to the sender's email account
            server.login(sender_email, sender_password)

            # Send the email
            server.sendmail(sender_email, recipient, message.as_string())

        st.success("Email sent successfully!")

    except Exception as e:
        st.error(f"An error occurred: {e}")
        print(e)
# Button to send email
if st.button("Get Data"):
    if password=="12345":
        
        send_email(recipient_email, subject)
    else:
        st.error("Wrong Password!")
