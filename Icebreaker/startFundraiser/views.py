from django.shortcuts import render, get_object_or_404, render_to_response, redirect
from django.contrib.auth import authenticate, login, logout
from django.forms import formset_factory, modelformset_factory
from django.contrib.auth.decorators import login_required
from django.db.models import Q, F
from datetime import date, datetime, timedelta
from django.template import loader
from django.http import HttpResponse, Http404, HttpResponseRedirect, JsonResponse
from django.views import generic
from django.template.loader import render_to_string

from .models import Campaign, Faqs, Update, Post, comment, reply, Reward
from .forms import CampaignForm, UserForm, UpdateForm, FaqsForm, PostForm, createcomment, createreply, BackersForm, \
    RewardModelFormset
from django.contrib.auth import get_user_model
import re

IMAGE_FILE_TYPES = ['png', 'jpg', 'jpeg']


def campaign_status():
    Campaign.objects.filter(start_Date__lte=date.today(), end_Date__gte=date.today()).update(campaign_status='started')
    Campaign.objects.filter(start_Date__lte=date.today(), end_Date__lte=date.today(), goal__lte=F('pledged')).update(
        campaign_status='successfully')
    Campaign.objects.filter(start_Date__lte=date.today(), end_Date__lte=date.today(), goal__gte=F('pledged')).update(
        campaign_status='unsuccessfully')


@login_required(login_url="http://127.0.0.1:8000/register/login/")
def add_update(request, pk):
    campaign = get_object_or_404(Campaign, pk=pk)
    if request.method == "POST":
        form = UpdateForm(request.POST)
        if form.is_valid():
            update = form.save(commit=False)
            update.campaign = campaign
            update.save()
            return redirect('startFundraiser:campaign_detail', campaign_id=pk)
    else:
        form = UpdateForm()
    return render(request, 'startFundraiser/add_update.html', {'form': form})


@login_required(login_url="http://127.0.0.1:8000/register/login/")
def add_rewards(request, pk):
    campaign = get_object_or_404(Campaign, pk=pk)
    template_name = 'startFundraiser/rewards.html'
    heading_message = 'Rewards'
    if request.method == 'POST':
        formset = RewardModelFormset(request.POST)
        if formset.is_valid():
            for form in formset:
                reward = form.save(commit=False)
                print(form.cleaned_data)
                reward.campaign = campaign
                reward.save()
            return redirect('startFundraiser:campaign_detail', campaign_id=pk)
    else:
        formset = RewardModelFormset(queryset=Reward.objects.none())
        return render(request, template_name, {
            'formset': formset,
            'heading': heading_message,
        })


@login_required(login_url="http://127.0.0.1:8000/register/login/")
def claim_reward(request, pk):
    reward = get_object_or_404(Reward, pk=pk)
    campaign = reward.campaign
    campaign.pledged = campaign.pledged + reward.amount
    reward.claimed = reward.claimed + 1
    campaign.save()
    reward.save()
    return render(request, 'startFundraiser/claim_reward.html', {'reward': reward})


def campaign_support(request, pk):
    campaign = get_object_or_404(Campaign, pk=pk)
    print(campaign)
    if request.method == "POST":
        form = BackersForm(request.POST)
        if form.is_valid():
            print('valid')
            backers = form.save(commit=False)
            backers.campaign = campaign
            backers.amount = form.cleaned_data['amount']
            if backers.amount < 50:
                context = {
                    'error_message': 'Please donate an amount greater than or equal to 50',
                    'form': form,
                }
                return render(request, 'startFundraiser/support_it.html', context)
            backers.save()
            campaign.pledged = campaign.pledged + backers.amount
            campaign.people_pledged = campaign.people_pledged + 1
            campaign.save()
            return redirect('startFundraiser:campaign_detail', campaign_id=pk)
    return render(request, 'startFundraiser/support_it.html', {'form': BackersForm(request.POST)})


@login_required(login_url="http://127.0.0.1:8000/register/login/")
def add_comment(request, pk):
    campaign1 = get_object_or_404(Campaign, pk=pk)
    if request.method == 'POST':
        form = createcomment(request.POST)
        if form.is_valid():
            a = request.POST.get('content')
            regex = re.compile('[^a-zA-Z]')
            e = regex.sub('', a)
            b = ['crap', 'shit']
            d = 0
            for c in b:
                if (e.find(c) != -1):
                    d = d + 1
            if d == 0:
                content = request.POST.get('content')
                comment1 = comment.objects.create(camp=campaign1, author=request.user, content=content)
                comment1.save()
                return redirect('startFundraiser:campaign_detail', campaign_id=pk)
                # return redirect("{% url 'startFundraiser:campaign_detail' campaign_id = campaign1.pk %}")
            else:
                return HttpResponse('Do not use bad words')
    else:
        form = createcomment()
    return render(request, 'startFundraiser/createcomment.html', {'form': form})


@login_required(login_url="http://127.0.0.1:8000/register/login/")
def add_faq(request, pk):
    campaign = get_object_or_404(Campaign, pk=pk)
    print(campaign)
    if request.method == "POST":
        form = FaqsForm(request.POST)
        if form.is_valid():
            print("valid")
            faq = form.save(commit=False)
            faq.campaign = campaign
            faq.save()
            return redirect('startFundraiser:campaign_detail', campaign_id=pk)
    else:
        form = FaqsForm()
    return render(request, 'startFundraiser/add_faq.html', {'form': form, 'campaign':campaign})


def index(request):
    projects = Campaign.objects.all()
    query = request.GET.get('q')
    if query:
        projects = projects.filter(
            Q(campaign_Title__icontains=query) |
            Q(campaign_Tagline__icontains=query) |
            Q(campaign_Category__icontains=query) |
            Q(tags__icontains=query)
        ).distinct()
        return render(request, 'startFundraiser/campaigns.html', {'projects': projects})
    else:
        return render(request, 'startFundraiser/campaigns.html', {'projects': projects})


def home(request):
    campaign_status()
    most_liked = Campaign.objects.order_by('-likes', '-pledged')[0]
    print(most_liked.campaign_status)
    camp_count = Campaign.objects.count()
    return render(request, 'startFundraiser/home.html', {'most_liked': most_liked, 'camp_count': camp_count})


def creative(request):
    projects = Campaign.objects.filter(campaign_Category__icontains='art')
    return render(request, 'startFundraiser/campaigns.html', {'projects': projects})


def social(request):
    projects = Campaign.objects.filter(campaign_Category__icontains='culture')
    return render(request, 'startFundraiser/campaigns.html', {'projects': projects})


def tech(request):
    projects = Campaign.objects.filter(campaign_Category__icontains='education')
    return render(request, 'startFundraiser/campaigns.html', {'projects': projects})


def campaigns(request):
    projects = Campaign.objects.all()
    return render(request, 'startFundraiser/campaigns.html', {'projects': projects})


def validate_start_campaign(start, end, file_type):
    error_message = {}
    duration = end - start
    delta = int(duration.days)
    print(delta)
    print(start)
    print(date.today())
    if delta > 40 or delta < 7:
        error_message['duration'] = 'Check the campaign duration'
    if file_type not in IMAGE_FILE_TYPES:
        error_message['image']: 'Image file must be PNG, JPG, or JPEG'
    if start < date.today():
        error_message['startDate']: 'Re-enter the start date to a future date'

    return error_message


@login_required(login_url="http://127.0.0.1:8000/register/login/")
def start_campaign(request):
    form = CampaignForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        campaign = form.save(commit=False)
        campaign.user = request.user
        campaign.image = request.FILES['image']
        file_type = campaign.image.url.split('.')[-1]
        file_type = file_type.lower()
        start = form.cleaned_data['start_Date']
        end = form.cleaned_data['end_Date']
        error_message = validate_start_campaign(start, end, file_type)
        print(error_message)
        if error_message:
            context = {
                'campaign': campaign,
                'form': form,
                'error_message': error_message,
            }
            return render(request, 'startFundraiser/campaign-form.html', context)
        campaign.save()
        return render(request, 'startFundraiser/detail.html', {'campaign1': campaign})
    context = {
        "form": form,
    }
    return render(request, 'startFundraiser/campaign-form.html', context)


@login_required(login_url="http://127.0.0.1:8000/register/login/")
def campaign_edit(request, pk, template_name='startFundraiser/campaign-editform.html'):
    campaign = get_object_or_404(Campaign, pk=pk)
    form = CampaignForm(request.POST or None, instance=campaign)
    if form.is_valid() and request.user == campaign.user:
        form.save()
        return redirect('startFundraiser:campaign_detail', campaign_id=pk)
    return render(request, template_name, {'form': form})


@login_required(login_url="http://127.0.0.1:8000/register/login/")
def campaign_delete(request, pk, template_name='startFundraiser/campaign-deleteform.html'):
    campaign = get_object_or_404(Campaign, pk=pk)
    if request.method == 'POST' and request.user == campaign.user and campaign.pledged == 0:
        campaign.delete()
        return redirect('startFundraiser:campaigns')
    return render(request, template_name, {'object': campaign})


def detail(request, campaign_id):
    campaign1 = get_object_or_404(Campaign, pk=campaign_id)
    is_liked = False
    if campaign1.likes.filter(id=request.user.id).exists():
        is_liked = True
    if request.user.is_authenticated and campaign1.user == request.user:
        if campaign1.tags:
            tag = campaign1.tags.split()
            context = {
                'is_editable': True,
                'campaign1': campaign1,
                'tag': tag,
                'is_liked': is_liked,
                'total_likes': campaign1.total_likes()
            }
        else:
            context = {
                'is_editable': True,
                'campaign1': campaign1,
                'is_liked': is_liked,
                'total_likes': campaign1.total_likes()
            }
    else:
        if campaign1.tags:
            tag = campaign1.tags.split()
            context = {
                'campaign1': campaign1,
                'tag': tag,
                'is_liked': is_liked,
                'total_likes': campaign1.total_likes()
            }
        else:
            context = {
                'campaign1': campaign1,
                'is_liked': is_liked,
                'total_likes': campaign1.total_likes()
            }
    return render(request, 'startFundraiser/detail.html', context)


def blog_post(request):
    web_updates = Post.objects.all()
    return render(request, 'startFundraiser/view_post.html', {'posts': web_updates})


@login_required(login_url="http://127.0.0.1:8000/register/login/")
def add_post(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post_item = form.save(commit=False)
            post_item.save()
            return render(request, 'startFundraiser/base.html')
            # return HttpResponse("Saved post")
    else:
        form = PostForm()
    return render(request, 'startFundraiser/post.html', {'form': form})


def edit_post(request, id=None):
    instance = get_object_or_404(Post, pk=id)
    form = PostForm(request.POST or None, instance=instance)
    if form.is_valid():
        form.save()
        return render(request, 'startFundraiser/base.html')
    context = {
        'form': form,
    }
    return render(request, 'startFundraiser/post.html', context)


def del_post(request, id):
    instance = get_object_or_404(Post, pk=id)
    instance.delete()
    return render(request, 'startFundraiser/base.html')


def like_camp(request):
    campaign = get_object_or_404(Campaign, id=request.POST.get('id'))
    is_liked = False
    if campaign.likes.filter(id=request.user.id).exists():
        is_liked = False
        campaign.likes.remove(request.user)
    else:
        is_liked = True
        campaign.likes.add(request.user)
    context = {
        'campaign': campaign,
        'is_liked': is_liked,
        'total_likes': campaign.total_likes()
    }

    if request.is_ajax():
        html = render_to_string('startFundraiser/like_section.html', context, request=request)
        return JsonResponse({'form': html})


def index(request):
    projects = Campaign.objects.all()
    query = request.GET.get('q')
    if query:
        projects = projects.filter(
            Q(campaign_Title__icontains=query) |
            Q(campaign_Tagline__icontains=query) |
            Q(campaign_Category__icontains=query) |
            Q(tags__icontains=query)
        ).distinct()
        return render(request, 'startFundraiser/campaigns.html', {'projects': projects})
    else:
        return render(request, 'startFundraiser/campaigns.html', {'projects': projects})
