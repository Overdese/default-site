from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from site_core.views import show_home, show_post,show_page, show_tag_posts, show_category_posts, ajax_json,\
    show_robots_file, search

#MEDIA setting
from django.conf import settings
from django.conf.urls.static import static
# sitemap setting
from site_core.sitemaps import PostSitemap
sitemaps = {'main': PostSitemap}
from site_core.models import Parameter
from django.core.exceptions import ObjectDoesNotExist



urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'default_site.views.home', name='home'),
    # url(r'^default_site/', include('default_site.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    #url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    url(r'^ckeditor/', include('ckeditor.urls')),

    #pages:
    url(r'^(?:(\d{1,5})/)?$', show_home),
    url(r'^post/(.+?)/$', show_post),
    url(r'^page/(.+?)/$', show_page),
    url(r'^tag/([^/]+)/(?:(\d{1,5})/)?$', show_tag_posts),
    url(r'^category/([^/]+)/(?:(\d{1,5})/)?$', show_category_posts),
    url(r'^search/$', search),

    #ajax
    url(r'^ajax/json/$', ajax_json),

    url(r'^sitemap\.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemaps}),

    #robots.txt
    url('^robots\.txt$', show_robots_file),

) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


