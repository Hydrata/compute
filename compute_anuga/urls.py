from rest_framework import routers
from django.conf.urls import url, include
from compute_anuga import api, views

router = routers.DefaultRouter()
router.register(r'compute', api.ComputeViewSet, 'compute')

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^api/', include(router.urls)),
 ]

