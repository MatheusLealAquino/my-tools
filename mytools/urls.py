"""mytools URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from quotation import views as views_quotation

router = routers.DefaultRouter()
router.register(r'demand', views_quotation.DemandViewSet, basename='demand')
router.register(r'state', views_quotation.StateViewSet)
router.register(r'city', views_quotation.CityViewSet)
router.register(r'group', views_quotation.GroupViewSet)
router.register(r'user', views_quotation.UserViewSet, basename='user')
router.register(r'user/(?P<pk>\d+)/group', views_quotation.UserGroupViewSet, basename='user_group')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('auth/', include('djoser.urls.authtoken')),
]
