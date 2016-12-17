# -*- coding: utf-8 -*-
from django.conf import settings
try:
    from django.contrib.contenttypes.fields import GenericForeignKey
except ImportError:  # Django < 1.9 pragma: no cover
    from django.contrib.contenttypes.generic import GenericForeignKey
from django.core import serializers
from django.db import models
from django.utils.encoding import python_2_unicode_compatible

from .managers import FieldHistoryManager


@python_2_unicode_compatible
class FieldHistory(models.Model):
    object_id = models.TextField(db_index=True)
    content_type = models.ForeignKey('contenttypes.ContentType', db_index=True)
    object = GenericForeignKey()
    field_name = models.CharField('Changed Field', max_length=500, db_index=True)
    serialized_data = models.TextField()
    date_created = models.DateTimeField('Date of Change', auto_now_add=True, db_index=True)
    # user = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True)
    user = models.CharField('User Name', max_length=50, db_index=True, blank=False, null=True)
    object_name = models.CharField('Object Name', max_length=500, db_index=True, blank=False, null=True)

    objects = FieldHistoryManager()

    class Meta:
        get_latest_by = 'date_created'
        verbose_name = 'History Item'
        verbose_name_plural = 'History Items'

    def __str__(self):
        return '{} field history for {}'.format(self.field_name, self.object)

    @property
    def field_value(self):
        instances = serializers.deserialize('json', self.serialized_data)
        instance = list(instances)[0].object
        return getattr(instance, self.field_name)
