from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from blog.models import Post




# profile page
@login_required
def profile(request, username):
    profile_user = get_object_or_404(User, username=username)
    posts = Post.objects.filter(author=profile_user, status="published")
    return render(request, "accounts/profile.html", {"profile_user": profile_user, "posts": posts})

# Edit Profile  page
@login_required
def edit_profile(request):
    return render(request, 'accounts/edit_profile.html')


