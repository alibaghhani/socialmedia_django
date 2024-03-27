from django.forms import ModelForm
from .models import Post

class UploadPostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'image']