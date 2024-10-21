from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.views import generic
from django.views.generic import CreateView

from .models import Post


# Página inicial com todos os posts publicados
def home(request):
    all_posts = Post.newmanager.all()  # Usando o custom manager para pegar os posts publicados
    return render(request, 'index.html', {'posts': all_posts})


# Página de detalhes de um post
def post_single(request, post):
    post = get_object_or_404(Post, slug=post, status='published')  # Busca um post com o status 'published'
    return render(request, 'single.html', {'post': post})


# View de cadastro de usuário (signup)
class SignUpView(generic.CreateView):  # Certifique-se de herdar de generic.CreateView
    form_class = UserCreationForm
    success_url = reverse_lazy('login')  # Redireciona para login após o cadastro
    template_name = 'registration/signup.html'


# Página de perfil do usuário logado
@login_required
def profile(request):
    return render(request, 'registration/profile.html', {'user': request.user})


# Edição de perfil do usuário logado
@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = UserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')  # Redireciona para o perfil após salvar as alterações
    else:
        form = UserChangeForm(instance=request.user)
    return render(request, 'registration/edit_profile.html', {'form': form})


# Listar posts do usuário logado
@login_required
def user_posts(request):
    posts = Post.objects.filter(author=request.user, status='published')  # Busca posts do usuário logado
    return render(request, 'blog/user_posts.html', {'posts': posts})


# Criar um novo post
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'excerpt', 'content', 'status']  # Campos do formulário de criação do post
    template_name = 'blog/create_post.html'
    success_url = reverse_lazy('blog:homepage')  # Redireciona para a página inicial após criar o post

    def form_valid(self, form):
        form.instance.author = self.request.user  # Define o autor como o usuário logado
        return super().form_valid(form)
