import asyncio
from email.mime.text import MIMEText
from os import getenv
import aiosmtplib

EMAIL_ACCOUNT=getenv('EMAIL_ACCOUNT')
EMAIL_SMTP_HOST=getenv('EMAIL_SMTP_HOST')
EMAIL_SMTP_PORT=getenv('EMAIL_SMTP_PORT')
EMAIL_PSW=getenv('EMAIL_PSW')

message = MIMEText("Sent via aiosmtplib")
message["From"] =EMAIL_ACCOUNT
message["To"] = "xx@qq.com"
message["Subject"] = "Hello World!"

async def sendemail(msg):
    async with aiosmtplib.SMTP(hostname=EMAIL_SMTP_HOST, port=EMAIL_SMTP_PORT) as smtp:
        await smtp.login(EMAIL_ACCOUNT,EMAIL_PSW)
        await smtp.send_message(msg)

async def send_email_to(to:str,msg:str,subject:str):
    message = MIMEText(msg)
    message["From"] = "瓶盖儿"
    message["To"] = to
    message["Subject"] = subject
    await sendemail(message)

async def send_email_code_to(to:str,code:str,subject:str):
    message = MIMEText("您的验证码: %s"%(code))
    message["From"] = "瓶盖儿"
    message["To"] = to
    message["Subject"] = subject
    await sendemail(message)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(sendemail(message))