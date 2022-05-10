from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .models import Post, Tag, Category, Comment, Profanity
from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from posts.forms import PostForm, CommentForm
from users.util_funcs import delete_profile_pic
from users.logger import log
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

#create
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
