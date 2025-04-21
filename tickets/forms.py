from django import forms
from accounts.models import Profile


class ProfileEditForm(forms.ModelForm):
    first_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=False
    )
    last_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=False
    )
    email = forms.EmailField(
        max_length=100,
        widget=forms.EmailInput(attrs={'class': 'form-control'}),
        required=False
    )
    phone = forms.CharField(
        max_length=14,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=False
    )
    image = forms.ImageField(
        widget=forms.ClearableFileInput(attrs={'class': 'form-control'}),
        required=False,
    )
    about_me = forms.CharField(
        max_length=250,
        widget=forms.Textarea(attrs={'class': 'form-control'}),
        required=False
    )

    class Meta:
        model = Profile
        fields = ('first_name', 'last_name', 'email', 'phone', 'image', 'about_me')
