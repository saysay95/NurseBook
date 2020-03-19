from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Nurse
from .models import Address
from django.utils.translation import gettext, gettext_lazy as _
from django.contrib.auth import authenticate, login
from SanteLib import config
from django_select2.forms import Select2MultipleWidget

# class NurseRegistrationForm(forms.ModelForm):
#     class Meta:
#         model = Nurse
#         fields = '__all__'
#         exclude = ('rating','address')
#         widgets = {
#             'date_of_graduation': forms.DateInput(attrs={'type': 'date'}),
#             'date_of_birth': forms.DateInput(attrs={'type': 'date'})
#         }


class NurseRegistrationForm(UserCreationForm):
    class Meta:
        model = Nurse
        fields = '__all__'
        # fields = ('username', 'email', 'password1', 'password2')
        exclude = ('rating','address')
        widgets = {
            'date_of_graduation': forms.DateInput(attrs={'type': 'date'}),
            'date_of_birth': forms.DateInput(attrs={'type': 'date'})
        }


class AddressForm(UserCreationForm):
    class Meta:
        model = Address
        fields = '__all__'


class SignupForm(UserCreationForm):

    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(max_length=32, required=False, help_text='Optional.',
                                 widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(max_length=32, required=False, help_text='Optional.',
                                widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}), max_length=64,
                             help_text='Enter a valid email address')
    password1 = forms.CharField(label=_("Password"), widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label=_("Password (re-type)"), widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = UserCreationForm.Meta.fields + ('first_name', 'last_name', 'email')

    def save(self, commit=True):
        user = super(SignupForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
        return user


class LoginForm(forms.Form):
    username = forms.CharField(label="Login")
    password = forms.CharField(label="Password", widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super(LoginForm, self).clean()
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        if not authenticate(username=username, password=password):
            raise forms.ValidationError("Wrong login or password")
        return self.cleaned_data


class NurseProfileForm(forms.Form):
    first_name = forms.CharField(max_length=32, required=False,
                                 widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(max_length=32, required=False,
                                widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}), max_length=64,
                             help_text='Enter a valid email address')
    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    date_of_graduation = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    sex = forms.ChoiceField(choices=config.SEX_CHOICES)
    # querset = MyModel.objects.filter(id__in=custom_list)
    # config.LANGUAGE_CHOICES.objects.filter
    # forms.MultipleChoiceField(choices=config.LANGUAGE_CHOICES, widget=forms.CheckboxSelectMultiple())
    # spoken_languages = forms.ModelMultipleChoiceField(queryset=config.LANGUAGE_CHOICES, widget=Select2MultipleWidget)

    spoken_languages = forms.MultipleChoiceField(choices=config.LANGUAGE_CHOICES, widget=forms.CheckboxSelectMultiple())

    diploma = forms.FileField()

    class Meta:
        model = Nurse
        fields = '__all__'
        # exclude = ('rating','address')
        # widgets = {
        #     'date_of_graduation': forms.DateInput(attrs={'type': 'date'}),
        #     'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
        #     'email': forms.EmailInput(attrs={'class': 'form-control'})
        # }



