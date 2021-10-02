from django.shortcuts import render
from email.mime.text import MIMEText
from smtplib import SMTP,SMTPAuthenticationError,SMTPException
# Create your views here.

def indexmail(request):
    strSmtp='smtp.gmail.com:587'
    strAccount='cxz123499@gmail.com'
    strPassword='j123042827'

    content='<h2>Gmail 寄信</h2><p>這是寄信郵件測試，請勿回復</p>'
    msg=MIMEText(content,'html','utf-8')
    msg["Subject"]="線上寄信"
    mailto="cxz123499@gmail.com"#mail=["email1","email2"]

    server=SMTP(strSmtp)#create SMTP connection
    server.ehlo()#connet with server
    server.starttls()#TLS security
    try:
        server.login(strAccount,strPassword)
        server.sendmail(strAccount,mailto,msg.as_string())
        hint="郵件已發送"
    except SMTPAuthenticationError:
        hint="Cannot login"
    except:
        hint="Sending Error"
    server.quit()#close connection
    return render(request,"mailindex.html",locals())
