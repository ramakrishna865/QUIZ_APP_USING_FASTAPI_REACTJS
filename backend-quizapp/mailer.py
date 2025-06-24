

import smtplib
from email.message import EmailMessage

def send_email(to_email: str, name: str, correct: int, total: int):
    msg = EmailMessage()
    msg['Subject'] = 'Your Quiz Results'
    msg['From'] = 'prameelarani769@gmail.com' 
    msg['To'] = to_email
    msg.set_content(f"Hi {name},\n\nYou scored {correct} out of {total} in the quiz.\n\nThank you!")

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
            smtp.starttls()
            smtp.login('prameelarani769@gmail.com', 'cnzb ix vprz')  
            smtp.send_message(msg)
      
    

        print(f"Email sent to {to_email}")
    except Exception as e:
        print(f"Error sending email: {e}")
