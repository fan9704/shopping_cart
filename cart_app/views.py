from django.shortcuts import  render,redirect
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
customemail=''

def index(request):
    global cartist
    if 'cartlist' in request.session:
        cartlist=request.session['cartlist']
    else:
        cartlist=[]
    cartnum=len(cartlist)
    productall=models.ProductModel.objects.all()
    return render(request,"index.html",locals())

def detail(request,productid=None):
    product=models.ProductModel.objects.get(id=productid)
    return render(request,"detail.html",locals())

def cart(request):
    global cartlist
    cartlist1=cartlist
    total=0
    for unit in cartlist:
        total+=int(unit[3])
    grandtotal=total+100
    return render(request,"cart.html",locals())
    
def addtocart(request,ctype=None,productid=None):
    global cartlist
    if ctype=='add':
        product=models.ProductModel.objects.get(id=productid)
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
        request.session['cartlist']=cartlist
        return redirect('/cart/')
    elif ctype=="empty":
        cartlist=[]
        request.session['cartlist']=cartlist
        return redirect('/index/')
    elif ctype=='remove':
        del cartlist[int(productid)]
        request.session['cartlist']=cartlist
        return redirect("/cart/")


def cartorder(request):
    global cartlist,message,customname,customphone,customaddress,customemail
    cartlist1=cartlist
    total=0
    for unit in cartlist:
        total+=int(unit[3])
    grandtotal=total+100
    customname1=customname
    customphone1=customphone
    customaddress1=customaddress
    customemail1=customemail
    message1=message
    return render(request,"cartorder.html",locals())

def cartok(request):
    global cartlist,message,customname,customphone,customaddress,customemail
    cartlist1=cartlist
    total=0
    for unit in cartlist:
        total+=int(unit[3])
    grandtotal=total+100
    message=''
    customname=request.POST.get('CustomerName','')
    customphone=request.POST.get('CustomerPhone','')
    customaddress=request.POST.get('CustomerAddress','')
    customemail=request.POST.get('CustomerEmail','')
    paytype=request.POST.get('paytype','')
    customname1=customname
    if customname=='' or customphone=='' or customaddress=='' or customemail=='':
        message='姓名、電話、住址及電子郵件皆須輸入'
        return redirect('/cartorder/')
    else:
        unitorder=models.OrderModel.objects.create(subtotal=total,shipping=100,grandtotal=grandtotal,customname=customname,customphone=customphone,customaddress=customaddress,customemail=customemail,paytype=paytype)
        for unit in cartlist:
            total=int(unit[1])*int(unit[2])
            unitdetail=models.DetailModel.objects.create(dorder=unitorder,pname=unit[0],unitprice=unit[1],quantity=unit[2],dtotal=total)
        orderid=unitorder.id
        mailfrom="cxz123499@gmail.com"
        mailpw="j123042827"
        mailto=customemail
        mailsubject="織夢數位購物網 - 訂單通知"
        mailcontent="感謝您的光臨，您已經成功的完成訂購程序。\n我們將盡快把您選購的商品郵寄給您! 再次感謝您的支持\n您的訂單編號為:"+str(orderid)+"，您可以使用這個編號回到網站中查詢訂單的詳細內容。\n織夢數位購物網"
        send_simple_message(mailfrom,mailpw,mailto,mailsubject,mailcontent)
        cartlist=[]
        request.session['cartlist']=cartlist
        return render(request,"cartok.html",locals())

def send_simple_message(mailfrom,mailpw,mailto,mailsubject,mailcontent):
    global message
    strSmtp="smtp.gmail.com:587"
    strAccount=mailfrom
    strPassword=mailpw
    msg=MIMEText(mailcontent)
    msg['Subject']=mailsubject
    mailto1=mailto
    server=SMTP(strSmtp)#create SMTP connetion
    server.ehlo()#communicate with host
    server.starttls()#create safe connettion
    try:
        server.login(strAccount,strPassword)
        server.sendmail(strAccount,mailto1,msg.as_string())
    except SMTPAuthenticationError:
        message="Login ERROR"
    except Exception as E:
        message="Sending ERROR"
    server.quit()

def cartordercheck(request):
    orderid=request.GET.get('orderid','')
    customemail=request.GET.get('customemail','')
    if orderid =='' and customemail=='':
        firstsearch=1
    else:
        order=models.OrderModel.objects.filter(id=orderid)
        if order ==None or order.customemail!= customemail :
            notfound=1
        else:
            details=models.DetailModel.objects.filter(dorder=order)
    return render(request,"cartordercheck.html",locals())