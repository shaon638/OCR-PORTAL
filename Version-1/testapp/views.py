from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import Contact_us, Category, register_table,add_Form
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from testapp.forms import add_product_form
# Create your views here.
def homePage(request):
    # recent = Contact_us.objects.all()[:5]
    cats = Category.objects.all().order_by("cat_name")
    
    return render(request, 'home.html',{ "category":cats})
def aboutPage(request):
    cats = Category.objects.all().order_by("cat_name")
    return render(request, 'about.html',{"category":cats})
def contactPage(request):
    all_data = Contact_us.objects.all().order_by("-id")
    cats = Category.objects.all().order_by("cat_name")
    # print(data)
    if request.method == "POST":
        name = request.POST["name"]
        con = request.POST["contact"]
        sub = request.POST["subject"]
        msg = request.POST["message"]
        data = Contact_us(name = name, contact_number = con, subject = sub, message = msg)
        data.save()
        res = "Dear {} Thanks for your feedback".format(name)
        return render(request, "contact.html", {"status": res, "messages":all_data})
        # return HttpResponse("<h1 style = 'color:green'>Dear {} Data saved succefully </h1>".format(name))
    return render(request, 'contact.html',{"messages": all_data, "category":cats})

def register(request):
    if request.method == "POST":
        fname = request.POST["first"]
        lname = request.POST["last"]
        username = request.POST["uname"]
        pwd = request.POST["password"]
        em = request.POST["email"]
        conName = request.POST["contact"]
        typ = request.POST["utype"]

        usr = User.objects.create_user(username, em, pwd)
        usr.first_name = fname
        usr.last_name = lname
        usr.save()

        reg = register_table(user = usr, contact_num = conName)
        reg.save()
        return render(request, "register.html", {"status":"Dear. {} your Account Created  Succefully ".format(fname)})
    return render(request, "register.html")

def checkUser(request):
    if request.method == "GET":
        uname = request.GET["usern"]
        check = User.objects.filter(username = uname)
        if len(check) == 1:
            return HttpResponse("Exists")
        else:
            return HttpResponse("Not Exists")

def login_user(request):
    if request.method == "POST":
        un = request.POST["username"]
        pwd = request.POST["password"]
        
        user = authenticate(username = un, password = pwd)
        print(user)
        if user:
            login(request, user)
            
            if user.is_superuser:
                return HttpResponseRedirect("/admin")
            else:
                return HttpResponseRedirect("/user_dashboard")
        else:
            return render(request, "home.html",{"status":"invalid Username or Password"})
        # return HttpResponse(user)
 
    return HttpResponse("called")
@login_required
def user_dashboard(request):
    context = {}
    check = register_table.objects.filter(user__id = request.user.id)
    if len(check)>0:


        
        data = register_table.objects.get(user__id =request.user.id)
        context["data"] = data
    return render(request, "user_dashboard.html", context)
@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')

def edit_Profile(request):
    context = {}
    check = register_table.objects.filter(user__id = request.user.id)
    if len(check)>0:

        data = register_table.objects.get(user__id =request.user.id)
        context["data"] = data
    if request.method =="POST":
        fn = request.POST["fname"]
        ln = request.POST['lname']
        em = request.POST["email"]
        con = request.POST["contact"]
        age = request.POST["age"]
        ct = request.POST["city"]
        gen= request.POST["gender"]

        usr = User.objects.get(id=request.user.id)
        usr.first_name = fn
        usr.last_name = ln
        usr.email = em
        usr.save()

        data.contact_number = con
        data.age = age
        data.city = ct
        data.gender = gen
        data.save()

        if "image" in request.FILES:
            img = request.FILES["image"]
            data.profile_pic = img
            data.save()
        context["status"] = "Changes Saved Successfully"
    return render(request,"edit_profile.html", context)

def changePassword(request):
    context={}
    ch = register_table.objects.filter(user__id=request.user.id)
    if len(ch)>0:
        data = register_table.objects.get(user__id=request.user.id)
        context["data"] = data
    if request.method=="POST":
        current = request.POST["cpwd"]
        new_pas = request.POST["npwd"]
        
        user = User.objects.get(id=request.user.id)
        un = user.username
        check = user.check_password(current)
        if check==True:
            user.set_password(new_pas)
            user.save()
            context["msz"] = "Password Changed Successfully!!!"
            context["col"] = "alert-success"
            user = User.objects.get(username=un)
            login(request,user)
        else:
            context["msz"] = "Incorrect Current Password"
            context["col"] = "alert-danger"

    return render(request,"change_password.html",context)
def add_form_view(request):
    context={}
    ch = register_table.objects.filter(user__id=request.user.id)
    if len(ch)>0:
        data = register_table.objects.get(user__id=request.user.id)
        context["data"] = data
    form = add_product_form()
    if request.method=="POST":
        form = add_product_form(request.POST,request.FILES)
        if form.is_valid():
            data = form.save(commit=False)
            login_user =User.objects.get(username=request.user.username)
            data.user_name = login_user
            data.save()
            context["status"] ="{} Added Successfully".format(data.form_name)

    context["form"] = form

    return render(request,"addform.html",context)
def my_forms(request):
    context = {}
    ch = register_table.objects.filter(user__id=request.user.id)
    if len(ch)>0:
        data = register_table.objects.get(user__id=request.user.id)
        context["data"] = data
        
    all = add_Form.objects.filter(user_name__id=request.user.id).order_by("-id")
    context["forms"] = all
    return render(request,"myform.html",context)