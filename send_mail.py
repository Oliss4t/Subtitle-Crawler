import smtplib, ssl

port = 465  # For SSL
smtp_server = "smtp.gmail.com"
sender_email = "raspberry4server@gmail.com"  # Enter your address
receiver_email = "asdf@gamil.com"  # Enter receiver address
password = "secret"
message = """\
Subject: Successful Build

The buildprocess was successful"""

try:
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)
except:
    pass

