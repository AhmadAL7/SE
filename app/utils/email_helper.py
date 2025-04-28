

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email(to, subject, body):
    sender_email = "restaurantremindertest@gmail.com"
    app_password = "zmsmgnoancpigprx"  # gmail App Password

    # Create the email
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = to
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    try:
        # Connect to Gmail SMTP server
        server = smtplib.SMTP('smtp.gmail.com', 587) 
        server.starttls()  # start encrypted connections
        server.login(sender_email, app_password)
        server.send_message(msg)
        server.quit()

        print(f"mail successfully sent to {to}")
    except Exception as e:
        print(f" failed to send email to {to}: {str(e)}")
