import smtplib,email.mime.multipart,email.mime.text,email.mime.base,email.encoders
import re

from __constants import REGEX,DOMAIN

from secret import SENDER_ID,SENDER_PASSWORD,DISCORD_LINK

from smtp.Templates.Verification import VERIFICATION_MAIL


def validMail(mailID:str,regex:str=REGEX,domain:str=DOMAIN):
    if re.match(regex,mailID)is None or mailID.split("@")[1]!=domain:
        return False
    return True

def send_mail(RECEIVER,KEY):

    SUBJECT=f"Verify Email Address for IIIT-B discord server "
    MESSAGE_HTML=VERIFICATION_MAIL(KEY,str(DISCORD_LINK),"sac@iiitb.org")

    session=smtplib.SMTP("smtp-mail.outlook.com",587)
    session.starttls()
    session.login(SENDER_ID,SENDER_PASSWORD)    
    
    msg=email.mime.multipart.MIMEMultipart()
    msg['From']=SENDER_ID
    msg['To']=RECEIVER
    msg['Subject']=SUBJECT
    msg.attach(email.mime.text.MIMEText(MESSAGE_HTML,"html"))

    print("Sending mail to "+RECEIVER)
    session.sendmail(SENDER_ID,RECEIVER,msg.as_string())
    session.quit()