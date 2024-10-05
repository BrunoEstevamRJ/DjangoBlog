# no momento meu views.py esta assim

from django.shortcuts import render, get_object_or_404
from .models import Post
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic


# Create your views here.

def home(request):
    all_posts = Post.newmanager.all()

    return render(request, 'index.html', {'posts': all_posts})


def post_single(request, post):
    post = get_object_or_404(Post, slug=post, status='published')

    return render(request, 'single.html', {'post': post})

# View de signup
class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    sucess_url = reverse_lazy('blog:login') # Após o signup, redireciona para a página de login
    template_name = 'registration/signup.html'


