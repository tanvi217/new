from django.contrib import admin

# Register your models here.

from .models import Campaign, Faqs, Update, Post,comment,Backers

admin.site.register(Campaign)
admin.site.register(Faqs)
admin.site.register(Update)
admin.site.register(Post)
admin.site.register(comment)
admin.site.register(Backers)
