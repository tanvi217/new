from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm
from django.forms import (formset_factory, modelformset_factory, inlineformset_factory)
from django.forms.widgets import SelectDateWidget
from django.utils import timezone
from ckeditor.widgets import CKEditorWidget
from django.utils.translation import gettext_lazy as _
from .models import Campaign, Faqs, Update, Post, comment, Backers, reply, Reward
import datetime
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Field


class CampaignForm(forms.ModelForm):
    start_Date = forms.DateField(widget=SelectDateWidget(
        empty_label=("Choose Year",
                     "Choose Month",
                     "Choose Day"),
    ),
        initial=timezone.now())
    end_Date = forms.DateField(widget=SelectDateWidget(
        empty_label=("Choose Year",
                     "Choose Month",
                     "Choose Day"),
    ),
        initial=timezone.now())

    class Meta:
        model = Campaign
        fields = ['campaign_Title', 'campaign_Tagline', 'campaign_Category', 'country', 'city', 'overview', 'goal',
                  'story', 'tags', 'campaign_Card_Image', 'image']
        widgets = {
            'campaign_Title': forms.TextInput(attrs={'required': True, 'placeholder': 'Title'}),
            'campaign_': forms.TextInput(attrs={'required': True}),
            'image': forms.ClearableFileInput(attrs={'multiple': True}),
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

    def __init(self, *args, **kwargs):
        super(CampaignForm, self).__init(*args, **kwargs)
        self.fields['campaign_Title'].error_messages = {
            "max_length": "This title is too long.",
            "required": "The title field is required."
        }

        for field in self.fields.values():
            field.error_message = {
                'required': "{fieldname} is required".format(fieldname=field.label),
            }


RewardModelFormset = modelformset_factory(
    Reward,
    fields=('amount', 'perks', 'quantity',),
    extra=1,
    widgets={'perks': forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Describe the reward that you\'d like to offer to supporters'
    })
    }
)


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']


class UpdateForm(forms.ModelForm):
    class Meta:
        model = Update
        fields = ['text']


class FaqsForm(forms.ModelForm):
    class Meta:
        model = Faqs
        fields = ['question', 'answer']

    helper = FormHelper()
    helper.form_method = 'POST'


class BackersForm(forms.ModelForm):
    class Meta:
        model = Backers
        fields = ['backer', 'amount']


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'description', 'description2', 'body', 'order', 'slug']


class createcomment(forms.ModelForm):
    content = forms.CharField(label="", widget=forms.Textarea(
        attrs={'class': 'form-control', 'placeholder': 'Text goes here', 'rows': '4', 'cols': '50'}))

    class Meta:
        model = comment
        fields = ['content']


class createreply(forms.ModelForm):
    content = forms.CharField(label="", widget=forms.Textarea(
        attrs={'class': 'form-control', 'placeholder': 'Text goes here', 'rows': '4', 'cols': '50'}))

    class Meta:
        model = reply
        fields = ['content']
