from django.conf.urls import url,include
from rest_framework import routers
from . import views
router = routers.DefaultRouter()
router.register(r'genres', views.GenreViewSet)
router.register(r'tracks', views.TracksViewSet)
urlpatterns=[
    url(r'^$', views.index, name='index'),
    url(r'^v1/', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^addtrack/$',views.add_track, name='add_track'),
    url(r'^addgenre/$',views.add_genre, name='add_genre'),
    url(r'^genre/$',views.genrelist, name='genre_list'),
    url(r'^track/(?P<id>[0-9]+)/$',views.trackDetails, name='edit_track'),
    url(r'^genre/(?P<id>[0-9]+)/$',views.genreDetails, name='edit_genre'),
]