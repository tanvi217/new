from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm
from ckeditor.widgets import CKEditorWidget
from django.utils.translation import gettext_lazy as _
from .models import Campaign, Faqs, Update, Post,comment,Backers,reply


class DateInput(forms.DateInput):
    input_type = 'date'


class CampaignForm(forms.ModelForm):

    class Meta:
        model = Campaign
        exclude = ['user', 'pledged', 'people_pledged','likes']
        widgets = {
            'start_Date': DateInput(),
            'end_Date': DateInput(),
            'campaign_Title': forms.TextInput(attrs={'required': True, 'placeholder': 'Title'}),
            'campaign_': forms.TextInput(attrs={'required': True}),
            'overview': forms.Textarea(attrs={'cols': 10, 'rows': 10})
        }

        labels = {
            'image': _('Overview Image'),
        }
        help_texts = {
            'overview': _('Tell us about your campaign in a few words.'),
            'story': _('What would you like the supporters to know? '),
            'tags': _('Words that you\'d associate your campaign with.'),
            'end_Date': _('Duration of the campaign must be between 7 and 40 days.')
        }
        error_messages = {
            'campaign_Tagline': {
                'max_length': _("This title is too long."),
            },
        }


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

# class BasicsForm(forms.ModelForm):
#
#     class Meta:
#         model = Basics
#         fields = '__all__'
#
#
# class ContentForm(forms.ModelForm):
#
#     class Meta:
#         model = Content
#         fields = '__all__'
#         help_texts = {
#             'overview': _('Tell us about your campaign'),
#         }
#
#
# class FundingForm(forms.ModelForm):
#
#     class Meta:
#         model = Funding
#         fields = ['goal', 'start_Date', 'duration']


class UpdateForm(forms.ModelForm):

    class Meta:
        model = Update
        fields = ['text']


class FaqsForm(forms.ModelForm):

    class Meta:
        model = Faqs
        fields = ['question', 'answer']

class BackersForm(forms.ModelForm):

    class Meta:
        model = Backers
        fields = ['backer', 'amount']


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title','description','description2','body','order','slug']

class createcomment(forms.ModelForm):
    content = forms.CharField(label = "",widget = forms.Textarea(attrs={'class':'form-control','placeholder':'Text goes here','rows':'4','cols':'50'}))
    class Meta:
        model = comment
        fields = ['content']

class createreply(forms.ModelForm):
    content = forms.CharField(label = "",widget = forms.Textarea(attrs={'class':'form-control','placeholder':'Text goes here','rows':'4','cols':'50'}))
    class Meta:
        model = reply
        fields = ['content']
