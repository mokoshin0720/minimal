from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from .forms import SignUpForm, ThingForm, ThingUpdateForm, UserUpdateForm
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
        object = get_object_or_404(MinimalModel, pk=pk)
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

def user_update(request, pk):
    if pk:
        user = get_object_or_404(CustomUser, pk=pk)
    else:
        user = CustomUser()

    initial_data = {
        'username': user.username,
        'last_name': user.last_name, 
        'first_name': user.first_name, 
        'email': user.email,
        'password': '',
    }

    if request.method == 'POST':
        form = UserUpdateForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            user = form.save(commit=False)
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('list')
    else:
        form = UserUpdateForm(initial=initial_data, instance=user)
    
    return render(request, 'user_update.html', {'form': form, 'user': user})
    
# ユーザー投稿ページに必要なデータを取ってくる関数
def user_posts_base(pk):
    user = get_object_or_404(CustomUser, pk=pk)
    object_list = MinimalModel.objects.filter(author=user)
    satisfied_list = MinimalModel.objects.filter(author=user, status__name='満足')
    planed_list = MinimalModel.objects.filter(author=user, status__name='手放すかも')
    threw_list = MinimalModel.objects.filter(author=user, status__name='手放した')
    return user, object_list, satisfied_list, planed_list, threw_list

def user_posts(request, pk):
    user, object_list, satisfied_list, planed_list, threw_list = user_posts_base(pk)
    return render(request, 'user_posts.html', {'user':user, 'object_list': object_list, 'satisfied_list': satisfied_list, 'planed_list': planed_list, 'threw_list': threw_list})

def user_posts_satisfied(request, pk):
    user, _, satisfied_list, _, _ = user_posts_base(pk)
    return render(request, 'user_posts_satisfied.html', {'user':user, 'satisfied_list': satisfied_list})

def user_posts_planed(request, pk):
    user, _, _, planed_list, _ = user_posts_base(pk)
    return render(request, 'user_posts_planed.html', {'user':user, 'planed_list': planed_list})

def user_posts_threw(request, pk):
    user, _, _, _, threw_list = user_posts_base(pk)
    return render(request, 'user_posts_threw.html', {'user':user, 'threw_list': threw_list})