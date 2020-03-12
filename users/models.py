from __future__ import unicode_literals
from __future__ import unicode_literals
from django.conf import settings
from django.contrib.auth.models import User

# from django.db import models
# from django.utils.encoding import smart_text as smart_unicode
from django.utils.translation import ugettext_lazy as _
from django.db import models

CHOICES = (
    ('bench','Bench'),
    ('devops', 'Devops'),
    ('production','Production'),
    ('hr','HR'),
    ('lead','Leaders'),
)


class UserInfo(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, primary_key=True)
    full_name = models.CharField(max_length=255, null=True, blank=True, default="NA")
    designation  = models.CharField(max_length=255)
    project = models.CharField(max_length=255, choices=CHOICES, default='bench', blank=True ,null=True)
    doj = models.DateTimeField(_("Date Created"), auto_now_add=True)
    gender = models.CharField(max_length=10, null=True, blank=True, default=None)
    permissions = models.CharField(max_length=1, default="V")
    mobile_number = models.IntegerField(max_length=10, null=True, blank=True, default=None)
    total_exp = models.IntegerField(max_length=2, null=True, blank=True, default=None)
    project_exp = models.IntegerField(max_length=2, null=True, blank=True, default=None)
    img = models.ImageField(upload_to='empid', blank=True, null=True, default="/media/empid/image.png")


    def __str__(self):
        return self.user.username+":"+self.project


class Shift(models.Model):
    user  = models.CharField(max_length=20)
    date = models.DateField(default=None)
    shift = models.CharField(max_length=1,default='G')

    class Meta:
        unique_together = ('user',"date","shift")
    def __str__(self):
        return self.user+":"+self.shift




# -> date format

# d = datetime.date(1997, 10, 19)
#
# # creating an instance of
# # GeeksModel
# geek_object = GeeksModel.objects.create(geeks_field=d)
# geek_object.save()



# ->custom responce

 # a = UserInfo.objects.all()
 #        list = []
 #        for i in a:
 #            list.append(
 #                {
 #                    'user':{
 #                        'id':i.user.id,
 #                        'username': i.user.username,
 #                        'email':i.user.email
 #                    },
 #                    'designation': i.designation,
 #                    'project': i.project,
 #                    "doj":i.doj,
 #                    'gender': i.gender,
 #                    'permission':i.permission
 #                }
 #            )
 #        return Response(list)