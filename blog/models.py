from django.db import models
from django.utils import timezone
from django.urls import reverse
# Create your models here.
class Post(models.Model):
    #since we expect one use to have control over this blog such as updating.
    # So we are directly linking author to an authorization user(super user)
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    title = models.CharField(max_length=256)
    text = models.TextField()
    create_date = models.DateTimeField(default = timezone.now)
    published_date = models.DateTimeField(null=True)

    def publish(self):
        print("////////////////////////timezone "+ str(timezone.now()))
        self.published_date=timezone.now()
        print(self.__str__())
        self.save()
        print("saved")

    def approve_comments(self):
        return self.comments.filter(approved_comment=True)

    #after creation of post and publish it will lead to the post_detail of pk just created
    def get_absolute_url(self):
        return reverse("post_detail",kwargs={'pk':self.pk})

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey('blog.Post', related_name='comments',null=True,on_delete=models.SET_NULL)
    auther = models.CharField(max_length=150)
    text = models.TextField()
    create_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=False)

    def approve(self):
        self.approved_comment=True
        self.save()

    def get_absolute_url(self):
        return reverse('post_list')

    def __str__(self):
        return self.text
