import smtplib
from socket import gaierror
import ssl

port = 465
password = "4hJszPE9BYRXz2mHc9BYI7fCw85" # paste your password generated by Mailtrap

# Specify the sender’s and receiver’s email addresses:
context = ssl.create_default_context()

sender = "person645h@gmail.com"
receiver = "randomguy13587@gmail.com"

# Type your message: use two newlines (\n) to separate the subject from the message body, and use 'f' to  automatically insert variables in the text
message = f"""\
Subject: Test email
To: {receiver}
From: {sender}
This is my first message with Python."""
try:

    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        server.login("person645h@gmail.com", password)
        
        server.sendmail(sender, receiver, message)
except (gaierror, ConnectionRefusedError):
  # tell the script to report if your message was sent or which errors need to be fixed
  print('Failed to connect to the server. Bad connection settings?')
except smtplib.SMTPServerDisconnected:
  print('Failed to connect to the server. Wrong user/password?')
except smtplib.SMTPException as e:
  print('SMTP error occurred: ' + str(e))
else:
  print('Sent') 
