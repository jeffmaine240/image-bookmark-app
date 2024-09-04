from django.shortcuts import render

from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.views.decorators.http import require_POST

from .forms import LoginForm, UserRegistrationForm, UserEditForm, ProfileEditForm
from .models import Profile, Contact

from actions.models import Action
from actions.utils import create_action

# def user_login(request):
#     if request.method == 'POST':
#         form = LoginForm(request.POST)
#         if form.is_valid():
#             cd = form.cleaned_data
#             user = authenticate(request,
#                                 username=cd['username'],
#                                 password=cd['password'])
#             if user is not None:
#                 if user.is_active:
#                     login(request, user)
#                     return HttpResponse('Authenticated successfully')
#                 else:
#                     return HttpResponse('Disabled account')
#             else:
#                 return HttpResponse('Invalid login')
#     else:
#         if request.user.is_authenticated:
#             redirect_path = reverse('dashboard')
#             return HttpResponseRedirect(redirect_path)
#         form = LoginForm()
#     return render(request, 'account/login.html', {'form': form})


def register(request):
    if request.method == "POST":
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            cd = user_form.cleaned_data
            new_user = user_form.save(commit=False)
            new_user.set_password(cd['password'])
            new_user.save()
            Profile.objects.create(user=new_user)
            create_action(user=new_user, verb="has created")
            return render(request, 'account/register_done.html', {'new_user': new_user})
    else:
        if request.user.is_authenticated:
            redirect_path = reverse('dashboard')
            return HttpResponseRedirect(redirect_path)
        user_form = UserRegistrationForm()
    return render(request,'account/register.html', {'user_form': user_form})


@login_required
def dashboard(request):
    actions = Action.objects.exclude(user=request.user)
    following_id = request.user.following.values_list('id', flat=True)
    if following_id:
        actions = actions.filter(user_id__in=following_id)
        actions = actions[:10]
        print(actions)
        # actions = actions.select_related('user', 'user__profile').prefetch_related('target')[:10]
    return render(request, 'account/dashboard.html', {'section': 'dashboard', 'actions': actions})


@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile, data=request.POST, files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile updated successfully')
            redirect_path = reverse("")
            return HttpResponseRedirect(redirect_path) 
        else:
            messages.error(request, 'Error updating your profile')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    return render(request, 'account/edit.html', {'user_form': user_form, 'profile_form': profile_form})

@login_required
def user_list(request):
    users = User.objects.filter(is_active=True).exclude(id=request.user.id)
    # print(users[0].profile.photo)
    return render(request, 'account/user/list.html', {'section': 'people', 'users': users})

@login_required
def user_detail(request, username):
    user = get_object_or_404(User, username=username, is_active=True)
    print(user.get_full_name())
    return render(request, 'account/user/detail.html', {'section': 'people', 'user_details': user})

@login_required
@require_POST
def user_follow(request):
    print("okay")
    user_id = request.POST.get('id')
    action = request.POST.get('action')
    if user_id and action:
        try:
            user = User.objects.get(id=user_id)
            if action == 'follow':
                Contact.objects.get_or_create(user_from=request.user, user_to=user)
                create_action(user=request.user, verb='is following', target=user)
            else:
                Contact.objects.filter(user_from=request.user, user_to=user).delete()
            return JsonResponse({'status': 'ok'})
        except User.DoesNotExist:
            return JsonResponse({'status': 'error'})
    return JsonResponse({'status': 'error'})


