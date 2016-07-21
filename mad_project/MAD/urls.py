from django.conf.urls import url
from MAD import views

urlpatterns = [
    url(r'^categories/$', views.category_list),
    url(r'^activities/$', views.activity_list),
    url(r'^categories/(?P<pk>[0-9]+)/$', views.category_detail),
]