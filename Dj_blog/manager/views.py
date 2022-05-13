from django.shortcuts import render
from .crud_users import *
from posts.models import Post, Tag, Category, Comment, Profanity
from posts.forms import PostForm, CommentForm, ProfanityForm, CategoryForm

# the following views are to control users and admins 
def users(request):
    return manager_show_normal_users(request)

def lock(request, id):
    return manager_lock_user(request, id)


def unlock(request, id):
    return manager_unlock_user(request, id)

def delete(request, id):
    return manager_delete_user(request, id)

def show(request, id):
    return manager_show_user(request, id)

def promote(request, id):
    return manager_promote_user(request, id)

def admins(request):
    return manager_show_admins(request)

def demote(request, id):
    return super_demote_admin(request, id)

def lock_admin(request, id):
    return super_lock_admin(request, id)

def unlock_admin(request, id):
    return super_unlock_admin(request, id)

def delete_admin(request, id):
    return super_delete_admin(request, id)

def promote_admin_to_super(request, id):
    return super_promote_admin(request, id)

def sort(request, num):
    return admin_sort(request, num)

def dash(request):
    """ Main admin dashboard and redirect normal users to homepage in case they wrote the url manually"""
    if(is_authorized_admin(request)):
        posts_count = len(Post.objects.all())
        admins_count = len(User.objects.filter(is_staff__exact=True))
        normal_count = len(User.objects.filter(is_staff__exact=False))
        return render(request, "manager/index.html", {"posts": posts_count, "admins": admins_count, "users": normal_count})
    else:
        return HttpResponseRedirect("/")

def add_category(request):
    if(is_authorized_admin(request)):
        form = CategoryForm()
        if request.method == 'POST':
            form = CategoryForm(request.POST)
            if form.is_valid():
                form.save()
                log("form is valid")
                return HttpResponseRedirect('/manager/posts#categories')
        else:
            context = {"pt_form": form}
            return render(request, "manager/categoryform.html", context)
    else:
        return HttpResponseRedirect("/")

def delete_category(request, cat_id):
    if(is_authorized_admin(request)):
        category = Category.objects.get(id=cat_id)
        category.delete()
        return HttpResponseRedirect('/manage/posts#categories')
    else:
        return HttpResponseRedirect("/")

def posts(request):
    if(is_authorized_admin(request)):
        posts = Post.objects.all()
        categories = Category.objects.all()
        profane_words = Profanity.objects.all()
        context = {'posts': posts, 'categories': categories,
                   'profane_words': profane_words}
        return render(request, 'manager/landing.html', context)
    else:
        return HttpResponseRedirect("/")

def post_delete(request, post_id):
    if(is_authorized_admin(request)):
        post = Post.objects.get(id=post_id)
        post.delete()
        return HttpResponseRedirect('/manager/posts')
    else:
        return HttpResponseRedirect("/")



def add_profane_word(request):
    if(is_authorized_admin(request)):
        form = ProfanityForm()
        if request.method == 'POST':
            form = ProfanityForm(request.POST)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect('/manager/posts#forbidden')
        else:
            context = {"pt_form": form}
            return render(request, "manager/form.html", context)
    else:
        return HttpResponseRedirect("/")


def delete_profane_word(request, id):
    if(is_authorized_admin(is_authorized_admin(request))):
        profane_word = Profanity.objects.get(id=id)
        profane_word.delete()
        return HttpResponseRedirect('/manager/posts#forbidden')
    else:
        return HttpResponseRedirect("/")
