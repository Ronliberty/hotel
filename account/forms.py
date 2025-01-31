from django import forms
from django.contrib.auth.models import User, Group
from django.core.exceptions import ValidationError


class CustomUserCreationForm(forms.Form):
    username = forms.CharField(max_length=150, required=True)
    password = forms.CharField(widget=forms.PasswordInput(), required=True)
    confirm_password = forms.CharField(widget=forms.PasswordInput(), required=True)
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    group = forms.ChoiceField(choices=[], required=True)

    def __init__(self, *args, **kwargs):
        groups = kwargs.pop('groups', None)  # Receive groups from the view
        super().__init__(*args, **kwargs)
        if groups:
            self.fields['group'].choices = [(group.name, group.name) for group in groups]

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password:
            if password != confirm_password:
                raise ValidationError("Passwords do not match.")

        return cleaned_data

    def save(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        email = self.cleaned_data['email']
        first_name = self.cleaned_data['first_name']
        last_name = self.cleaned_data['last_name']
        group_name = self.cleaned_data['group']
        group = Group.objects.get(name=group_name)

        user = User.objects.create_user(username=username, password=password, email=email,
                                        first_name=first_name, last_name=last_name)
        user.groups.add(group)
        user.save()

        return user
