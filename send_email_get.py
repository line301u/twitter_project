from bottle import get, response
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import g

def send_email(user):
    try:
        sender_email = "line301u@gmail.com"
        receiver_email = user["user_email"]
        password = g.EMAIL_PASSWORD

        message = MIMEMultipart("alternative")
        message["Subject"] = "Welcome to Twitter!"
        message["From"] = sender_email
        message["To"] = receiver_email
        print(receiver_email)

        # TEXT AND HTML version of your message
        text = f"""\
        Hi {user["user_first_name"]},
        thank you for signing up!
        """

        html = f"""\
        <html>
            <body>
            <p>
                <b> Hi {user["user_first_name"]},</b><br>
                thank you for signing up!<br>
            </p>
            </body>
        </html>
        """

        # Turn these into plain/html MIMEText objects
        part1 = MIMEText(text, "plain")
        part2 = MIMEText(html, "html")

        # Add HTML/plain-text parts to MIMEMultipart message
        # The email client will try to render the last part first
        message.attach(part1)
        message.attach(part2)

        # Create connection with server and send email
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            try:
                server.login(sender_email, password)
                server.sendmail(sender_email, receiver_email, message.as_string())
                print(f"email sent to: {receiver_email}")
                return "yes, email sent"
            except Exception as ex:
                print(ex)
                return "Could not send the email"

    except Exception as ex:
        print(ex)