from django.db import models
from django.db.models import PROTECT
from django.utils import timezone
import datetime
from datetime import timedelta
from PIL import Image
from django.contrib.auth.models import User
from django.utils.text import slugify
from ckeditor_uploader.fields import RichTextUploadingField
from django.urls import reverse

choose_from_categories = (
    ('creative', (
        ('comics', 'comics'),
        ('art', 'art'),
    )),
    ('tech', (
        ('education', 'education'),
        ('phones', 'phones'),
    )),
    ('community', (
        ('environment', 'environment'),
        ('culture', 'culture'),
    ))
)

choose_from_status = (
    ('cc', 'campaign created'),
    ('cd', 'campaign started'),
    ('ces', 'campaign ended successfully'),
    ('ceu', 'campaign ended unsuccessfully'),
)


class Campaign(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    campaign_Title = models.CharField(max_length=200)
    campaign_Tagline = models.CharField(max_length=200)
    campaign_Card_Image = models.ImageField(blank=True, null=True)
    campaign_Category = models.CharField(
        max_length=20,
        choices=choose_from_categories,
    )
    country = models.CharField(max_length=50, default='India')
    city = models.CharField(max_length=50)
    image = models.ImageField(upload_to="media", blank=True)
    tags = models.CharField(max_length=200, blank=True, null=True)
    overview = models.TextField(max_length=500)
    story = models.TextField(max_length=500, blank=True, null=True)
    goal = models.FloatField()
    start_Date = models.DateField()
    end_Date = models.DateField()
    pledged = models.FloatField(default=0.0)
    people_pledged = models.IntegerField(default=0)
    #    campaign_Status = models.ForeignKey(CampaignStatus, on_delete=models.PROTECT)
    likes = models.ManyToManyField(User, related_name='likes',blank=True)

    def __str__(self):
        return self.campaign_Title

    def duration_of_campaign(self):
        return self.end_Date - self.start_Date

    def get_absolute_url(self):
        return reverse('startFundraiser:campaign_detail', args=[self.id])

    def total_likes(self):
        return self.likes.count()
    # def camapign_began(self):
    #     return datetime.


class CampaignStatus(models.Model):
    class Meta:
        verbose_name_plural = 'Campaign Status'

    campaign = models.OneToOneField(Campaign, on_delete=models.CASCADE)
    status = models.CharField(max_length=5,
                              choices=choose_from_status,
                              default='cc',
                              )


#
# class CampaignStatusHistory(models.Model):
#     class Meta:
#         verbose_name_plural = 'Campaign Status History'
#     campaign_ID = models.ForeignKey(Campaign, on_delete=models.CASCADE)
#     campaign_Status = models.ForeignKey(Campaign, on_delete=models.CASCADE)


class Faqs(models.Model):
    class Meta:
        verbose_name_plural = 'FAQs'

    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE)
    question = models.TextField(max_length=100, blank=True)
    answer = models.TextField(max_length=200, blank=True)


class Update(models.Model):
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE)
    text = RichTextUploadingField()
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.text

class Post(models.Model):
    title = models.CharField(max_length = 255, blank = True, null = True)
    description = RichTextUploadingField(blank = True, null = True)
    description2 = RichTextUploadingField(blank = True, null = True, config_name = 'special')
    body = models.TextField(blank = True, null = True)
    order = models.IntegerField(blank = True, null = True)
    slug = models.SlugField(default = '', blank = True)

    def save(self):
        self.slug = slugify(self.title)
        super(Post, self).save()
    def __str__(self):
        return '%s' % self.title


class comment(models.Model):
    content = models.TextField(max_length=1000)
    date = models.DateTimeField(auto_now_add=True, null=True)
    author = models.ForeignKey(User, default=None, on_delete=models.CASCADE)
    camp = models.ForeignKey(Campaign, default=None, on_delete=models.CASCADE)

class reply(models.Model):
    content = models.TextField(max_length=1000)
    comment = models.ForeignKey(comment, default=None,null=True,on_delete=models.CASCADE)
    author = models.ForeignKey(User,default=None,null=True,on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True, null=True)


class Backers(models.Model):
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE)
    backer = models.CharField(max_length=50)
    amount = models.FloatField(null=False, blank=False)
    date_backed = models.DateTimeField(default=timezone.now)
