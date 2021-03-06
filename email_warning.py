import smtplib
from socket import gaierror
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_message(pressure_list):

    port = 465
    password = "4hJszPE9BYRXz2mHc9BYI7fCw85" # paste your password generated by Mailtrap
    
    # Specify the sender’s and receiver’s email addresses:
    context = ssl.create_default_context()
    
    sender = "person645h@gmail.com"
    receiver = "randomguy13587@gmail.com"
    list_string = ','.join(str(p) for p in pressure_list)
    message = MIMEMultipart("alternative")
    message["Subject"] = "Leak Detected"
    message["From"] = sender
    message["To"] = receiver
    text = "There may have been a leak. The last pressures were {}".format(list_string)
    part1 = MIMEText(text, "plain")
    message.attach(part1)

    try:

        with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
            server.login("person645h@gmail.com", password)
        
            server.sendmail(sender, receiver, message.as_string())
    except (gaierror, ConnectionRefusedError):
        # tell the script to report if your message was sent or which errors need to be fixed
        print('Failed to connect to the server. Bad connection settings?')
    except smtplib.SMTPServerDisconnected:
        print('Failed to connect to the server. Wrong user/password?')
    except smtplib.SMTPException as e:
        print('SMTP error occurred: ' + str(e))
    else:
        print('Sent') 
if __name__ == '__main__':
    send_message([1, 2, 3, 5, 6])
