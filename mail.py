import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def sendMail():
    try :
        sender_email = "simplon.devcloud@gmail.com"
        receiver_email = "simplon.devcloud@gmail.com"
        password = input("Type your password and press enter:")

        message = MIMEMultipart("alternative")
        message["Subject"] = "New Games BG !"
        message["From"] = sender_email
        message["To"] = receiver_email

        # Create HTML version of my message
        html_format_message = """\
        <html>
        <body>
            <p>Hi,<br>
            T'as envie de geeker Bro ? Check this out !<br>
            file:///home/simplon/DevCloud/Brief23_Test_flask/site%20vitrine/index.html"<br>
            <a href="///home/simplon/DevCloud/Brief23_Test_flask/site%20vitrine/index.html">Click Here</a> 
            <a href="http://localhost:4500/TOP?name=PC&ranking=10">This link shoul work</a>
            </p>
        </body>
        </html>
        """

        # Turn these into html MIMEText objects
        message_as_object = MIMEText(html_format_message, "html")
        # Add HTML parts to MIMEMultipart message
        message.attach(message_as_object)

        # Create secure connection with server and send email
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message.as_string())

        print("Message sent")

    except Exception as e:
        print("An error occured during the sent of an email :", e)

sendMail()