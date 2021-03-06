from django.conf.urls import patterns, include, url
from django.contrib import admin
from rest_framework import routers
from MAD import views

router = routers.DefaultRouter()



urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'mad_project.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^api', include(router.urls)),
    url(r'^', include('MAD.urls')),

)
