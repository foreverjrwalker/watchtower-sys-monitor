from django.conf.urls import patterns, include, url

from django.contrib import admin
import watchtower.urls
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'wt_server.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')), 
    url(r'^watchtower/', include(watchtower.urls)),
    url(r'^watchtower/api/', include(watchtower.urls)),
    url(r'^admin/', include(admin.site.urls)),
)
