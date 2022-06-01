from django import forms
from .models import Post, Comment, Profanity, Category

class PostForm(forms.ModelForm):
	class Meta:
		model = Post
		fields=('title','body','image','status', 'category', 'restrict_comment')
		widgets = {
			'title': forms.TextInput(attrs={'class': 'form-control'}),
			'body': forms.Textarea(attrs={'class': 'form-control'}),
			'image': forms.FileInput(attrs={'class': 'form-control-file'}),
			'status': forms.Select(attrs={'class': 'custom-select'}),
			'category': forms.Select(attrs={'class': 'custom-select'}),
		}

class CommentForm(forms.ModelForm):
	content = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'reply'}))
	class Meta:
		model = Comment
		fields = ('content',)

class ProfanityForm(forms.ModelForm):
	profane_word = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control',}))
	class Meta:
		model = Profanity
		fields = ('profane_word',)
		
class CategoryForm(forms.ModelForm):
	name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control',}))
	class Meta:
		model = Category
		fields = ('name',)