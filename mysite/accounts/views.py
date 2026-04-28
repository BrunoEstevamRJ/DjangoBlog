from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib.auth.models import User
from blog.models import Post
from .forms import ProfileForm



'''==[ Profile Page ]=='''
def profile(request, username):
    profile_user = get_object_or_404(User, username=username)
    posts = Post.objects.filter(author=profile_user).order_by('-publish')
    is_following = False

    if request.user.is_authenticated and request.user != profile_user:
        is_following = profile_user.profile in request.user.profile.following.all()

    return render(request, "accounts/profile.html", {
        "profile_user": profile_user,
        "posts": posts,
        "is_following": is_following,
    })

'''==[ Editar Perfil ]=='''
@login_required
def edit_profile(request):
    profile = request.user.profile
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('accounts:profile', username=request.user.username)

    else:
        form = ProfileForm(instance=profile)
    return render(request, 'accounts/edit_profile.html', {'form': form})


@login_required
@require_POST
def toggle_follow(request, username):
    target_user = get_object_or_404(User, username=username)

    if target_user == request.user:
        return redirect('accounts:profile', username=target_user.username)

    my_profile = request.user.profile
    target_profile = target_user.profile

    if target_profile in my_profile.following.all():
        my_profile.following.remove(target_profile)
    else:
        my_profile.following.add(target_profile)

    return redirect('accounts:profile', username=target_user.username)
