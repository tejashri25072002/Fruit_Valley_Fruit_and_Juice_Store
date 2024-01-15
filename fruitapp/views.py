from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from fruitapp.models import fruit_product,juice_product,FruitAddCart,JuiceAddCart,FruitOrder,JuiceOrder,customer_details
from django.db.models import Q
import random
import razorpay
from django.core.mail import send_mail
from django.contrib.auth.hashers import make_password

# Create your views here.
def home(request):
    userid=request.user.id
    #print("id of logged in user :",userid)
    #print("Result:",request.user.is_authenticated)
    context={}
    p=fruit_product.objects.filter(is_active=True)
    context['fruits']=p
    #print(p)
    return render(request,"home.html",context)

def ulogin(request):
    if request.method=="POST":
        uname=request.POST['uname']
        upass=request.POST['upass']
        context={}
        if uname=="" or upass=="":
            context['errmsg']="Feilds cannot be empty"
            return render(request,"login.html",context)
            #print(uname)
            #print(upass)
            #return HttpResponse("Data Fetched")
        else:
            u=authenticate(username=uname,password=upass)
            #print(u)
            #print(u.username)
            #print(u.password)
            #print(u.is_superuser)
            if u is not None:
                login(request,u)
                return redirect('/home')
            else:
                context['errmsg']="Invalid Username/Password"
                return render(request,"login.html",context)        
    else:
        return render(request,"login.html")

def register(request):
    if request.method=="POST":
        uname=request.POST['uname']
        uemail=request.POST['uemail']
        upass=request.POST['upass']
        ucpass=request.POST['ucpass']
        #print(uname)
        context={}
        if uname=="" or uemail=="" or upass=="" or ucpass=="":
            context['errmsg']="Feilds cannot be empty"
            return render(request,"register.html",context)
        elif upass!=ucpass:
            context['errmsg']="Password did not match"
            return render(request,"register.html",context)
        else:
            try:
                u=User.objects.create(password=upass,username=uemail,first_name=uname)
                u.set_password(upass)
                u.save()
                context['success']="User Registered Successfully"
                return render(request,"login.html",context)
                #return HttpResponse("Data Fetched")
            except Exception:
                context['errmsg']="Username already exists! Try Login."
                return render(request,"register.html",context)
    else:
        return render(request,"register.html")

def ulogout(request):
    logout(request)
    return redirect('/home')

def about(request):
    return render(request,'about.html')

def fruits(request):
    userid=request.user.id
    #print("id of logged in user :",userid)
    #print("Result:",request.user.is_authenticated)
    context={}
    f=fruit_product.objects.filter(is_active=True)
    context['fruits']=f
    #print(p)
    return render(request,'fruits.html',context)

def fruitdetails(request,fid):
    context={}
    f=fruit_product.objects.filter(id=fid)
    context['fruits']=f
    print(f)
    return render(request,"fruitdetails.html",context)

def juices(request):
    userid=request.user.id
    #print("id of logged in user :",userid)
    #print("Result:",request.user.is_authenticated)
    context={}
    j=juice_product.objects.filter(is_active=True)
    context['juices']=j
    #print(p)
    return render(request,'juices.html',context)

def juicedetails(request,jid):
    context={}
    j=juice_product.objects.filter(id=jid)
    context['juices']=j
    print(j)
    return render(request,"juicedetails.html",context)

def catfilter(request,fv):
    q1=Q(is_active=True)
    q2=Q(cat=fv)
    f=fruit_product.objects.filter(q1 & q2)
    print(f)
    context={}
    context['fruits']=f
    return render(request,"fruits.html",context)

def juicecatfilter(request,jv):
    q1=Q(is_active=True)
    q2=Q(juicecat=jv)
    j=juice_product.objects.filter(q1 & q2)
    print(j)
    context={}
    context['juices']=j
    return render(request,"juices.html",context)

def fruitaddcart(request,pid):
    if request.user.is_authenticated:
        userid=request.user.id
        u=User.objects.filter(id=userid)
        print(u)
        f=fruit_product.objects.filter(id=pid)
        print(f)
        q1=Q(uid=u[0])
        q2=Q(pid=f[0])
        c=FruitAddCart.objects.filter(q1 & q2)
        print(c)
        context={}
        n=len(c)
        if n==1:
            context['errmsg']="Fruit already exists in Cart"
            context['fruits']=f
            return render(request,'fruitdetails.html',context)
        else:
            c=FruitAddCart.objects.create(uid=u[0],pid=f[0])
            c.save()
            context['success']="Fruit Added to Cart!"
            context['fruits']=f
            return render(request,'fruitdetails.html',context)
    else:
        return redirect('/login')  

def juiceaddcart(request,pid):
    if request.user.is_authenticated:
        userid=request.user.id
        u=User.objects.filter(id=userid)
        print(u)
        j=juice_product.objects.filter(id=pid)
        print(j)
        q1=Q(uid=u[0])
        q2=Q(pid=j[0])
        d=JuiceAddCart.objects.filter(q1 & q2)
        print(d)
        context={}
        n=len(d)
        if n==1:
            context['errmsg']="Juice already exists in Cart"
            context['juices']=j
            return render(request,'juicedetails.html',context)
        else:
            c=JuiceAddCart.objects.create(uid=u[0],pid=j[0])
            c.save()
            context['success']="Juice Added to Cart!"
            context['juices']=j
            return render(request,'juicedetails.html',context)
    else:
        return redirect('/login') 

def fruitcart(request):
    f=FruitAddCart.objects.filter(uid=request.user.id)
    print(f)
    context={}
    context['data']=f

    s=0
    for x in f:
        print(x)
        print(x.pid.price)
        s=s+x.pid.price * x.quantity
    print(s)
    context['total']=s
    np=len(f)
    context['items']=np
    return render(request,"fruitcart.html",context)

def juicecart(request):
    j=JuiceAddCart.objects.filter(uid=request.user.id)
    print(j)
    context={}
    context['data1']=j

    s=0
    for x in j:
        print(x)
        print(x.pid.price)
        s=s+x.pid.price * x.quantity
    print(s)
    context['total']=s
    np=len(j)
    context['items']=np
    return render(request,'juicecart.html',context)

def fruitremove(request,cid):
    f=FruitAddCart.objects.filter(id=cid)
    f.delete()
    return redirect('/fruitcart')

def updatefruitquantity(request,qv,cid):
    f=FruitAddCart.objects.filter(id=cid)
    print(f[0])
    print(f[0].quantity)  
    if qv=='1':
        t=f[0].quantity+1
        f.update(quantity=t)
    else:
        t=f[0].quantity-1
        f.update(quantity=t)
    return redirect('/fruitcart')

def juiceremove(request,cid):
    j=JuiceAddCart.objects.filter(id=cid)
    j.delete()
    return redirect('/juicecart')

def updatejuicequantity(request,qv,cid):
    j=JuiceAddCart.objects.filter(id=cid)
    print(j[0])
    print(j[0].quantity)  
    if qv=='1':
        t=j[0].quantity+1
        j.update(quantity=t)
    else:
        t=j[0].quantity-1
        j.update(quantity=t)
    return redirect('/juicecart')

def fruitplaceorder(request):
    userid=request.user.id
    f=FruitAddCart.objects.filter(uid=userid)
    oid=random.randrange(1000,9999)
    print(oid)
    for x in f:
        o=FruitOrder.objects.create(order_id=oid,uid=x.uid,pid=x.pid,quantity=x.quantity)
        o.save()
        x.delete()
    fruitorders=FruitOrder.objects.filter(uid=request.user.id)
    context={}
    context['data']=fruitorders
    s=0
    for x in fruitorders:
        #print(x)
        #print(x.pid.price)
        s=s+x.pid.price * x.quantity
    print(s)
    context['total']=s
    np=len(fruitorders)
    context['items']=np
    return render(request,'fruitplaceorder.html',context)

def juiceplaceorder(request):
    userid=request.user.id
    j=JuiceAddCart.objects.filter(uid=userid)
    oid=random.randrange(1000,9999)
    print(oid)
    for x in j:
        o=JuiceOrder.objects.create(order_id=oid,uid=x.uid,pid=x.pid,quantity=x.quantity)
        o.save()
        x.delete()
    juiceorders=JuiceOrder.objects.filter(uid=request.user.id)
    context={}
    context['data1']=juiceorders
    s=0
    for x in juiceorders:
        #print(x)
        #print(x.pid.price)
        s=s+x.pid.price * x.quantity
    print(s)
    context['total']=s
    np=len(juiceorders)
    context['items']=np
    return render(request,'juiceplaceorder.html',context)

def fruitmakepayment(request):
    fruitorders=FruitOrder.objects.filter(uid=request.user.id)
    s=0
    np=len(fruitorders)
    for x in fruitorders:
        s=s+x.pid.price * x.quantity
        oid=x.order_id

    client = razorpay.Client(auth=("rzp_test_YvjZinDbG3pKzW", "3ahukKWs5YofrX6HW2Y8cCi9"))

    data = { "amount": s*100, "currency": "INR", "receipt": oid }
    payment = client.order.create(data=data)
    context={}
    context['data']=payment
    uemail=request.user.username
    print(uemail)
    context['uemail']=uemail
    #return HttpResponse("In Payment Page")
    return render(request,'fruitmakepayment.html',context)

def juicemakepayment(request):
    juiceorders=JuiceOrder.objects.filter(uid=request.user.id)
    s=0
    np=len(juiceorders)
    for x in juiceorders:
        s=s+x.pid.price * x.quantity
        oid=x.order_id

    client = razorpay.Client(auth=("rzp_test_YvjZinDbG3pKzW", "3ahukKWs5YofrX6HW2Y8cCi9"))

    data = { "amount": s*100, "currency": "INR", "receipt": oid }
    payment = client.order.create(data=data)
    context={}
    context['data1']=payment
    uemail=request.user.username
    print(uemail)
    context['uemail']=uemail
    #return HttpResponse("In Payment Page")
    return render(request,'juicemakepayment.html',context)

def fruitsendusermail(request):
    send_mail(
    "Fashion Valley Fruit Order Placed Successfully",
    "Fruit Order Completed !! Thanks for Ordering. Stay Happy and Healty",
    "tejashriprakashshinde25702@gmail.com",
    ["tejashripshinde002@gmail.com"],
    fail_silently=False,
    )
    context={}
    context['emailsend']="Email Sent Successfully for Fruit Order"
    return render(request,'home.html',context)

def juicesendusermail(request):
    send_mail(
    "Fashion Valley Juice Order Placed Successfully",
    "Juice Order Completed !! Thanks for Ordering. Stay Happy and Healty",
    "tejashriprakashshinde25702@gmail.com",
    ["tejashripshinde002@gmail.com"],
    fail_silently=False,
    )
    context={}
    context['emailsend']="Email Sent Successfully for Juice Order"
    return render(request,'home.html',context)

def password(request):
    context={}
    c=User.objects.filter(username=request.user.username)
    # t=User.objects.get(id=request.user.id)
    # o=t.password
    
    context['data']=c
    return render(request,'change_password.html',context) 

def changepassword(request,uid):
    if request.method == 'POST':
        uname=request.POST['uname']
        passw=request.POST['passw']
        newpass=request.POST['newpass']
        confirmpass=request.POST['confrimpass']
        upass1=make_password(confirmpass)
        context={}
        c=User.objects.filter(username=request.user.username)
        u=authenticate(username=uname,password=passw)

        if passw=="" or newpass=="" or confirmpass=="" :
            context['data']=c
            context['errmsg']="Fields can not be empty"
            return render(request ,'change_password.html',context)

        elif newpass!=confirmpass:
            context['data']=c
            context['errmsg']="Password is not matching "
            return render(request ,'change_password.html',context)
        else:
            u=authenticate(username=uname,password=passw)
            if u is not None:
                m=User.objects.filter(id=uid)
                m.update(password=upass1)
                context['data']=c
                context['success']='Password updated successfully,'
                return render(request ,'change_password.html',context)   
    else:
        return redirect('/changepassword') 

def user_profile(request):
    c=User.objects.filter(username=request.user.username)
    context={}
    context['data']=c
    p=customer_details.objects.filter(uname=request.user.username)
    context['data1']=p
    return render(request,'profile.html',context)

def update_profile(request,uid):
    if request.method == 'POST':
        uname=request.POST['uname']
        firstname=request.POST['firstname']
        lastname=request.POST['lastname']
        mobile=request.POST['mobile']
        address=request.POST['address']
        context={}
        c=User.objects.filter(username=request.user.username)
        context['data']=c
        p=customer_details.objects.filter(uname=request.user.username)
        context['data1']=p
        m=User.objects.filter(id=uid)
        m.update(username=uname,first_name=firstname,last_name=lastname)   
        m=customer_details.objects.filter(uname=request.user.username)
        m.create(uname=uname,firstname=firstname,lastname=lastname,mobile=mobile,address=address) 
        m.update(uname=uname,firstname=firstname,lastname=lastname,mobile=mobile,address=address) 
        context['success']='Profile updated successfully,'
        return render(request,'profile.html',context)  
    else:
        return redirect('/profile')

def display_cart(request):
    return render(request,'cart_display.html')

def orderhistory(request):
    userid=request.user.id
    f=FruitAddCart.objects.filter(uid=userid)
    j=JuiceAddCart.objects.filter(uid=userid)
    oid=random.randrange(1000,9999)
    print(oid)
    for x in f:
        o=FruitOrder.objects.create(order_id=oid,uid=x.uid,pid=x.pid,quantity=x.quantity)
        o.save()
        x.delete()
    for x in j:
        a=JuiceOrder.objects.create(order_id=oid,uid=x.uid,pid=x.pid,quantity=x.quantity)
        a.save()
        x.delete()
    fruitorders=FruitOrder.objects.filter(uid=request.user.id)
    juiceorders=JuiceOrder.objects.filter(uid=request.user.id)
    context={}
    context['data']=fruitorders
    context['data1']=juiceorders
    return render(request,'orders.html',context)
