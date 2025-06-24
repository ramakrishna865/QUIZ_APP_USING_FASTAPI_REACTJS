import smtplib
from email.mime.text import MIMEText

def send_email(to_email: str, name: str, score: int, total: int):
    from_email = "youremail@example.com"
    password = "yourpassword"

    subject = "Your Quiz Results"
    body = f"Hello {name},\n\nYour score is {score}/{total}.\n\nThanks for participating!"

    message = MIMEText(body)
    message["Subject"] = subject
    message["From"] = from_email
    message["To"] = to_email

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(from_email, password)
            server.sendmail(from_email, to_email, message.as_string())
    except Exception as e:
        print(f"Failed to send email: {e}")
