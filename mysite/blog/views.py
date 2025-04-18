from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import logout
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.views.generic import DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from .models import Post, Comment
from .forms import PostForm, CommentForm

from django.db.models import Count


# Página inicial com todos os posts publicados
def home(request):
    all_posts = Post.objects.filter(status='published').order_by('-publish')
    return render(request, 'index.html', {'posts': all_posts})
    

# Página de detalhes de um post
def post_single(request, post_slug):
    post = get_object_or_404(Post, slug=post_slug)
    comments = post.comments.filter(parent__isnull=True).prefetch_related('replies')
    return render(request, 'blog/post_single.html', {'post': post, 'comments': comments})


# View de cadastro de usuário (signup)
class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'


 


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
    posts_drafts = Post.objects.filter(author=request.user, status='draft')

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


# Editar postagem
@login_required
def edit_post(request, post_slug):
    post = get_object_or_404(Post, slug=post_slug, author=request.user)

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, "Postagem atualizada com sucesso!")            
            return redirect('blog:post_single', post_slug=post.slug)
    else:
        form = PostForm(instance=post)

    return render(request, 'blog/edit_post.html', {'form': form, 'post': post})    




# Like na Postagem
@login_required
def like_post(request, post_slug):
    post = get_object_or_404(Post, slug=post_slug)
    if request.user in post.dislikes.all():
        post.dislikes.remove(request.user)
    if request.user in post.likes.all():
        post.likes.remove(request.user)
        liked = False
    else:
        post.likes.add(request.user)
        liked = True
    return JsonResponse({
        'liked': liked,
        'total_likes': post.total_likes(),
        'total_dislikes': post.total_dislikes()
    })


# Deslike na Postagem
@login_required
def dislike_post(request, post_slug):
    post = get_object_or_404(Post, slug=post_slug)
    if request.user in post.likes.all():
        post.likes.remove(request.user)
    if request.user in post.dislikes.all():
        post.dislikes.remove(request.user)
        disliked = False
    else:
        post.dislikes.add(request.user)
        disliked = True
    return JsonResponse({
        'disliked': disliked,
        'total_likes': post.total_likes(),
        'total_dislikes': post.total_dislikes()
    })


# Comment
def add_comment(request, post_slug, parent_id=None):
    post = get_object_or_404(Post, slug=post_slug)
    parent_comment = None

    if parent_id:
        parent_comment = get_object_or_404(Comment, id=parent_id)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.parent = parent_comment
            comment.save()
            return redirect('blog:post_single', post_slug=post_slug)

    return redirect('blog:post_single', post_slug=post_slug)


""" Deletar Comenntarios """
@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)

    if request.user == comment.author:
        comment.delete()        
        return JsonResponse({'success': True})
    
    return JsonResponse({'success': False, 'error': 'Você não tem permissão para apagar este comentário.'})


""" Deletar postagem """
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = "blog/post_confirm_delete.html"
    success_url = reverse_lazy("blog:user_posts")


    def test_func(self):
        """Garante que apenas o autor pode deletar a postagem"""
        post = self.get_object()
        return self.request.user == post.author
    

"""
class DeleteCommnet(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    temmplate_name = '/'
    success_url = reverse_lazy('blog:user_posts')

    def
"""