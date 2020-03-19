from django.urls import path
from django.conf.urls import url
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.nurses),
    path('index',views.index, name='index'),
    path('nurse/<int:user_id>', views.nurse, name='nurse'),
    path('nurses',views.nurses, name='nurses'),
    path('nurse/register', views.nurse_registration, name='nurse_registration'),
    path('sign-in', views.sign_in, name='sign_in'),
    path('sign-out', views.sign_out, name='sign_out'),
    path('sign-up', views.sign_up, name='sign_up'),
    url(r'^activate/(?P<uid>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
