from django.shortcuts import render, redirect
from voteapp.models import Category, CategoryItem
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


# Create your views here.

def signup(request):

    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
             
            # login starts here
            username = request.POST['username']
            password = request.POST['password1']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("index")
            
            
    context = {"form":form}
    return render(request, "voteapp/signup.html", context)

def signin(request):
    msg = ""
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            
            if "next" in request.POST:
                return redirect(request.POST.get("next"))
            
            else:
            
                return redirect("index")
        else:
            msg = "Invalid Credentials"
            
    context = {"msg":msg}
    return render(request, "voteapp/signin.html", context)


def signout(request):
    logout(request)
    return redirect("index")

def index(request):
    context = {}
    categories = Category.objects.all()
    context['categories'] = categories
    
    return render(request, "voteapp/index.html", context)

@login_required(login_url="signin")
def detail(request,  *args, **kwargs):
    context = {}
    slug = kwargs.get('slug')

    category = Category.objects.get(slug=slug)
    context['category'] = category

    categories = CategoryItem.objects.filter(category=category)
    context['categories'] = categories
    
    msg = None
    
    if request.user.is_authenticated:
        if category.voters.filter(id=request.user.id).exists():
            msg = "voted"
    context['msg'] = msg
    
    if request.method == 'POST':
        selected_id = request.POST.get("category_item")
        print(selected_id)
        item = CategoryItem.objects.get(id=selected_id)
        item.total_vote += 1
        
        item_category = item.category 
        item_category.total_vote += 1
        
        item.voters.add(request.user)
        item_category.voters.add(request.user)
        
        item.save()
        item_category.save()
        
        return redirect("result", slug=category.slug)

    return render(request, "voteapp/detail.html", context)

@login_required(login_url="signin")
def result(request,  *args, **kwargs):
    context = {}
    slug = kwargs.get('slug')
    category = Category.objects.get(slug=slug)
    context['category'] = category

    items = CategoryItem.objects.filter(category=category)
    context['items'] = items

    return render(request, "voteapp/result.html", context)
