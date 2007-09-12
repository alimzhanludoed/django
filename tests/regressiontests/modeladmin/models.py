# coding: utf-8
from django.db import models

class Band(models.Model):
    name = models.CharField(max_length=100)
    bio = models.TextField()


__test__ = {'API_TESTS': """

>>> from django.contrib.admin.options import ModelAdmin
>>> from django.contrib.admin.sites import AdminSite

None of the following tests really depend on the content of the request, so
we'll just pass in None.

>>> request = None

>>> band = Band(name='The Doors', bio='')

Under the covers, the admin system will initialize ModelAdmin with a Model
class and an AdminSite instance, so let's just go ahead and do that manually
for testing.

>>> site = AdminSite()
>>> ma = ModelAdmin(Band, site)

>>> ma.form_add(request).base_fields.keys()
['name', 'bio']


# form/fields/fieldsets interaction ##########################################

fieldsets_add and fieldsets_change should return a special data structure that
is used in the templates. They should generate the "right thing" whether we
have specified a custom form, the fields arugment, or nothing at all.

Here's the default case. There are no custom form_add/form_change methods,
no fields argument, and no fieldsets argument.

>>> ma = ModelAdmin(Band, site)
>>> ma.fieldsets_add(request)
[(None, {'fields': ['name', 'bio']})]
>>> ma.fieldsets_change(request, band)
[(None, {'fields': ['name', 'bio']})]


If we specify the fields argument, fieldsets_add and fielsets_change should
just stick the fields into a formsets structure and return it.

>>> class BandAdmin(ModelAdmin):
...     fields = ['name']

>>> ma = BandAdmin(Band, site)
>>> ma.fieldsets_add(request)
[(None, {'fields': ['name']})]
>>> ma.fieldsets_change(request, band)
[(None, {'fields': ['name']})]




If we specify fields or fieldsets, it should exclude fields on the Form class
to the fields specified. This may cause errors to be raised in the db layer if
required model fields arent in fields/fieldsets, but that's preferable to
ghost errors where you have a field in your Form class that isn't being
displayed because you forgot to add it to fields/fielsets

>>> class BandAdmin(ModelAdmin):
...     fields = ['name']

>>> ma = BandAdmin(Band, site)
>>> ma.form_add(request).base_fields.keys()
['name']
>>> ma.form_change(request, band).base_fields.keys()
['name']

>>> class BandAdmin(ModelAdmin):
...     fieldsets = [(None, {'fields': ['name']})]

>>> ma = BandAdmin(Band, site)
>>> ma.form_add(request).base_fields.keys()
['name']
>>> ma.form_change(request, band).base_fields.keys()
['name']




"""
}
