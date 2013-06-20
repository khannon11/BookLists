from django.conf.urls import patterns, include, url

from books import views

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'login.html'}, name='login'),
    url(r'^register/$', views.register, name='register'),
    url(r'^profile/$', views.profile, name='profile'),
    url(r'^accounts/profile/$', views.profile, name='profile'),
    url(r'^addBook/$', views.addBook, name='add_book'),
    url(r'^addRec/$', views.newRec, name='add_rec'),
    url(r'^addReview/$', views.addReview, name='add_review'),
    url(r'^logout/$', views.logout_user, name='logout'),
    url(r'^review/(?P<id_num>\d+)/$', views.view_review, name='review'),
    url(r'^rec/(?P<id_num>\d+)/$', views.view_rec, name='review'),
    # url(r'^$', 'booklists.views.home', name='home'),
    # url(r'^booklists/', include('booklists.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
