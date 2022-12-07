## https://stackoverflow.com/questions/73026671/how-do-i-now-since-june-2022-send-an-email-via-gmail-using-a-python-script

import smtplib, ssl

subject = 'some subject message'
body = """text body of the email"""
sender_email = 'my_gmail_account_name@gmail.com'
receiver_email = 'some_recipient@something.com'

# Create a multipart message and set headers
message = MIMEMultipart()
message['From'] = 'Mike'
message['To'] = receiver_email
message['Subject'] = subject
# Add body to email
message.attach(MIMEText(body, 'plain'))
# Open file in binary mode
#with open( client_zip_filename, 'rb') as attachment:
    # Add file as application/octet-stream
    # Email client can usually download this automatically as attachment
    #part = MIMEBase('application', 'octet-stream')
    #part.set_payload(attachment.read())
# Encode file in ASCII characters to send by email    
#encoders.encode_base64(part)
# Add header as key/value pair to attachment part
#part.add_header(
#    'Content-Disposition',
#    f'attachment; filename={subject}',
#)
# Add attachment to message and convert message to string
#message.attach(part)
text = message.as_string()
# Log in to server using secure context and send email
context = ssl.create_default_context()
with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as server:
    print( 'waiting to login...')
    server.login(sender_email, password)
    print( 'waiting to send...')
    server.sendmail(sender_email, receiver_email, text)
print( 'email appears to have been sent')
