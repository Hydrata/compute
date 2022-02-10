from django.contrib import admin
from django.urls import path, include

from compute_anuga import urls as compute_anuga_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('compute_anuga/', include(compute_anuga_urls)),
]
