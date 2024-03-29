from django.forms import ModelForm
from .models import Post,Image

class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content']

class ImageForm(ModelForm):
    class Meta:
        model = Image
        fields = ['image']