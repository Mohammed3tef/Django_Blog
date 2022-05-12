from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .models import Post, Tag, Category, Comment, Profanity
from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from posts.forms import PostForm, CommentForm
from users.util_funcs import delete_profile_pic
from django.core.mail import send_mail

# Create your views here.


def posts(request):
    posts = Post.objects.all()
    popular_posts = Post.objects.order_by('-likes')[:5]
    paginator = Paginator(posts, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    categotries = Category.objects.all()
    tags = Tag.objects.all()[:10]
    user = request.user

    context = {'page_obj': page_obj, 'categories': categotries,
               'tags': tags, 'user': user, 'popular_posts': popular_posts}
    return render(request, 'home.html', context)

# create


def post_create(request):
    form = PostForm()
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            tag_list = getTags(request.POST.get('post_tags'))
            post.save()
            queryset = Tag.objects.filter(name__in=tag_list)
            post.tags.set(queryset)
            return HttpResponseRedirect('/')
    else:
        context = {"pt_form": form}
        return render(request, "post_form.html", context)


def getTags(string):
    tag_list = list(string.split(" "))
    for tag in tag_list:
        if not Tag.objects.filter(name=tag):
            Tag.objects.create(name=tag)
    return tag_list

# update


def post_update(request, id):
    post = get_object_or_404(Post, id=id)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            img = request.FILES.get('image')
            if (img):
                if(post.image):
                    delete_profile_pic(post.image)
                post.image = img
            post.user = request.user
            tag_list = getTags(request.POST.get('post_tags'))
            post.save()
            queryset = Tag.objects.filter(name__in=tag_list)
            post.tags.set(queryset)
            return HttpResponseRedirect('/')
    else:
        form = PostForm(instance=post)
        context = {"pt_form": form}
        return render(request, "post_form.html", context)

# delete


def post_delete(request, num):
    instance = Post.objects.get(id=num)
    instance.delete()
    return HttpResponseRedirect('/')


# to like the post if the user is not in like or dislike tables it will be added one like
# if the user in one of the tables he must pressed one more time in the same button


def like_post(request, id):
    post = get_object_or_404(Post, pk=id)
    postIsDisliked = post.dislikes.all()
    post_isliked = post.likes.all()
    user = request.user
    if (user not in post_isliked):
        if(user not in postIsDisliked):
            post.likes.add(user)
            post.save()
    else:
        post.likes.remove(user)
        post.save()
    return HttpResponseRedirect("/post/"+id)


# to dislike the post if the user is not in like or dislike tables it will be added one dislike
# if the user in one of the tables he must pressed one more time in the same button


def dislike_post(request, id):
    post = get_object_or_404(Post, pk=id)
    postIsDisliked = post.dislikes.all()
    post_isliked = post.likes.all()
    user = request.user
    if (user not in postIsDisliked):
        if(user not in post_isliked):
            post.dislikes.add(user)
            post.save()
    else:
        post.dislikes.remove(user)
        post.save()

    total = post.dislikes.count()
    if(total == 10):
        post.delete()
        return HttpResponse("<h1> this post has been deleted </h1>")
    return HttpResponseRedirect("/post/"+id)


def tagPosts(request, tag_id):
    tag = Tag.objects.get(id=tag_id)
    posts = tag.post_set.all()
    paginator = Paginator(posts, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    categotries = Category.objects.all()
    tags = Tag.objects.all()[:10]
    user = request.user
    context = {'page_obj': page_obj,
               'categories': categotries, 'tags': tags, 'user': user}
    return render(request, 'home.html', context)


def categoryPosts(request, cat_id):
    category = Category.objects.get(id=cat_id)
    posts = Post.objects.filter(category=category)
    paginator = Paginator(posts, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    categotries = Category.objects.all()
    tags = Tag.objects.all()[:10]
    user = request.user
    context = {'page_obj': page_obj,
               'categories': categotries, 'tags': tags, 'user': user}
    return render(request, 'home.html', context)


def search(request):
    query = request.GET.get('q')
    posts = Post.objects.filter(Q(title__icontains=query))
    paginator = Paginator(posts, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    categotries = Category.objects.all()
    tags = Tag.objects.filter(Q(name__icontains=query))[:10]
    user = request.user
    context = {'page_obj': page_obj,
               'categories': categotries, 'tags': tags, 'user': user}
    return render(request, 'home.html', context)


def post_detail(request, id):
    categotries = Category.objects.all()
    tags = Tag.objects.all()[:10]
    post = Post.objects.get(id=id)
    user = request.user
    comments = Comment.objects.filter(post=post, reply=None).order_by('-id')

    if request.method == 'POST':
        comment_form = CommentForm(request.POST or None)
        if comment_form.is_valid():
            content = request.POST.get('content')
            reply_id = request.POST.get('comment_id')
            comment_qs = None
            if reply_id:
                comment_qs = Comment.objects.get(id=reply_id)

            Comment.objects.create(
                post=post, user=request.user, content=content, reply=comment_qs)
            comment_form = CommentForm()

    else:
        comment_form = CommentForm()
    context = {
        'post': post,
        'comments': comments,
        'comment_form': comment_form,
        'categories': categotries,
        'tags': tags,
        'user': user
    }
    return render(request, 'single.html', context)


def commentEdit(request, id):
    comment = Comment.objects.get(id=id)
    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment.user)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('deletecomment')
    else:
        form = CommentForm(instance=comment)
    return render(request, 'post_detail.html', {'form': form})


def subscribe(request, cat_id):
    user = request.user
    category = Category.objects.get(id=cat_id)
    category.user.add(user)
    # send email to user after subscription
    try:
        send_mail("subscribed to a new category", 'hello ,'+user.first_name+" "+user.last_name+'\nyou have just subscribed to category '+category.name,
                  'dproject.os40@gmail.com', [user.email], fail_silently=False,)
    except Exception as ex:
        log("couldn't send email message"+str(ex))
    return HttpResponseRedirect('/')


def unsubscribe(request, cat_id):
    user = request.user
    category = Category.objects.get(id=cat_id)
    category.user.remove(user)
    return HttpResponseRedirect('/')
