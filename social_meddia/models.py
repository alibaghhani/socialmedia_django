from django.db import models
from django.template.defaultfilters import slugify
from authentication.models import User

class Follow(models.Model):
    follower = models.ForeignKey(User, related_name='follower', on_delete=models.CASCADE)
    following = models.ForeignKey(User, related_name='following', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class Post(models.Model):
    title = models.CharField(max_length=250)
    content = models.CharField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    like = models.ManyToManyField(User,related_name='post_like')
    def get_like_count(self):
        return self.like.count()
    # def get_dislike_count(self):
    #     return self.posts_like.filter(like=False)



def get_image_filename(instance,filename):
    title = instance.post.title
    slug = slugify(title)
    return "post_images/%s-%s" % (slug, filename)


def get_profile_picture_filename(instance,filename):
    title = instance.user.username
    slug = slugify(title)
    return "user_profile/%s-%s" % (slug, filename)

#
# class Like(models.Model):
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')
#     post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name='posts_like',null=True)
#     like = models.BooleanField(null=True,unique=True)





class Comment(models.Model):
    content = models.TextField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE, related_name='comments')
    post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name='comment_post')
    reply = models.ForeignKey('self',on_delete=models.CASCADE,related_name='reply_comment',blank=True,null=True)
    is_replied = models.BooleanField(default=False)
    def __str__(self):
        return f'{self.user}-{self.content}'

class Image(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name='post_image')
    image = models.ImageField(upload_to=get_image_filename, default=None, null=True, blank=True)
    created_time = models.DateTimeField(auto_now_add=True, blank=True,null=True)
    update_time = models.DateTimeField(auto_now=True, blank=True,null=True)

class UserProfilePicture(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE, related_name='user_profile')
    profile_picture = models.ImageField(upload_to=get_profile_picture_filename,null=True,blank=True)


