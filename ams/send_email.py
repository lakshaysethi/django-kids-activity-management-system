# using SendGrid's Python Library
# https://github.com/sendgrid/sendgrid-python
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail



def sendEmailWithSendGrid(customMessage):
        
        
    message = Mail(
        from_email='lakshaynew@gmail.com',
        to_emails=customMessage.to_emails,
        subject=customMessage.subject,
        plain_text_content= customMessage.plain_text_content,
        html_content=customMessage.html_content)


    
    
    try:
        sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
        print('sent')
    except Exception as e:
        print(e.body)