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
