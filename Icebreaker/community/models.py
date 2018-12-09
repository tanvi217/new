from django.db import models
from django.contrib.auth.models import User
import datetime



class GroupTable(models.Model):
    founder = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    type = models.CharField(max_length=100)
    lat = models.FloatField(default=0.0)
    lon = models.FloatField(default=0.0)
    date = models.DateField()
    number = models.IntegerField(default=0)
    address = models.CharField(max_length=100, default="")


    def __str__(self):
        return self.title

class MemberTable(models.Model):
    group = models.ForeignKey(GroupTable, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return u'%s by %s' % (self.group, self.user)

class CommentTable(models.Model):
    group = models.ForeignKey(GroupTable, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    comment = models.CharField(max_length=500)


    def __str__(self):
        return u'on %s by %s said    %s' % (self.group, self.user, self.comment)

class UpdateTable(models.Model):
    group = models.ForeignKey(GroupTable, on_delete=models.CASCADE)
    update = models.CharField(max_length=1000)
    #date = models.DateField(default=datetime.date.today())
    def __str__(self):
        return u'%s' % (self.update)

