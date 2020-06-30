from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.contrib.auth import update_session_auth_hash


# Create your views here.


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username') #or use username = request.POST['username']
            messages.success(request, f'Account has been created for {username} ! You can now  login')
            return redirect('login')
    else:
        form = UserRegisterForm()

    return render(request, 'users/register.html', {'form':form})


# THE FOLLOWING CLASSBASEDVIEW CAN ALSO BE USED FOR  USER REGISTRATION........!

class RegisterView(CreateView):
    form_class = UserRegisterForm
    template_name = "users/view_register.html"
    success_url = reverse_lazy("login")




@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated')
            return redirect('profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

        
    context = {
        'u_form' : u_form,
        'p_form' :  p_form
    }
    return render(request, 'users/profile.html', context)



def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success( request, 'Your Password has been changed successfully!')
            return redirect('home-blog')
    else:
        form = PasswordChangeForm(user=request.user)                        # update_session_auth_hash makes the user to be logged in after
                                                                            # user changes password, otherwise changing passwords logouts 
    context = {'form': form}                                                # the user by default.
    return render(request, 'users/change_password.html', context)
