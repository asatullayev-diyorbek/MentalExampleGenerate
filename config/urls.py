from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from .views import user_login, user_logout

urlpatterns = [
    path('login/', user_login, name='login'),
    path('admin/', admin.site.urls),
    path('', include("smallFriends.urls")),
    path('big-friends/', include("bigFriends.urls")),
    path('family/', include("family.urls")),
    path('simple/', include("simple.urls")),
    path('logout/', user_logout, name='logout'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
