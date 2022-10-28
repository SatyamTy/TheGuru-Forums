from msilib.schema import Condition
from django.shortcuts import redirect, render, get_object_or_404
from .models import Author, Category, Post, Comment, Reply, id_info
from .utils import update_views
from .forms import PostForm,id_form
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

def home(request):
    forums = Category.objects.all()
    num_posts = Post.objects.all().count()
    num_users = User.objects.all().count()
    num_categories = forums.count()
    try:
        last_post = Post.objects.latest("date")
    except:
        last_post = []

    context = {
        "forums":forums,
        "num_posts":num_posts,
        "num_users":num_users,
        "num_categories":num_categories,
        "last_post":last_post,
        "title": "The Guru Forums"
    }
    return render(request, "home.html", context)

def detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    try: 
        author = Author.objects.get(user=request.user)
    except:
        author = '1'
    
    if "comment-form" in request.POST:
        comment = request.POST.get("comment")
        new_comment, created = Comment.objects.get_or_create(user=author, content=comment)
        post.comments.add(new_comment.id)

    if "reply-form" in request.POST:
        reply = request.POST.get("reply")
        commenr_id = request.POST.get("comment-id")
        comment_obj = Comment.objects.get(id=commenr_id)
        new_reply, created = Reply.objects.get_or_create(user=author, content=reply)
        comment_obj.replies.add(new_reply.id)


    context = {
        "author":author,
        "authors":Author.objects.all(),
        "post":post,
        "title": post.title,
    }
    update_views(request, post)

    return render(request, "detail.html", context)

def posts(request, slug):
    category = get_object_or_404(Category, slug=slug)
    posts = Post.objects.filter(approved=True, category=category)
    paginator = Paginator(posts, 5)
    page = request.GET.get("page")
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages) 

    context = {
        "posts":posts,
        "forum": category,
        "title": category.title,
    }

    return render(request, "posts.html", context)


@login_required
def create_post(request):
    context = {}
    form = PostForm(request.POST or None)
    try: 
        author = Author.objects.get(user=request.user)
    except:
        author = '1'
    if request.method == "POST":
        if form.is_valid():
            print("\n\n its valid")
            author = Author.objects.get(user=request.user)
            new_post = form.save(commit=False)
            new_post.user = author
            new_post.save()
            form.save_m2m()
            return redirect("home")
    context.update({
        "form": form,
        "title": "Create New Post",
        "author": author,
        "authors": Author.objects.all(), 
    })
    return render(request, "create_post.html", context)

@login_required
def create_id(request):
    context = {}
    try:
        id = id_info.objects.get(user=request.user)
        id_all = id_info.objects.all()
    except:
        id="1"
        id_all="2"

    if id in id_all:
        form = id_form(request.POST, request.FILES, instance=id)

    else:
        form = id_form(request.POST, request.FILES)


    if request.method == "POST":
            new_id = form.save(commit=False)
            new_id.user = request.user
            if new_id.pic == None:
                new_id.pic= "id-pics/default.png"
            new_id.save()
            return redirect("id")
    context.update({
        "title": "Generate Your ID",
        'form': id_form(),
    })
    return render(request, "id_form.html", context)

@login_required
def id(request):
    context = {}
    try: 
        author = id_info.objects.get(user=request.user)
    except:
        author = ''
    if author == '':
        return redirect('create_id')
    context.update({
        "title": "Your ID",
        'form': id_form(),
        "info": author,
    })
    return render(request, "id.html", context)

def latest_posts(request):
    posts = Post.objects.all().filter(approved=True)[:10]
    context = {
        "posts":posts,
        "title": "Latest 10 Posts"
    }

    return render(request, "latest-posts.html", context)

def search_result(request):

    return render(request, "search.html")

def about_site(request):

    return render(request, "about.html")

