import smtplib,email.mime.multipart,email.mime.text,email.mime.base,email.encoders
import re
import os

from __constants import REGEX,DOMAIN

from dotenv import load_dotenv
load_dotenv()
SENDER_ID=os.getenv("SENDER_ID")
SENDER_PASSWORD=os.getenv("SENDER_PASSWORD")


#Turn on the option in https://www.google.com/settings/security/lesssecureapps

def validMail(mailID:str,regex:str=REGEX,domain:str=DOMAIN):
    if re.match(regex,mailID)is None or mailID.split("@")[1]!=domain:
        return False
    return True

def send_mail(RECEIVER,KEY):

    SUBJECT=f"Verify Email Address for IIIT-B discord server! "
    MESSAGE=(f"Hey there! You have been successfully registered for IIITB discord server.\n\n"
            f"To verify your email, please use the below key : "
            f"\n'{KEY}'\n Check the rules-page in the server for more information."
            f"\n\n!verify {RECEIVER} {KEY}\n\nIn case of any issues, contact any of the server admins. "
            f"DO NOT reply to this mail! (I'm not an AI bot :p)\n\n\n~IIITB Discord Bot"
            )

    session=smtplib.SMTP("smtp.gmail.com",587)
    session.starttls()
    session.login(SENDER_ID,SENDER_PASSWORD)    
    
    msg=email.mime.multipart.MIMEMultipart()
    msg['From']=SENDER_ID
    msg['To']=RECEIVER
    msg['Subject']=SUBJECT
    msg.attach(email.mime.text.MIMEText(MESSAGE,"plain"))

    print("Sending mail to "+RECEIVER)
    session.sendmail(SENDER_ID,RECEIVER,msg.as_string())
    session.quit()