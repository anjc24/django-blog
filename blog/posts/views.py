from django.db.models import Q
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import *
from django.contrib.auth import login, logout, authenticate
from datetime import date
from django.core.paginator import Paginator

# Create your views here.
def All_category():
    all_cat = Category.objects.all()
    li = []
    for i in all_cat:
        c = Post.objects.filter(category=i).count()
        li.append(c)
    z = zip(all_cat, li)
    return z


def tags():
    tags = Tag.objects.all()
    return tags


def recent_and_popular():
    allpost = Post.objects.all()

    recent_three = allpost[::-1][:3]
    popular_five = Post.objects.order_by('-likecount')[:4]
    return recent_three, popular_five


def Index(request):
    data = None
    if request.user.is_authenticated :
        data = User_Details.objects.filter(usr=request.user).first()
    post_data = Post.objects.all().order_by('-publishing_date')
    pg = Paginator(post_data, 5)
    page_number = request.GET.get('page')
    page_obj = pg.get_page(page_number)
    recent, popular = recent_and_popular()
    p = {"allcat": All_category(), 'listcat': All_category() ,'pg': pg ,'post': page_obj, "tags": tags(), "userdetail": data, "recent":recent, "popular":popular, "pg":pg}
    return render(request, 'posts/index.html', p)



def Register(request):
    already = False
    perror = False
    succ = False

    if request.method == 'POST':
        re = request.POST

        uname = re['username']
        fname = re['fname']
        lname = re['lname']
        p1 = re['p1']
        p2 = re['p2']
        if not request.FILES:
            pass
        else:
            img = request.FILES['img']

        data = User.objects.filter(username=uname)

        if p1 != p2:
            perror = True
        else:
            if data:
                already = True
            else:
                succ = True
                user = User.objects.create_user(username=uname, first_name=fname, last_name=lname, password=p1)
                usr = User_Details.objects.create(usr=user, image=img)
                login(request, user)
                return redirect('posts:Index')

    dic = {'already': already, 'succ': succ, 'pass': perror}
    return render(request, 'posts/register.html',dic)


def Login(request):
    error = False

    if request.method == 'POST':
        re = request.POST

        uname = re['username']
        p = re['p']

        user = authenticate(username=uname, password=p)
        if user:
            login(request, user)
            return redirect('posts:Index')
        else:
            error = True

    dic = {'error': error}
    return render(request, 'posts/login.html',dic)

def Logout(request):
    logout(request)
    return redirect('posts:login')

def detail(request, pid):
    post_data = Post.objects.get(id=pid)
    uid = post_data.User.id
    publisher = User.objects.get(id=uid)

    d =False
    if request.user.is_authenticated:
        data = LikeComment.objects.filter(usr=request.user, post_data=post_data).first()
    if request.user.is_authenticated and data:
        if data.like == True :
            d = True

    likecount = LikeComment.objects.filter(post_data=post_data, like=True).count()


    comments = Comment.objects.filter(post_data=post_data)

    previous = Post.objects.filter(id__lt=pid).order_by('id').first()
    next = Post.objects.filter(id__gt=pid).order_by('id').first()

    commentcount = Comment.objects.filter(post_data=post_data).count()
    p = {"allcat": All_category(), 'post': post_data, 'publisher':publisher, "tags": tags(), "like":d, "likecount":likecount, "commentcount":commentcount, "comments":comments ,"previous":previous, "next":next}

    if request.method == 'POST':
        re = request.POST

        name = re['name']
        email = re['email']
        content = re['content']
        td = date.today()

        l = Post.objects.get(id=pid)
        l.commentcount += 1
        l.save()
        comment = Comment.objects.create(post_data=post_data, name=name, email=email, content=content, publishing_date=td)
        return redirect('posts:detail', pid=pid)


    return render(request, 'posts/single-blog.html', p)

def category(request, cid):
    post_data = Post.objects.filter(category=cid).order_by('-publishing_date')
    pg = Paginator(post_data, 5)
    page_number = request.GET.get('page')
    page_obj = pg.get_page(page_number)
    cname = Category.objects.filter(id=cid).first().title
    p = {"allcat": All_category(), 'post':page_obj , 'pg':pg ,'category': cname, "tags": tags()}
    return render(request, 'posts/category.html', p)

def tag(request, tid):
    post_data = Post.objects.filter(tag=tid).order_by('-publishing_date')
    pg = Paginator(post_data, 5)
    page_number = request.GET.get('page')
    page_obj = pg.get_page(page_number)
    tname = Tag.objects.filter(id=tid).first().name
    p = {"allcat": All_category(), 'post': page_obj, 'pg': pg, 'tagname': tname, "tags": tags()}
    return render(request, 'posts/category.html', p)

def CreatePost(request):
    p = {"allcat": All_category()}

    if request.method == 'POST':
        re = request.POST

        title = re['title']
        content = re['content']
        tag = re['tag']
        cat = re['cat']
        img = request.FILES['img']

        tags = tag.split(",")
        cdata = Category.objects.get(id=cat)
        user = request.user
        td = date.today()

        for t in tags :
            texist = Tag.objects.filter(name=t).first()
            if not texist :
                Tag.objects.create(name=t)

        pid = Post.objects.create(category=cdata, User=user, title=title, content=content, image=img, publishing_date=td)

        for t in tags :
            tid = Tag.objects.filter(name=t).first().id
            Post.objects.get(title=pid).tag.add(tid)

        return redirect('posts:Index')

    return render(request, 'posts/createpost.html', p)


def SearchPost(request):
    query = request.GET.get("query")
    post_data =  Post.objects.filter(Q(title__icontains=query) |
                                   Q(content__icontains=query) |
                                   Q(tag__name__icontains=query)
                                  ).order_by('id').distinct()
    pg = Paginator(post_data, 4)
    page_number = request.GET.get('page')
    page_obj = pg.get_page(page_number)

    p = {"allcat": All_category(), 'post':page_obj , 'pg':pg , "tags": tags()}
    return render(request, 'posts/search.html',p)


def UpdateBlog(request, bid):
    blog = Post.objects.filter(id=bid).first()
    if request.method == "POST":
        dd = request.POST
        if dd['title'] == None:
            pass
        else:
            t = dd['title']
            blog.title = t
            blog.save()

        if dd['content'] == None:
            pass
        else:
            s = dd['content']
            blog.content = s
            blog.save()

        if not request.FILES:
            pass
        else:
            i = request.FILES['img']
            blog.image = i
            blog.save()

        cat = dd['cat']
        tag = dd['tag']
        tags = tag.split(",")
        cdata = Category.objects.get(id=cat)
        td = date.today()

        blog.category = cdata
        blog.publishing_date = td
        blog.save()

        for t in tags:
            texist = Tag.objects.filter(name=t).first()
            if not texist:
                Tag.objects.create(name=t)

        for t in tags :
            tid = Tag.objects.filter(name=t).first().id
            Post.objects.get(id=bid).tag.add(tid)

        return redirect('posts:Index')


    tags = blog.tag.all()
    s = ','.join([str(i) for i in tags])
    dic = {"allcat": All_category(), "blogdetails": blog, "tags" : s}
    return render(request, 'posts/updateblog.html', dic)

def DeleteBlog(request, bid) :
    blog = Post.objects.filter(id=bid).first()
    blog.delete()
    return redirect('posts:Index')


def LikePost(request, pid):
    if not request.user.is_authenticated:
        return redirect('posts:login')
    data = Post.objects.get(id = pid)
    data2 = LikeComment.objects.filter(usr=request.user, like=True, post_data=data)


    if not data2:
        LikeComment.objects.create(post_data=data, usr=request.user, like=True)
        l= Post.objects.get(id=pid)
        l.likecount+=1
        l.save()

        print(l)
        return redirect('posts:detail',pid= pid)
    else:
        return redirect('posts:detail',pid= pid)


def UpdateProfile(request):
    data = User_Details.objects.filter(usr=request.user).first()
    Userd = User.objects.get(username=request.user)

    if request.method == "POST":

        dd = request.POST
        if dd['uname'] == None:
            pass
        else:
            t = dd['uname']
            Userd.username = t
            Userd.save()

        if dd['fname'] == '':
            pass
        else:
            t = dd['fname']
            Userd.first_name = t
            Userd.save()

        if dd['lname'] == '':
            pass
        else:
            t = dd['lname']
            Userd.last_name = t
            Userd.save()

        if dd['email'] == '':
            pass
        else:
            t = dd['email']
            Userd.email = t
            Userd.save()

        if dd['phoneno'] == '':
            pass
        else:
            t = dd['phoneno']
            data.phone = t
            data.save()

        if dd['about'] == '':
            pass
        else:
            t = dd['about']
            data.about = t
            data.save()

        if not request.FILES :
            pass
        else:
            i = request.FILES['img']
            data.image = i
            data.save()

    d = {"allcat": All_category(), "userdata":data}
    return render(request, 'posts/profile.html', d)


def PasswordReset(request):
     error = False
     succ = False

     if request.method == 'POST':
        re = request.POST

        Uname = User.objects.get(username=request.user).username
        op = re['op']
        np = re['np']
        rnp = re['rnp']
        pmatch = False

        user = authenticate(username=Uname, password=op)
        if np == rnp:
            pmatch=True

        if user and pmatch:
            u = User.objects.get(username=request.user)
            u.set_password(np)
            u.save()
            succ = True
            user = authenticate(username=Uname, password=np)
            if user:
                login(request, user)
            return redirect('posts:reset_password')
        else:
            error = True

     dic = {'error': error, 'succ':succ}
     return render(request, 'posts/resetpass.html', dic)


def userposts(request, uid):
    user = User.objects.get(id = uid)
    post_data = Post.objects.filter(User = user).order_by('-publishing_date')
    print(post_data)
    pg = Paginator(post_data, 5)
    page_number = request.GET.get('page')
    page_obj = pg.get_page(page_number)
    p = {"allcat": All_category(), 'post':page_obj , 'pg':pg ,"tags": tags()}
    return render(request, 'posts/category.html', p)


def contact(request):
    return render(request, 'posts/contact.html')

def about(request):
    return render(request, 'posts/about.html')