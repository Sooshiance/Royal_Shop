from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [

    # TODO: Change the path to something else
    path('online-royal/nonsense/admin/', admin.site.urls),

    path("api/v1/user/", include("user.urls")),

    path("api/v1/store/", include("store.urls")),

    path("api/v1/club/", include("club.urls")),

]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
