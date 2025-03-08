import random
import string

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.text import slugify


class Post(models.Model):
    class NewManager(models.Manager):
        def get_queryset(self):
            return super().get_queryset().filter(status='published')

    options = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )

    title = models.CharField(max_length=255)
    excerpt = models.TextField(null=True)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    publish = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    content = models.TextField()
    status = models.CharField(max_length=10, choices=options, default='draft')
    objects = models.Manager()
    newmanager = NewManager()
    likes = models.ManyToManyField(User, related_name='post_likes', blank=True)
    dislikes = models.ManyToManyField(User, related_name='post_dislikes', blank=True)
    image = models.ImageField(upload_to='post_images/', blank=True, null=True)

    def total_likes(self):
        return self.likes.count()

    def total_dislikes(self):
        return self.dislikes.count()

    def generate_unique_slug(self):
        """Gera um slug único, adicionando números aleatórios se necessário."""
        base_slug = slugify(self.title)
        unique_slug = base_slug

        while Post.objects.filter(slug=unique_slug).exists():
            random_number = ''.join(random.choices(string.digits, k=4))  # Gera um número aleatório de 4 dígitos
            unique_slug = f"{base_slug}-{random_number}"

        return unique_slug

  


    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.generate_unique_slug()

        self.content = self.content.replace("\r\n", "\n")  # Força quebra de linha

        super().save(*args, **kwargs)


    def get_absolute_url(self):
        return reverse('blog:post_single', args=[self.slug])

    class Meta:
        ordering = ('-publish',)

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comentário de {self.author} em {self.post.title}'
