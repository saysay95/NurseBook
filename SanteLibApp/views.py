from django.shortcuts import render, redirect
from .models import Nurse
from .forms import NurseRegistrationForm, SignupForm, LoginForm, NurseProfileForm
from django.http import HttpResponse, HttpResponseRedirect
import os.path
from PIL import Image
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.contrib.auth.models import User
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.core.mail import EmailMessage
from django.utils.encoding import force_bytes, force_text
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


def nurse(request, user_id):
    if request.method == 'POST':
        form = NurseProfileForm(request.POST or None, request.FILES)
        if form.is_valid() and request.user.is_authenticated:
            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]
            date_of_birth = form.cleaned_data["date_of_birth"]
            date_of_graduation = form.cleaned_data["date_of_graduation"]
            sex = form.cleaned_data["sex"]
            email = form.cleaned_data["email"]
            diploma = form.cleaned_data["diploma"]
            spoken_languages = form.cleaned_data["spoken_languages"]

            try:
                current_nurse = Nurse.objects.filter(user_id=user_id).update(first_name=first_name,last_name=last_name,
                                                                             email=email,date_of_birth=date_of_birth,
                                                                             date_of_graduation=date_of_graduation,
                                                                             sex=sex,user_id=user_id,diploma=diploma,
                                                                             spoken_languages=spoken_languages)
                # current_nurse.first_name = first_name
                # current_nurse.last_name = last_name
                # current_nurse.save(update_fields=['first_name','last_name'])
            except Nurse.DoesNotExist:
                new_nurse = Nurse(first_name=first_name,last_name=last_name,
                                  email=email,date_of_birth=date_of_birth,
                                  date_of_graduation=date_of_graduation,
                                  sex=sex,user_id=user_id,diploma=diploma,
                                  spoken_languages=spoken_languages)
                new_nurse.save()
            # Duplicate(instance,128,128)
    else:
        try:
            current_nurse = Nurse.objects.get(user_id=user_id)
            form = NurseProfileForm(initial={'first_name': current_nurse.first_name,
                                             'last_name' : current_nurse.last_name,
                                             'email' : current_nurse.email,
                                             'date_of_birth' : current_nurse.date_of_birth,
                                             'date_of_graduation' : current_nurse.date_of_graduation,
                                             'sex' : current_nurse.sex,
                                             'diploma' : current_nurse.diploma,
                                             'spoken_languages' : current_nurse.spoken_languages})
        except Nurse.DoesNotExist:
            form = NurseProfileForm()

    if request.user.is_authenticated:
        context = {"user": User.objects.get(id=request.user.id),
                   "form": form}
    else:
        context = {"user": User.objects.get(id=user_id),
                   "first_name": "test",
                   "form": form}

    return render(request, "en/nurse_profile.html", context)


def index(request):
    return render(request, "en/index.html")


def sign_in(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                if request.GET.get('next') is not None:
                    return redirect(request.GET['next'])
                return redirect(reverse('index'))

        else:
            return render(request, 'en/sign_in.html', {'form': form})
    else:
        form = LoginForm()

    return render(request, 'en/sign_in.html', {'form': form})


def sign_up(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            new_user.is_active = False
            new_user.save()

            current_site = get_current_site(request)
            mail_subject = 'Activate your SanteLib account.'
            message = render_to_string('en/account_confirmation_email.html', {
                'user': new_user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(new_user.pk)),
                'token': account_activation_token.make_token(new_user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.send()
            return render(request,'en/account_confirmation.html')

        else:
            return render(request, 'en/sign_up.html', {'form': form})
    else:
        form = SignupForm()

    return render(request, 'en/sign_up.html', {'form': form})


def sign_out(request):
    logout(request)
    return render(request, 'en/home.html')

# todo : username + password prepopulated
# def login(request, username):
#     context = {
#         "user": User.objects.get(username=username)
#     }
#     return render(request, "en/sign_in.html",context)


def nurse_registration(request):
    sent = False
    if request.method == 'POST':
        form = NurseRegistrationForm(request.POST or None, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            # Duplicate(instance,128,128)
            sent = True
            return HttpResponse('Please confirm your email address to complete the registration')
    else:
        form = NurseRegistrationForm()
    return render(request, 'en/nurse_registration.html', locals())


# Create a thumbnail from image
def resize_image(original,l,h):
    # Duplicate uploaded photo to /small directory
    folder_path = os.path.dirname(original.photo.path)
    base_name = os.path.basename(original.photo.path)
    file_name = os.path.basename(base_name) [0]
    file_extension = os.path.splitext(original.photo.path)[1]
    new_file_path = folder_path + '/small/' + base_name

    # Shrink the duplicated photo
    try:
        size = (l, h)
        im = Image.open(original.photo.path)
        im.thumbnail(size)
        im.save(new_file_path, "JPEG")
    except IOError:
        print("Cannot create thumbnail for ", new_file_path)

    return


def nurses(request):
    context = {
        "nurses": Nurse.objects.all()
    }
    return render(request, "en/nurses.html", context)

# TODO: check if username exists via ajax, and send confirmation email before creation



def activate(request, uid, token):
    try:
        uid = force_text(urlsafe_base64_decode(uid))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        # return redirect('home')
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')