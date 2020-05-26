# using SendGrid's Python Library
# https://github.com/sendgrid/sendgrid-python
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

message = Mail(
    from_email='me@lakshaysethi.com',
    to_emails=['alex040892@gmail.com'],
    subject='Test from python backend',
    html_content='TEST')

    

def sendEmailWithSendGrid(message):
    try:
        sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
        print('sent')
    except Exception as e:
        print(e.body)