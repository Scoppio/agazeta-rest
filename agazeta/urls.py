from django.contrib import admin
from django.conf.urls import url, include
from rest_framework import routers
from rest_framework.authtoken import views as vAuth
from arquivo import views, viewsets
import django_pydenticon.urls

router = routers.DefaultRouter()
router.register(r'users', viewsets.UserViewSet)
router.register(r'tob-tokens', viewsets.TobTokenViewSet)
#router.register(r'matchs', viewsets.MatchViewSet)
#router.register(r'card-played', viewsets.CardViewSet)


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/v1/', include(router.urls, namespace='v1')),
    url(r'^api/v2/', include(router.urls, namespace='v2')),
    url(r'^account/profile/$', views.account_profile),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api-token-auth/', vAuth.obtain_auth_token),
    url(r'^identicon/', include(django_pydenticon.urls.get_patterns())),
    url(r'^invitations/', include('invitations.urls', namespace='invitations')),
]