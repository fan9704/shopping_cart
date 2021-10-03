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
    
def addtocart1(request,ctype=None,productid=None):
    global cartlist
    if ctype=='add':
        product=models.ProdeuctModel.objects.get(id=productid)
        flag=True
        for unit in cartlist:
            if product.pname ==unit[0]:#product exist
                unit[2]=str(int(unit[2])+1)#count++
                unit[3]=str(int(unit[3])+product.pprice)#accumulate price
                flag=False
                break
        if flag:
            temlist=[]
            temlist.append(product.pname)
            temlist.append(str(product.pprice))
            temlist.append("1")#temp quantity ==1
            temlist.append(str(product.pprice))#total price
            cartlist.append(temlist)
        request.session['cartlist']=cartlist
        return redirect('/cart/')
    elif ctype=="update":
        n=0
        for unit in cartlist:
            unit[2]=request.POST.get('qty'+str(n),'1')
            unit[3]=str(int(unit[1])*int(unit[2]))#P*Q =total price
            n+=1
    elif ctype=="empty":
        cartlist=[]
        request.session['cartlist']=cartlist
        return redirect('/index/')
    elif ctype=='remove':
        del cartlist[int(productid)]
        request.session['cartlist']=cartlist
        return redirect("/cart/")

def cartorder(request):
    pass