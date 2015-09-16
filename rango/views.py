from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, render_to_response
from django.template import RequestContext

from rango.models import Category, Page, UserProfile
from rango.forms import CategoryForm, PageForm
from rango.forms import UserForm, UserProfileForm
from datetime import datetime


def index(request):
    categories = Category.objects.all().order_by('-likes')[:5]
    pages = Page.objects.all().order_by('-views')[:5]
    context_dict = {'categories': categories, 'pages': pages}

    visits = request.session.get('visits')
    if not visits:
        visits = 1
    last_visit = request.session.get('last_visit')
    if last_visit:
        last_visit_time = datetime.strptime(last_visit[:-7], '%Y-%m-%d %H:%M:%S')
        if (datetime.now() - last_visit_time).days > 0:
            visits += 1
    request.session['visits'] = visits
    request.session['last_visit'] = str(datetime.now())
    return render(request, 'rango/index.html', context_dict)  # 注意rango前面是没有反斜杠的


def category(request, category_slug):
    context_dict = dict()
    try:
        cat = Category.objects.get(slug=category_slug)
        context_dict['category_name'] = cat.name
        context_dict['category_slug'] = cat.slug

        pages = Page.objects.filter(category=cat).order_by('-views')
        context_dict['pages'] = pages

        context_dict['category'] = cat
    except Category.DoesNotExist:
        pass
    return render(request, 'rango/category.html', context_dict)


@login_required
def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
            return index(request)
        else:
            print(form.errors)
    else:
        form = CategoryForm()
    return render(request, 'rango/add_category.html', {'form': form})


@login_required
def add_page(request, category_slug):
    try:
        cat = Category.objects.get(slug=category_slug)  # 不能用filter
    except Category.DoesNotExist:
        cat = None
    if request.method == 'POST':
        form = PageForm(request.POST)
        if form.is_valid():
            if cat:
                page = form.save(commit=False)  # 关联其他表字段，则不能直接commit，后面进行关联
                page.category = cat
                page.views = 0
                page.save()
                print(page)
                return category(request, category_slug)
        else:
            print(form.errors)
            # 如果到了这里，则form对象中有数据，在下面return后，页面表单就会出现form对象中的数据
    else:
        form = PageForm()
    context_dict = {'form': form, 'category': cat}
    return render(request, 'rango/add_page.html', context_dict)


def about(request):
    visits = request.session.get('visits')
    if not visits:
        visits = 0
    return render(request, 'rango/about.html', {'visits': visits})


def register(request):
    registered = False

    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)  # set_password方法 对密码进行hash
            user.save()

            user_profile = profile_form.save(commit=False)
            user_profile.user = user
            if 'picture' in request.FILES:  # 检查文件是否上传成功
                user_profile.picture = request.FILES['picture']
            user_profile.save()
            registered = True
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(request, 'rango/register.html',
                  {'user_form': user_form, 'profile_form': profile_form, 'registered': registered})


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)  # 将登陆信息放入session中吗？
                next_url = request.POST.get('next', '/rango/')
                return HttpResponseRedirect(next_url)
            else:
                return HttpResponse('Your Rango account is disabled.')
        else:
            login_error = {'login_error': 'username or password is incorrect!'}
            return render(request, 'rango/login.html', login_error)
    else:
        next_url = request.GET.get('next', '/rango/')
        context_dict = {'next': next_url}
        return render(request, 'rango/login.html', context_dict)


@login_required
def restricted(request):
    return render(request, 'rango/restricted.html', {})


@login_required
def user_logout(request):
    logout(request)
    return index(request)


def track_url(request):
    if request.method == 'GET':
        if 'page_id' in request.GET:
            page_id = request.GET['page_id']
            page = Page.objects.get(id=int(page_id))
            page.views += 1
            page_url = page.url
            page.save()

            # 这种方式如何实现在新标签页中打开链接----> 在a标签中使用 target='_blank'
            return HttpResponseRedirect(page_url)
    return index(request)


@login_required
def profile(request):
    user = request.user
    user_profile = UserProfile.objects.filter(user=user).first()
    context_dict = {'user_profile': user_profile}
    return render(request, 'rango/profile.html', context_dict)


@login_required
def like_category(request):
    # 接收category_id 数据的GET请求，增加一个category的likes数据，并将likes数据返回
    cat_id = None
    if request.method == 'GET':
        cat_id = request.GET['category_id']

    likes = 0
    if cat_id:
        cat = Category.objects.get(id=int(cat_id))
        if cat:
            likes = cat.likes + 1
            cat.likes = likes
            cat.save()
    print(likes)
    return HttpResponse(likes)


def get_category_list(max_results=0, starts_with=''):
    # 查找category对象，通过匹配name字段与starts_with参数来进行过滤，返回category对象列表
    cat_list = []
    if starts_with:
        cat_list = Category.objects.filter(name__startswith=starts_with).order_by('-likes')

    if len(cat_list) > max_results > 0:
        cat_list = cat_list[:max_results]

    return cat_list


def suggest_category(request):
    # 获取请求的context，便于将context
    # 用于与 render_to_response 配合使用
    context = RequestContext(request)

    cat_list = []
    starts_with = ''
    if request.method == 'GET' and 'suggestion' in request.GET:
        starts_with = request.GET['suggestion']
    elif 'suggestion' in request.POST:
        starts_with = request.POST['suggestion']

    cat_list = get_category_list(max_results=5, starts_with=starts_with)

    return render_to_response('rango/cats.html', {'cats': cat_list}, context)


@login_required
def auto_addpage(request):
    context = RequestContext(request)
    if request.method == "GET":
        cat_id = request.GET['category_id'].strip()
        title = request.GET['title'].strip()
        url = request.GET['url'].strip()
        if url:
            if not (url.startswith("https://") or url.startswith("http://")):
                url = 'http://' + url

        cat = Category.objects.get(id=int(cat_id))
        Page.objects.get_or_create(category=cat, title=title, url=url)
        pages = Page.objects.filter(category=cat).order_by('-views')
        return render_to_response('rango/page_list.html', {'pages': pages}, context)
    return HttpResponse("error")
