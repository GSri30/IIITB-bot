from email import message
import smtplib,email.mime.multipart,email.mime.text,email.mime.base,email.encoders
import os
from dotenv import load_dotenv

load_dotenv()

SENDER_ID=os.getenv("SENDER_ID")
SENDER_PASSWORD=os.getenv("SENDER_PASSWORD")


#Turn on the option in https://www.google.com/settings/security/lesssecureapps

def send_mail(RECEIVER,KEY):

    SUBJECT=f"Verify Email Address for IIIT-B discord server!"
    MESSAGE=f"Hey there!\n\nThanks for taking out your time for this!\nTo verify your email, please use the below key :\n{KEY}\nYou can use my !verify command in the same channel or can directly message me!\n\n!verify {KEY}\n\nIn case of any issues, contact any of the server admins. DO NOT reply to this mail! (I'm not an AI bot :p)\n\n\n~IIITB Discord Bot"


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
    #print(msg.as_string())
    session.quit()