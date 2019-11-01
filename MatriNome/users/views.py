from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm, ProfileCreationForm
from django.contrib.auth.decorators import login_required
from .models import Profile, ContactRequest
from django.contrib.auth.models import User

from django.core.mail import send_mail
from django.conf import settings


def register(request):
    if request.method == 'POST':
        u_form = UserRegisterForm(request.POST)
        p_form = ProfileCreationForm(request.POST, request.FILES)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            profile = Profile.objects.create(user=User.objects.filter(username=request.POST.get('username')).first(),
                                             age=request.POST.get('age'),
                                             gender=request.POST.get('gender'),
                                             about=request.POST.get('about'),
                                             religion=request.POST.get('religion'),
                                             mother_tongue=request.POST.get('mother_tongue'))
            profile.save()
            messages.success(request, f'Your account has been created! You are now able to login')
            return redirect('login')
    else:
        u_form = UserRegisterForm()
        p_form = ProfileCreationForm()
    return render(request, "users/register.html", {'u_form': u_form, 'p_form': p_form})


def ProfileDetailView(request, *args, **kwargs):
    if kwargs.get('pk') == request.user.id:
        if request.method == 'POST':
            u_form = UserUpdateForm(request.POST, instance=request.user)
            p_form = ProfileUpdateForm(request.POST,
                                       request.FILES,
                                       instance=request.user.profile)

            if u_form.is_valid() and p_form.is_valid():
                u_form.save()
                p_form.save()
                messages.success(request, f'Your account has been updated!')
                return redirect('profile')
        else:
            u_form = UserUpdateForm(instance=request.user)
            p_form = ProfileUpdateForm(instance=request.user.profile)

        context = {
            'u_form': u_form,
            'p_form': p_form
        }
        return render(request, "users/self_profile.html", context)
    else:
        return render(request, "users/profile.html", {'user': User.objects.filter(id=kwargs.get('pk')).first()})


def ProfileListView(request):
    if request.user.is_authenticated:
        queryset = Profile.objects.exclude(user=request.user)
    else:
        queryset = Profile.objects.all()
    return render(request, "users/home.html", {'profiles': queryset})


@login_required
def ProfileSearchView(request):
    queryset = Profile.objects.filter(gender=request.GET.__getitem__('gender'),
                                      age__gte=int(request.GET.__getitem__('age_from')),
                                      age__lte=int(request.GET.__getitem__('age_to')),
                                      mother_tongue=request.GET.__getitem__('mother_tongue'),
                                      religion=request.GET.__getitem__('religion')).exclude(user=request.user)

    return render(request, "users/home.html", {'profiles': queryset})


def contact(request, *args, **kwargs):
    reverse, created_rev = ContactRequest.objects.get_or_create(
        user_to=request.user, user_from=User.objects.all().filter(id=kwargs.get("pk")).first())
    new, created_new = ContactRequest.objects.get_or_create(
        user_from=request.user, user_to=User.objects.all().filter(id=kwargs.get("pk")).first())
    if created_new:
        new.save()
    if created_rev and created_new:
        send_mail('New Smash Request',
                  f'Request by {request.user}',
                  settings.EMAIL_HOST_USER,
                  {User.objects.all().filter(id=kwargs.get("pk")).first().email})

    if not created_rev and created_new:
        send_mail('Smash',
                  f'Contact of {request.user}',
                  settings.EMAIL_HOST_USER,
                  {User.objects.all().filter(id=kwargs.get("pk")).first().email})

        send_mail('Smash',
                  f'Contact of {User.objects.all().filter(id=kwargs.get("pk")).first()}',
                  settings.EMAIL_HOST_USER,
                  {request.user.email})

    return render(request, "users/profile.html", {'user': User.objects.filter(id=kwargs.get('pk')).first()})
