from django.forms import ModelForm
from .models import Post,Image,Comment

class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content']

class ImageForm(ModelForm):
    class Meta:
        model = Image
        fields = ['image']

class CommentCreateForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['content']