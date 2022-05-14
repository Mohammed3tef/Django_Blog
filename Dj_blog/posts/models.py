from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import User
from django.db.models.signals import pre_save, post_delete
from django.dispatch import receiver
from django.template.defaultfilters import slugify
# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=30)
    user = models.ManyToManyField(
        User, blank=True, null=True, related_name='categories')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"


class Tag(models.Model):
    name = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.name


class Post(models.Model):
    STATUS_CHOICIS = (
        ('draft', 'Draft'),
        ('published', 'published'),
    )
    title = models.CharField(max_length=50, null=False, blank=False)
    body = models.TextField()
    tags = models.ManyToManyField('Tag', blank=True,)
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(
        upload_to='media', null=True, blank=True, default='image_1.jpg')
    date_published = models.DateTimeField(
        auto_now_add=True, verbose_name="date published")
    date_updated = models.DateTimeField(
        auto_now=True, verbose_name="date updated")
    slug_url = models.SlugField(blank=True, unique=True)
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICIS, default='published')
    likes = models.ManyToManyField(User, related_name="post_likes", blank=True)
    dislikes = models.ManyToManyField(
        User, related_name="post_dislikes", blank=True)
    restrict_comment = models.BooleanField(default=False)

    def snippet(self):
        return self.body[:50]+"..."

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('-date_published',)

    def get_absolute_url(self):
        return reverse('posts:post_detail', args=[self.id])


# to show the image in the post


    @property
    def image_url(self):
        if self.image and hasattr(self.image, 'url'):
            return self.image.url


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reply = models.ForeignKey('Comment', null=True,
                              related_name="replies", on_delete=models.CASCADE)
    content = models.TextField(max_length=300)
    approved = models.BooleanField(default=False)
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{} commented on {}.'.format(str(self.user.username), self.post.title)

    def get_delete_url(self):
        return reverse('posts:delete', args=[self.id])

    def filtered_content(self):
        profane_words = Profanity.objects.all()
        for profane_word in profane_words:
            self.content = self.content.replace(
                str(profane_word), '*' * len(str(profane_word)))
        return self.content


class Profanity(models.Model):
    profane_word = models.CharField(max_length=50)

    def __str__(self):
        return self.profane_word

# delete img from file media within the post


@receiver(post_delete, sender=Post)
def submission_delete(sender, instance, **kwargs):
    instance.image.delete(False)

# slug concat username with post title to be more readable in url & to be unique


def pre_save_post_receiver(sender, instance, *args, **kwargs):
    if not instance.slug_url:
        instance.slug_url = slugify(instance.user.username+"_"+instance.title)


pre_save.connect(pre_save_post_receiver, sender=Post)
