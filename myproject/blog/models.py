from django.db import models
from django.utils import timezone
from django.utils.text import slugify as django_slugify
from time import time
from django.conf import settings


def get_slug(s):
    new_slug = django_slugify(s)
    return new_slug + '-' + str(int(time()))


class Post(models.Model):
    title = models.CharField(max_length=200, verbose_name="Заголовок")
    slug = models.SlugField(max_length=250, unique=True, blank=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='posts')
    body = models.TextField(verbose_name="Текст поста")
    image = models.ImageField(upload_to='post_images/', blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    def __str__(self):
        return self.title
    

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = get_slug(self.title)
        super().save(*args, **kwargs)


    class Meta:
        ordering = ['-created_date']
        verbose_name = "Пост"
        verbose_name_plural = "Посты"


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    body = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_date']

    def __str__(self):
        return f'Комментарий от {self.author} к посту "{self.post.title}"'