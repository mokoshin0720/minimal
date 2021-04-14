from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from .forms import SignUpForm, ThingForm
from .models import MinimalModel

# Create your views here.

def index(request):
    return render(request, 'index.html')

@login_required # 非ログイン状態→LOGIN_URLに飛ばす
def home(request):
    return render(request, 'home.html')

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('index')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

@login_required
def list(request):
    object_list = MinimalModel.objects.all()
    return render(request, 'list.html', {'object_list': object_list})

@login_required
def detail(request, pk):
    object = get_object_or_404(MinimalModel, pk=pk)
    return render(request, 'detail.html', {'object': object})

# @login_required
# def create(request):
#     if request.method == 'POST':
#         form = ThingForm(request.POST)
#         if form.is_valid():
#             thing = MinimalModel()
#             print('Here')
#             thing.title = request.POST['title']
#             thing.author = request.user
#             thing.buy_reason = request.POST['buy_reason']
#             thing.sell_reason = request.POST['sell_reason']
#             thing.obj_image = request.FILES['obj_image']
#             thing.buy_date = request.POST['buy_date']
#             thing.buy_price = request.POST['buy_price']
#             thing.save()            

#             return redirect('list')
#     else:
#         form = ThingForm
#     return render(request, 'create.html', {'form': form})

@login_required
def create(request):
    if request.method == 'POST':
        form = ThingForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()            
            return redirect('list')
    else:
        form = ThingForm
    return render(request, 'create.html', {'form': form})