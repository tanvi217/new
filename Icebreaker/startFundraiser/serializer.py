from rest_framework import serializers
from django.contrib.auth.models import User
from startFundraiser.models import Backers
'''
class UserLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email']
'''

class fundsSerializer(serializers.ModelSerializer):
    #backer = UserLogSerializer()
    class Meta:
        model = Backers
        fields = ('campaign','backer','amount','date_backed') #email, phone no
        #read_only_fields = ('force',)
