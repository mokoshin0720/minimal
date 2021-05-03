from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from .forms import SignUpForm, ThingForm, ThingUpdateForm, UserUpdateForm
from .models import CustomUser, Like, MinimalModel
from django.http import JsonResponse, HttpResponseServerError
from django.views.decorators.csrf import requires_csrf_token

def index(request):
    return render(request, 'index.html')

@login_required
def home(request):
    user = request.user
    return render(request, 'home.html', {'user':user})

def like_list(request, objects):
    liked_list = []
    for object in objects:
        liked = object.like_set.filter(user=request.user)
        if liked.exists():
            liked_list.append(object.id)
    context = {
        'objects': objects,
        'liked_list': liked_list,
    }
    return context

def list(request):
    objects = MinimalModel.objects.all()

    if request.user.is_authenticated:
        context = like_list(request, objects)
        return render(request, 'list.html', context)

    else:
        return render(request, 'list.html', {'objects': objects})

def list_satisfied(request):
    objects = MinimalModel.objects.filter(status__name='満足')

    if request.user.is_authenticated:
        context = like_list(request, objects)
        return render(request, 'list.html', context)

    else:
        return render(request, 'list.html', {'objects': objects})

def list_planed(request):
    objects = MinimalModel.objects.filter(status__name='手放し予定')

    if request.user.is_authenticated:
        context = like_list(request, objects)
        return render(request, 'list.html', context)

    else:
        return render(request, 'list.html', {'objects': objects})

def list_threw(request):
    objects = MinimalModel.objects.filter(status__name='手放した')

    if request.user.is_authenticated:
        context = like_list(request, objects)
        return render(request, 'list.html', context)

    else:
        return render(request, 'list.html', {'objects': objects})

@login_required
def like(request):
    if request.method == 'POST':
        thing = get_object_or_404(MinimalModel, pk=request.POST.get('object_id'))
        user = request.user
        liked = False
        like = Like.objects.filter(thing=thing, user=user)
        if like.exists():
            like.delete()
        else:
            like.create(thing=thing, user=user)
            liked=True
        
        context = {
            'object_id': thing.id,
            'liked': liked,
            'count': thing.like_set.count(),
        }

    if request.is_ajax():
        return JsonResponse(context)

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

def detail(request, pk):
    object = get_object_or_404(MinimalModel, pk=pk)
    current_user = request.user
    return render(request, 'detail.html', {'object': object, 'current_user': current_user})

@login_required
def update(request, pk):
    if pk:
        object = get_object_or_404(MinimalModel, pk=pk)
    else:
        object = MinimalModel()

    if object.author.id == request.user.id:
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
    
    else:
        message = '他のアカウントの投稿は編集できません。'
        return render(request, 'detail.html', {'message': message, 'object': object})


@login_required
def delete(request, pk):
    object = get_object_or_404(MinimalModel, pk=pk)
    if object.author.id == request.user.id:
        object.delete()
        message = '投稿は削除されました。'
    else:
        message = '他のアカウントの投稿は削除できません。'
    return render(request, 'detail.html', {'message': message, 'object': object})

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

def guest_login(request):
    guest_user = CustomUser.objects.get(username='ゲスト')
    login(request, guest_user)
    return redirect('index')

@login_required
def user_detail(request, pk):
    user = get_object_or_404(CustomUser, pk=pk)
    if user.id == request.user.id:
        return render(request, 'user_detail.html', {'user': user})
    else:
        return redirect('index')

@login_required
def user_update(request, pk):
    if pk:
        user = get_object_or_404(CustomUser, pk=pk)
    else:
        user = CustomUser()

    if user.id == request.user.id:
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

    else:
        return redirect('index')
    
# ユーザー投稿ページに必要なデータを取ってくる関数
def user_posts_base(pk):
    user = get_object_or_404(CustomUser, pk=pk)
    object_list = MinimalModel.objects.filter(author=user)
    satisfied_list = MinimalModel.objects.filter(author=user, status__name='満足')
    planed_list = MinimalModel.objects.filter(author=user, status__name='手放し予定')
    threw_list = MinimalModel.objects.filter(author=user, status__name='手放した')

    buy_price_sum = 0
    planed_price_sum = 0
    sell_price_sum = 0

    for i in satisfied_list:
        if i.buy_price is not None: buy_price_sum += i.buy_price

    for i in planed_list:
        if i.buy_price is not None: planed_price_sum += i.buy_price
    
    for i in threw_list:
        if i.sell_price is not None: sell_price_sum += i.sell_price

    buy_price_sum = "{:,}".format(buy_price_sum)
    planed_price_sum = "{:,}".format(planed_price_sum)
    sell_price_sum = "{:,}".format(sell_price_sum)

    context = {
        'user': user,
        'object_list': object_list,
        'satisfied_list': satisfied_list,
        'planed_list': planed_list,
        'threw_list': threw_list,
        'buy_price_sum': buy_price_sum,
        'planed_price_sum': planed_price_sum,
        'sell_price_sum': sell_price_sum,
    }

    return context

def user_posts(request, pk):
    context = user_posts_base(pk)
    return render(request, 'user_posts.html', context)

def user_posts_satisfied(request, pk):
    context = user_posts_base(pk)
    return render(request, 'user_posts_satisfied.html', context)

def user_posts_planed(request, pk):
    context = user_posts_base(pk)
    return render(request, 'user_posts_planed.html', context)

def user_posts_threw(request, pk):
    context = user_posts_base(pk)
    return render(request, 'user_posts_threw.html', context)

# 自作server_error
@requires_csrf_token
def my_customized_server_error(request, template_name='500.html'):
    import sys
    from django.views import debug
    error_html = debug.technical_500_response(request, *sys.exc_info()).content
    return HttpResponseServerError(error_html)