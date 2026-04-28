from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.http import require_POST
from blog.models import Post
from .forms import ProfileForm


'''==[ Profile Page ]=='''
def profile(request, username):
    profile_user = get_object_or_404(User, username=username)
<<<<<<< HEAD
    posts = Post.objects.filter(author=profile_user).order_by('-publish')
=======
    posts = Post.objects.filter(author=profile_user, status='published').order_by('-publish')
>>>>>>> origin/main
    is_following = False

    if request.user.is_authenticated and request.user != profile_user:
        is_following = profile_user.profile in request.user.profile.following.all()

    return render(request, "accounts/profile.html", {
        "profile_user": profile_user,
        "posts": posts,
        "is_following": is_following,
    })


'''==[ Follow Lists ]=='''
def follow_list(request, username, relation):
    profile_user = get_object_or_404(User, username=username)
    can_unfollow = request.user.is_authenticated and request.user == profile_user

    if relation not in {"followers", "following"}:
        raise Http404("Tipo de lista invalido.")

    if relation == "followers":
        profiles = profile_user.profile.followers.select_related("user").order_by("user__username")
        page_title = f"Seguidores de {profile_user.username}"
        empty_message = "Este usuario ainda nao tem seguidores."
    else:
        profiles = profile_user.profile.following.select_related("user").order_by("user__username")
        page_title = f"{profile_user.username} esta seguindo"
        empty_message = "Este usuario ainda nao esta seguindo ninguem."

    return render(request, "accounts/follow_list.html", {
        "profile_user": profile_user,
        "profiles": profiles,
        "relation": relation,
        "can_unfollow": can_unfollow,
        "page_title": page_title,
        "empty_message": empty_message,
    })


def discover_people(request):
    query = request.GET.get("q", "").strip()
    users = User.objects.select_related("profile").order_by("username")
    following_ids = set()

    if request.user.is_authenticated:
        users = users.exclude(pk=request.user.pk)
        following_ids = set(
            request.user.profile.following.values_list("user_id", flat=True)
        )

    if query:
        users = users.filter(
            Q(username__icontains=query) |
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query)
        )

    return render(request, "accounts/discover_people.html", {
        "users": users,
        "query": query,
        "following_ids": following_ids,
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
<<<<<<< HEAD
=======
@require_POST
>>>>>>> origin/main
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

<<<<<<< HEAD
=======
    next_url = request.POST.get("next")
    if next_url and url_has_allowed_host_and_scheme(
        url=next_url,
        allowed_hosts={request.get_host()},
        require_https=request.is_secure(),
    ):
        return redirect(next_url)

>>>>>>> origin/main
    return redirect('accounts:profile', username=target_user.username)
