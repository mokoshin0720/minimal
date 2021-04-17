from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from .forms import SignUpForm, ThingForm, ThingUpdateForm
from .models import CustomUser, MinimalModel

# Create your views here.

def index(request):
    return render(request, 'index.html')

@login_required
def home(request):
    user = request.user
    return render(request, 'home.html', {'user':user})

@login_required
def list(request):
    object_list = MinimalModel.objects.all()
    return render(request, 'list.html', {'object_list': object_list})

# 以下、投稿に関するview
@login_required
def create(request):
    if request.method == 'POST':
        form = ThingForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()            
            return redirect('list')
    else:
        form = ThingForm
    return render(request, 'create.html', {'form': form})

@login_required
def detail(request, pk):
    object = get_object_or_404(MinimalModel, pk=pk)
    current_user = request.user
    current_user_id = request.user.id
    return render(request, 'detail.html', {'object': object, 'current_user': current_user, 'current_user_id': current_user_id,})

@login_required
def update(request, pk):
    if pk:
        object = get_object_or_404(MinimalModel, pk = pk)
    else:
        object = MinimalModel()
    
    if request.method == 'POST':
        form = ThingUpdateForm(request.POST, request.FILES, instance=object)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('list')
    else:
        form = ThingUpdateForm(instance=object)
    
    return render(request, 'update.html', {'form': form})


@login_required
def delete(request, pk):
    post = get_object_or_404(MinimalModel, pk=pk)
    post.delete()
    return redirect('list')

# 以下、ユーザーに関するview
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


def user_detail(request, pk):
    user = get_object_or_404(CustomUser, pk=pk)
    return render(request, 'user_detail.html', {'user': user})

def user_posts(request, pk):
    user = get_object_or_404(CustomUser, pk=pk)
    object_list = MinimalModel.objects.filter(author=user)
    satisfied = MinimalModel.objects.filter(author=user, status__name='満足')
    planed = MinimalModel.objects.filter(author=user, status__name='手放し予定')
    threw = MinimalModel.objects.filter(author=user, status__name='手放した')
    return render(request, 'user_posts.html', {'user':user, 'object_list': object_list, 'satisfied': satisfied, 'planed': planed, 'threw': threw})