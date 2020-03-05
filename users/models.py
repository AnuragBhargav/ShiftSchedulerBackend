from __future__ import unicode_literals
from __future__ import unicode_literals
from django.conf import settings

# from django.db import models
# from django.utils.encoding import smart_text as smart_unicode
from django.utils.translation import ugettext_lazy as _
from django.db import models


class UserInfo(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    designation  = models.CharField(max_length=255)
    project = models.CharField(max_length=255)
    doj = models.DateTimeField(_("Date Created"), auto_now_add=True)
    gender = models.CharField(max_length=10)

