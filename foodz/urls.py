from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include("web.urls",namespace="web")),
    path('manager/',include("manager.urls",namespace="manager")),
    path('restaurant/',include("restaurant.urls",namespace="restaurant")),

    path('api/v1/customer/', include('api.v1.customer.urls')),
]


if settings.DEBUG:
    urlpatterns += (
        static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) +
        static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
)
