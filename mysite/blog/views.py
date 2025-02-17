from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib import messages

from .models import Post
from .forms import PostForm


# Página inicial com todos os posts publicados
def home(request):
    all_posts = Post.objects.filter(status='published').order_by('-publish')
    return render(request, 'index.html', {'posts': all_posts})


# Página de detalhes de um post
def post_single(request, post):
    post = get_object_or_404(Post, slug=post, status='published')
    return render(request, 'single.html', {'post': post})


# View de cadastro de usuário (signup)
class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'


# Página de perfil do usuário logado
@login_required
def profile(request):
    return render(request, 'registration/profile.html', {'user': request.user})


# Edição de perfil do usuário logado
@login_required
def edit_post(request, post_slug):
    post = get_object_or_404(Post, slug=post_slug)

    if post.author != request.user:
        messages.error(request, "Você não tem permissão para editar este post.")
        return redirect("blog:user_posts")

    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, "Postagem atualizada com sucesso!")
            return redirect('blog:post_single', post_slug=post.slug)

    else:
        form = PostForm(instance=post)

    return render(request, 'blog/edit_post.html', {'form': form, 'post': post})


# Listar posts do usuário logado
@login_required
def user_posts(request):
    posts_published = Post.objects.filter(author=request.user, status='published')
    posts_drafts = Post.objects.filter(author=request.user, status='draft')  # Se houver rascunhos

    return render(request, 'blog/user_posts.html', {
        'posts_published': posts_published,
        'posts_drafts': posts_drafts
    })



# Criar um novo post
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/create_post.html'
    success_url = reverse_lazy('blog:homepage')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


@login_required
def edit_post(request, post_slug):
    post = get_object_or_404(Post, slug=post_slug, author=request.user)

    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, "Postagem atualizada com sucesso!")
            return redirect('blog:post_single', post_slug=post.slug)
    else:
        form = PostForm(instance=post)

    return render(request, 'blog/edit_post.html', {'form': form, 'post': post})



@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = UserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Perfil atualizado com sucesso!")
            return redirect('blog:profile')
    else:
        form = UserChangeForm(instance=request.user)
    return render(request, 'registration/edit_profile.html', {'form': form})
