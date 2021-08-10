from django.contrib.sitemaps import Sitemap
from . import models

class OfferSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.9

    def items(self):
        return models.Offer.objects.all()

    def lastmod(self, obj):
        return obj.created
