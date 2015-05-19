from django.conf.urls import patterns, include, url
from django.contrib import admin
from polls.views import search,about,getSearchData,extendNode,index,searchProvinceTime,searchSingle

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'liyi.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$',index),
    url(r'^index/$',index,name = "index"),
    url(r'^about/$',about,name = "about"),
    url(r'^search/$',search,name = "search"),
    url(r'^searchSingle/$',searchSingle,name = "searchSingle"),
    url(r'^searchProvinceTime/$',searchProvinceTime,name = "searchProvinceTime"),
    url(r'^getSearchData/$',getSearchData,name = "getSearchData"),
    url(r'^extendNode/$',extendNode,name = "extendNode")
)