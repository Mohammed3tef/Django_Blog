from django.db import models

# Create your models here.


class Post(models.Model):
    STATUS_CHOICIS=(
        ('draft','Draft'),
        ('published','published'),    
    )
    title = models.CharField(max_length=50 , null= False , blank = False)
    body = models.TextField()
    tags = models.ManyToManyField('Tag', blank=True,)
    category = models.ForeignKey(Category, on_delete = models.DO_NOTHING)
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    image = models.ImageField(upload_to='../media',null=True , blank = True)
    date_published=models.DateTimeField(auto_now_add=True,verbose_name="date published")
    date_updated=models.DateTimeField(auto_now =True,verbose_name="date updated")
    slug_url = models.SlugField(blank=True,unique=True)
    status=models.CharField(max_length=10,choices=STATUS_CHOICIS,default='published')
    likes = models.ManyToManyField(User,related_name="post_likes",blank=True)
    dislikes= models.ManyToManyField(User,related_name="post_dislikes",blank=True)
    restrict_comment = models.BooleanField(default=False)
    def snippet(self):
        return self.body[:50]+"..."

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('-date_published',)

    def get_absolute_url(self):
        return reverse('posts:post_detail', args=[self.id])
