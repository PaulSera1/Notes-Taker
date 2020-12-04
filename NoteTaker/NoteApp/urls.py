from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('', include('django.contrib.auth.urls')),
    url(r'^signup/$', views.signup, name='signup'),
    path('post/ajax/note', views.postnote, name='post_note'),
    path('post/ajax/deletenote', views.deletenote, name='delete_note'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)