from django.db import models
from django.utils.timezone import now
from django.conf import settings


class AccessLogs(models.Model):
    url_path = models.CharField(max_length=512)
    view_name = models.CharField(max_length=64)
    method = models.CharField(max_length=8)
    host_ip = models.CharField(max_length=32, blank=True)
    http_x_forwarded_for = models.TextField(blank=True)
    query_params = models.TextField( blank=True)
    form_data = models.TextField(blank=True)
    file_params = models.TextField(blank=True)
    results = models.TextField()
    accessed_on = models.DateTimeField(default=now)
    accessed_by = models.ForeignKey(settings.AUTH_USER_MODEL, models.DO_NOTHING, blank=True, null=True)
    uuid = models.CharField(max_length=64, blank=True)
