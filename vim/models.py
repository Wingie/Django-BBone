from django.db import models


# Create your models here.
class VimeoUser(models.Model):
    display_name = models.CharField(max_length=256,default="")
    user_name = models.CharField(max_length=256,default="")
    page_url = models.URLField(max_length=256,default="http://")
    is_pay = models.BooleanField(default=False)
    has_staff_pick = models.BooleanField(default=False)
    has_videos= models.BooleanField(default=False)
    def __unicode__(self):
        return self.display_name
