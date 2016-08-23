from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from django.conf.urls import include
from MAD import views

urlpatterns = [
    url(r'^login/$', views.login.as_view()),
		url(r'^new-pass/$', views.setPassword.as_view()),
    url(r'^categories/$', views.category_list.as_view()),
    url(r'^activities/$', views.activity_list.as_view()),
    url(r'^activities/(?P<pk>[0-9]+)/$', views.ActivityDetail.as_view()),
    url(r'^staff/$', views.staff_activiy_list.as_view()),
    url(r'^new-event/$', views.newEvent.as_view()),
    url(r'^new-admin/$', views.newAdmin.as_view()),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),

]

urlpatterns = format_suffix_patterns(urlpatterns)