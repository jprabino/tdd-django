from django.db import models
from django.core.urlresolvers import reverse
from django.conf import settings
# Create your models here.

class List(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True)

    def get_absolute_url(self):
        return reverse('view_list', args=[self.id])

    @staticmethod
    def create_new(first_item_text, owner=None):
        if owner is not None:
            list_ = List.objects.create(owner=owner)
        else:
            list_ = List.objects.create()
        Item.objects.create(text=first_item_text, list=list_)
        return list_
    @property
    def name(self):
        return self.item_set.first().text

class Item(models.Model):
    text = models.TextField(default='')
    list = models.ForeignKey(List, default=None)

    def __str__(self):
        return self.text

    class Meta:
        ordering = ('id',)
        unique_together = ('list', 'text')

