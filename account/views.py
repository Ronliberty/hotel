from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views import View
from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import UserCreationForm
from .forms import CustomUserCreationForm
# Create your views here.
User = get_user_model()
def role_based_redirect(request):
    if request.user.is_superuser:
        return redirect('dashboard:super_dashboard')
    if request.user.groups.filter(name='manager').exists():
        return redirect('dashboard:manager_dashboard')
    elif request.user.groups.filter(name='cashier').exists():
        return redirect('dashboard:cashier_dashboard')
    elif request.user.groups.filter(name='storekeeper').exists():
        return redirect('dashboard:store_dashboard')
    elif request.user.groups.filter(name='roomkeeper').exists():
        return redirect('dashboard:rooms_dashboard')
    else:
        messages.error(request, "Try again!.")
        return redirect('base:index')


class CreateUserView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = 'auth.add_user'  # Permission to add users

    def get(self, request):

        groups = Group.objects.all() # Get all available groups
        form = CustomUserCreationForm(groups=groups)

        return render(request, 'account/create_user.html', {'form': form, 'groups': groups})

    def post(self, request):
        # Get all available groups again (in case the page was refreshed)
        groups = Group.objects.all()

        # Instantiate the form with POST data and pass the groups to it
        form = CustomUserCreationForm(request.POST, groups=groups)

        if form.is_valid():
            # Check if the username already exists
            username = form.cleaned_data['username']
            if get_user_model().objects.filter(username=username).exists():
                messages.error(request, "The username already exists. Please choose another one.")
                return render(request, 'account/create_user.html', {'form': form, 'groups': groups})

            # If the form is valid and username doesn't exist, save the user
            form.save()
            return redirect('account:user_management')

        # If form is not valid, render the page with the form and groups again
        return render(request, 'account/create_user.html', {'form': form, 'groups': groups})

class UserManagementView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = 'auth.change_user'

    def get(self, request):
        users = User.objects.all()  # List all users
        return render(request, 'account/user_management.html', {'users': users})



class AssignToGroupView(LoginRequiredMixin, View):
    def get(self, request, user_id):
        user = User.objects.get(id=user_id)
        groups = Group.objects.all()
        return render(request, 'account/assign_group.html', {'user': user, 'groups': groups})

    def post(self, request, user_id):
        user = User.objects.get(id=user_id)
        group_name = request.POST.get('group')
        group = Group.objects.get(name=group_name)
        user.groups.add(group)
        return redirect('account/user_management')  # Redirect back to user management page



class ViewUsersInGroupView(LoginRequiredMixin, View):
    def get(self, request):
        group_name = request.GET.get('group')  # Get group from URL parameters
        group = Group.objects.get(name=group_name)
        users = group.user_set.all()  # Get users in the group
        return render(request, 'account/view_users_in_group.html', {'users': users, 'group': group})


class UserListView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = 'auth.view_user'  # Permission to view users

    def get(self, request):
        users = User.objects.all()  # Get all users
        return render(request, 'account/user_list.html', {'users': users})