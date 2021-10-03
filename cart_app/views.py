from typing_extensions import Required
from django.shortcuts import get_object_or_404, render,redirect
from email.mime.text import MIMEText
from smtplib import SMTP,SMTPAuthenticationError,SMTPException

from cart_app import models
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

message=''
cartlist=[]
customname=''
customphone=''
customaddress=''
customemai=''

def index(request):
    global cartist
    if 'cartlist' in request.session:
        cartlist=request.session['cartlist']
    else:
        cartlist=[]
    cartnum=len(cartlist)
    productall=models.ProdeuctModel.objects.all()
    return render(request,"index.html",locals())

def detail(request,productid=None):
    product=models.ProdeuctModel.objects.get(id=productid)
    return render(request,"detail.html",locals())

def cart(request):
    global cartlist
    cartlist1=cartlist
    total=0
    for unit in cartlist:
        total+=int(unit[3])
    grandtotal=total+100
    return render(request,"cart.html",locals())
    
