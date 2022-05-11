from django.urls import path
from posts import views

urlpatterns = [
    path('', views.posts),
    path('createpost', views.post_create),
    path('updatepost/<id>', views.post_update),
    path('delpost/<num>', views.post_delete),
    path('dislike_post/<id>', views.dislike_post, name="dislike_post"),
    path('tag/<tag_id>', views.tagPosts),

    path('delpost/<num>', views.post_delete),
    path('post/<int:id>', views.post_detail),
    path('category/<cat_id>', views.categoryPosts),
    path('editcomment/<int:id>/', views.commentEdit, name='commentEdit'),
]
