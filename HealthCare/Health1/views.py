from django.shortcuts import render,redirect
from .forms import SignUpForm,LogInForm
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.core.paginator import Paginator
from .models import *

def home(request):
    request.session['cart']={}
    data=HealthProduct.objects.all()
    return render(request,"Health1/index.html",{'data':data})




def search(request):
    data=HealthProduct.objects.all()
    search_data=request.GET.get('search')
    if request.method=="POST":
        stock=int(request.POST.get('instock'))
        required=int(request.POST.get('req_quantity'))
        id=int(request.POST.get('productid'))
        if required > stock:
            data=HealthProduct.objects.all()
            msg="Out of Stock"
            return render(request,"store1/Cloths.html",{'msg':msg,'data':data,'id':id})
    
        med_id=id
        cart=request.session.get('cart')
        old=cart.get(med_id)
        if old:
            cart[med_id]=required+old
        else:
            cart[med_id]=required
        request.session['cart']=cart
        cart=request.session.get('cart')
    if search_data:
        data=data.filter(name__icontains=search_data)
        return render(request,"Health1/search.html",{'data':data})
    else:
        msg="Data Not Found"
        return render(request,"Health1/search.html",{'msg':msg})
    


def shop(request):
    if request.method=="POST" and request.POST.get('max'):
        mx=int(request.POST.get('max'))
        # mn=int(request.POST.get('min'))
        data1=HealthProduct.objects.all()
        # data=HealthProduct.products.Filter(min,max)
        return render(request,"Health1/shop.html",{'data1':data1,'mx':mx})
    if request.method=="POST":
        stock=int(request.POST.get('instock'))
        required=int(request.POST.get('req_quantity'))
        id=int(request.POST.get('productid'))
        
        if required > stock:
            data=HealthProduct.objects.all()
            msg="Out of Stock"
            return render(request,"store1/Cloths.html",{'msg':msg,'data':data,'id':id})
        
        med_id=id
        cart=request.session.get('cart')
        old=cart.get(med_id)
        if old:
            cart[med_id]=required+old
        else:
            cart[med_id]=required
        request.session['cart']=cart
        cart=request.session.get('cart')

    mydata=HealthProduct.objects.all()
    paginator_data=Paginator(mydata,3)
    page_no=request.GET.get('page')
    finaldata=paginator_data.get_page(page_no)
    lastpage=finaldata.paginator.num_pages
    data=HealthProduct.objects.all()

    return render(request,"Health1/shop.html",{'data':data,'finaldata':finaldata,'lastpage':lastpage,'totalpage':[n+1 for n in range(lastpage)]})


    # if request.method=="POST":
    #     required=int(request.POST.get('req_quantity'))
    #     id=int(request.POST.get('productid'))
    #     med="medi"
    #     med_id=med+str(id)
    #     cart=request.session.get('cart')
    #     old=cart.get(med_id)
    #     if old:
    #         cart[med_id]=required+old
    #     else:
    #         cart[med_id]=required
    #     request.session['cart']=cart
    #     cart=request.session.get('cart')
def addcart(request):
    data=request.session.get('cart')
    print(data)
    list_final=[]
    GT=0
    for i,j in data.items():
            id=i
            d1=HealthProduct.objects.get(pk=id)
            price=d1.productprice
            total=j*price
            lis=[d1,j,total]
            list_final.append(lis)
            GT+=total

    return render(request,"Health1/mycart.html",{'list_final':list_final,'GT':GT})

        # if "wmen" in i:
        #     id=int(i[4:])
        #     d1=HealthProduct.objects.get(pk=id)
        #     price=d1.productprice
        #     total=j*price
        #     lis=[d1,j,total]
        #     list_final.append(lis)
        #     GT+=total



def sign_up(request):
    if request.method=="POST":
        fm=SignUpForm(request.POST)
        if fm.is_valid():
            fm.save()
            messages.success(request,"SIGNUP SUCCESS")
            return render(request,'Health1/Login.html',{'fm':fm})
    else:
        fm=SignUpForm()
    return render(request,'Health1/signup.html',{'fm':fm})



def Log_in(request):
    if request.method=="POST":
        fm=LogInForm(request=request,data=request.POST)
        if fm.is_valid():
            fname=fm.cleaned_data['username']
            fpass=fm.cleaned_data['password']
            user=authenticate(username=fname,password=fpass)
            if user is not None:
                login(request,user)
                messages.success(request,"LOGIN SUCCESFULL")
                fm=LogInForm()
                return redirect("home")
    else:
        fm=LogInForm()
    return render(request,"Health1/Login.html",{'fm':fm})



def Log_out(request):
    logout(request)
    fm=SignUpForm()
    messages.success(request,"LOGOUT SUCCESSFULLY")
    return render(request,'auth1/signup.html',{'fm':fm})



def add(request,id):
    id=request.POST.get(id=id)
    cat="medi"
    user=request.user
    quan=id.productquantity
    ins=Transaction(user=user,category=cat,category_id=id,purchase_quan=quan)
    ins.save()
    return redirect("shop")



import razorpay
from django.views.decorators.csrf import csrf_exempt

def item_payment(request):
    if request.method=="POST":
        name = request.POST['productname']
        amount = float(request.POST['productprice']) * 100
        print(amount)
        client = razorpay.Client(auth=("rzp_test_LL3yvrWOvyuM0w" , "d72uVsuzf31GsrPGRuY9MBic" ))
        response_payment = client.order.create({'amount':amount, 'currency':'INR',
                              'payment_capture':'1' })
    
        print(response_payment)
        order_status = response_payment['status']
        order_id = response_payment['id']
        
        if order_status=='created':
            product = PurchaseItem(name=name , amount =amount , order_id = response_payment['id'],)
            product.save()
            data=request.session.get('cart')
            print(data)
            list_final=[]
            GT=0
            for i,j in data.items():
                id=i
                d1=HealthProduct.objects.get(pk=id)
                price=d1.productprice
                total=j*price
                lis=[d1,j,total]
                list_final.append(lis)
                GT+=total
            return render(request,'Health1/mycart.html',{'payment':response_payment,'list_final':list_final,'GT':GT})
        



@csrf_exempt
def payment_status(request):
    # print(request.POST)
    if request.method=='POST':
        response = request.POST
        print(response)
        params_dict = {
            'razorpay_order_id': response['razorpay_order_id'],
            'razorpay_payment_id': response['razorpay_payment_id'],
            'razorpay_signature': response['razorpay_signature']
        }

        # client instance
        client = razorpay.Client(auth=("rzp_test_LL3yvrWOvyuM0w" , "d72uVsuzf31GsrPGRuY9MBic" ))

        try:
            status = client.utility.verify_payment_signature(params_dict)
            item = PurchaseItem.objects.get(order_id=response['razorpay_order_id'])
            item.razorpay_payment_id = response['razorpay_payment_id']
            item.paid = True
            item.save()
            return render(request, 'razorpay/payment_status.html', {'status': True})
        except:
            return render(request, 'Health1/payment_status.html', {'status': False})
    return render(request, 'Health1/payment_status.html')


# def make_payment(request):
#     if request.method=="POST":
#         if request.user.is_authenticated:
#             user=request.user
#             data=request.session.get('cart')
#             for i,j in data.items():
#                     if 'medi' in i:
#                         cat='medi'
#                         id_str=i[4:]
#                         try:
#                             id=int(id_str)
#                         except ValueError:
#                             continue
#                     quan=j
#                     print(quan)
#                     product_name=i.name
#                     print(product_name)
#             request.session['cart']={}
#             return redirect("/")
#         else:
#             return redirect("login")




# def make_payment(request):
#     if request.method=="POST":
#         if request.user.is_authenticated:
#             user=request.user
#             data=request.session.get('cart')
#             for i,j in data.items():
#                     id_str=i
#                     try:
#                         id=int(id_str)
#                     except ValueError:
#                         continue
#                     quan=j
#                     cat="medi"
#                     ins=Transaction(user=user,category=cat,category_id=id,purchase_quan=quan)
#                     ins.save()
#             request.session['cart']={}
#             return redirect("/")
#         else:
#             return redirect("login")

# if req.user.is_authenticated:
#     user=req.user
# data=request.session.get('cart')

#dlt cart item
# req.session['cart']={}