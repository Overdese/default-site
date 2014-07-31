from django.contrib.sitemaps import Sitemap
from models import Post, Parameter
from django.http import Http404
from django.core.exceptions import ObjectDoesNotExist


class PostSitemap(Sitemap):
    def __init__(self):
        super(PostSitemap, self).__init__()
        try:
            sitemap = Parameter.objects.get(name='sitemap.xml')
            if not sitemap.enable:
                raise Http404
        except ObjectDoesNotExist:
            raise Http404

    priority = 0.5

    def items(self):
        return Post.objects.filter(published=True)

    def lastmod(self, obj):
        return obj.post_date

    def location(self, obj):
        return obj.slug

