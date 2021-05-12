from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from .forms import SignUpForm, ThingForm, ThingUpdateForm, UserUpdateForm
from .models import CustomUser, Like, MinimalModel
from django.http import JsonResponse, HttpResponseServerError
from django.views.decorators.csrf import requires_csrf_token
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def index(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('user_posts', pk=user.id)
    else:
        form = SignUpForm()
    return render(request, 'index.html', {'form': form})

@login_required
def home(request):
    user = request.user
    return render(request, 'home.html', {'user':user})

def like_list(request, page_obj):
    liked_list = []
    for object in page_obj:
        liked = object.like_set.filter(user=request.user)
        if liked.exists():
            liked_list.append(object.id)
    context = {
        'page_obj': page_obj,
        'liked_list': liked_list,
    }
    return context

# ページネーションの元となる関数
def paginate_query(request, queryset, count):
  paginator = Paginator(queryset, count)
  page = request.GET.get('page')
  try:
    page_obj = paginator.page(page)
  except PageNotAnInteger:
    page_obj = paginator.page(1)
  except EmptyPage:
    page_obj = paginator.page(paginator.num_pages)
  return page_obj

PAGE_PER_ITEM = 2

def list(request):
    all_objects = MinimalModel.objects.order_by('-created_at')
    page_obj = paginate_query(request, all_objects, PAGE_PER_ITEM)   # ページネーション

    if request.user.is_authenticated:
        context = like_list(request, page_obj)
        return render(request, 'list.html', context)

    else:
        return render(request, 'list.html', {'page_obj': page_obj})

def list_satisfied(request):
    all_objects = MinimalModel.objects.filter(status__name='満足').order_by('-created_at')
    page_obj = paginate_query(request, all_objects, PAGE_PER_ITEM)

    if request.user.is_authenticated:
        context = like_list(request, page_obj)
        return render(request, 'list.html', context)

    else:
        return render(request, 'list.html', {'page_obj': page_obj})

def list_planed(request):
    all_objects = MinimalModel.objects.filter(status__name='手放し予定').order_by('-created_at')
    page_obj = paginate_query(request, all_objects, PAGE_PER_ITEM)

    if request.user.is_authenticated:
        context = like_list(request, page_obj)
        return render(request, 'list.html', context)

    else:
        return render(request, 'list.html', {'page_obj': page_obj})

def list_threw(request):
    all_objects = MinimalModel.objects.filter(status__name='手放した').order_by('-created_at')
    page_obj = paginate_query(request, all_objects, PAGE_PER_ITEM)

    if request.user.is_authenticated:
        context = like_list(request, page_obj)
        return render(request, 'list.html', context)

    else:
        return render(request, 'list.html', {'page_obj': page_obj})

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
            return redirect('user_posts', pk=request.user.id)
    else:
        form = ThingForm
    return render(request, 'create.html', {'form': form})

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
                return redirect('user_posts', pk=object.author.id)
        else:
            form = ThingUpdateForm(instance=object)

        return render(request, 'update.html', {'form': form})
    
    else:
        return redirect('user_posts', pk=request.user.id)


@login_required
def delete(request, pk):
    object = get_object_or_404(MinimalModel, pk=pk)
    if object.author.id == request.user.id:
        object.delete()
    return redirect(request.META['HTTP_REFERER'])

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
            return redirect('user_posts', pk=user.id)
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

def guest_login(request):
    guest_user = CustomUser.objects.get(username='ゲスト')
    login(request, guest_user)
    return redirect('user_posts', pk=guest_user.id)

@login_required
def user_detail(request, pk):
    user = get_object_or_404(CustomUser, pk=pk)
    if user.id == request.user.id:
        return render(request, 'user_detail.html', {'user': user})
    else:
        return render(request, 'user_detail.html', {'user': request.user})

@login_required
def user_update(request, pk):
    if pk:
        user = get_object_or_404(CustomUser, pk=pk)
    else:
        user = CustomUser()

    if user.id != request.user.id:
        user = get_object_or_404(CustomUser, pk=request.user.id)
    
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
            return redirect('user_detail', pk=pk)
    else:
        form = UserUpdateForm(initial=initial_data, instance=user)    
    return render(request, 'user_update.html', {'form': form, 'user': user})
    
# ユーザー投稿ページに必要なデータを取ってくる関数
def user_posts_base(request, pk):
    user = get_object_or_404(CustomUser, pk=pk)
    object_list = MinimalModel.objects.filter(author=user).order_by('-created_at')
    satisfied_list = MinimalModel.objects.filter(author=user, status__name='満足').order_by('-created_at')
    planed_list = MinimalModel.objects.filter(author=user, status__name='手放し予定').order_by('-created_at')
    threw_list = MinimalModel.objects.filter(author=user, status__name='手放した').order_by('-created_at')

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
    context = user_posts_base(request, pk)
    page_obj = paginate_query(request, context['object_list'], PAGE_PER_ITEM)
    context['page_obj'] = page_obj
    return render(request, 'user_posts.html', context)

def user_posts_satisfied(request, pk):
    context = user_posts_base(request, pk)
    page_obj = paginate_query(request, context['satisfied_list'], PAGE_PER_ITEM)
    context['page_obj'] = page_obj
    return render(request, 'user_posts.html', context)

def user_posts_planed(request, pk):
    context = user_posts_base(request, pk)
    page_obj = paginate_query(request, context['planed_list'], PAGE_PER_ITEM)
    context['page_obj'] = page_obj
    return render(request, 'user_posts.html', context)

def user_posts_threw(request, pk):
    context = user_posts_base(request, pk)
    page_obj = paginate_query(request, context['threw_list'], PAGE_PER_ITEM)
    context['page_obj'] = page_obj
    return render(request, 'user_posts.html', context)

# 自作server_error
@requires_csrf_token
def my_customized_server_error(request, template_name='500.html'):
    import sys
    from django.views import debug
    error_html = debug.technical_500_response(request, *sys.exc_info()).content
    return HttpResponseServerError(error_html)