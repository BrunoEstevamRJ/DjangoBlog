from django.views.generic import CreateView
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from .models import Post
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
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
    success_url = reverse_lazy('login') # Após o signup, redireciona para a página de login
    template_name = 'registration/signup.html'


@login_required
def profile(request):
    return render(request, 'registration/profile.html',{'user':request.user})

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = UserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')  # Redireciona para o perfil após a edição
    else:
        form = UserChangeForm(instance=request.user)
    return render(request, 'registration/edit_profile.html', {'form': form})


@login_required
def user_posts(request):
    posts = Post.objects.filter(author=request.user,status='published')
    return render(request, 'blog/user_posts.html', {'posts':posts})


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'excerpt', 'content', 'status']  # Campos do modelo que deseja exibir no formulário
    template_name = 'blog/create_post.html'
    success_url = reverse_lazy('blog:homepage')

    def form_valid(self, form):
        form.instance.author = self.request.user  # Define o autor como o usuário logado
        return super().form_valid(form)
