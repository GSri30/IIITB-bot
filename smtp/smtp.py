import smtplib,email.mime.multipart,email.mime.text,email.mime.base,email.encoders
import re

from __constants import REGEX,DOMAIN

from secret import SENDER_ID,SENDER_PASSWORD,DISCORD_LINK

from smtp.Templates.Verification import VERIFICATION_MAIL


class SMTP:

    def __init__(self) -> None:
        self.session=smtplib.SMTP("smtp-mail.outlook.com",587)
        self.session.starttls()
        self.session.login(SENDER_ID,SENDER_PASSWORD)
        self.init()

    def init(self):
        SUBJECT=f"Verify Email Address for IIIT-B discord server"
        self.msg=email.mime.multipart.MIMEMultipart()
        self.msg['From']=SENDER_ID
        self.msg['Subject']=SUBJECT


    def validMail(mailID:str,regex:str=REGEX,domain:str=DOMAIN):
        if re.match(regex,mailID)is None or mailID.split("@")[1]!=domain:
            return False
        return True


    def send_mail(self,RECEIVER,KEY):

        MESSAGE_HTML=VERIFICATION_MAIL(KEY,str(DISCORD_LINK),"sac@iiitb.org")

        self.msg['To']=RECEIVER
        self.msg.attach(email.mime.text.MIMEText(MESSAGE_HTML,"html"))

        self.session.sendmail(SENDER_ID,RECEIVER,self.msg.as_string())
    

    def quit(self):
        self.session.quit()