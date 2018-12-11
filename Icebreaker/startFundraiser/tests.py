from django.test import TestCase, Client
from .models import *

class TestUrls(TestCase):

    def test_all_campaigns_url(self):
        response = self.client.get('/startfundraiser/all_campaigns/')
        self.assertEqual(response.status_code, 200)

    def test_campaigns_creative_url(self):
        response = self.client.get('/startfundraiser/campaigns/creative/')
        self.assertEqual(response.status_code, 200)

    def test_campaigns_social_url(self):
        response = self.client.get('/startfundraiser/campaigns/social/')
        self.assertEqual(response.status_code, 200)

    def test_campaigns_tech_url(self):
        response = self.client.get('/startfundraiser/campaigns/tech/')
        self.assertEqual(response.status_code, 200)

    def test_index_url(self):
        response = self.client.get('/startfundraiser/index/')
        self.assertEqual(response.status_code, 200)

    def test_posts_url(self):
        response = self.client.get('/startfundraiser/posts/')
        self.assertEqual(response.status_code, 200)

 #models testing


class TestCampaignModels(TestCase):
    def test_campaign_title_representation(self):
        campaign_title = Campaign(campaign_Title="My entry title")
        self.assertEqual(str(campaign_title), campaign_title.campaign_Title)


class TestFaqsModels(TestCase):
    def test_question_representation(self):
        question = Faqs(question="")
        self.assertEqual(str(question), question.question)


class TestUpdateModels(TestCase):
    def test_text_title_representation(self):
        text = Update(text="My entry title")
        self.assertEqual(str(text), text.text)


class TestPostModels(TestCase):
    def test_title_representation(self):
        title = Post(title="My entry title")
        self.assertEqual(str(title), title.title)


class TestcommentModels(TestCase):
    def test_content_representation(self):
        content = comment(content="My entry title")
        self.assertEqual(str(content), content.content)


class TestreplyModels(TestCase):
    def test_date_representation(self):
        date = reply(date="12/12/2018")
        self.assertEqual(str(date), date.date)


class TestBackersModels(TestCase):
    def test_amount_representation(self):
        amount = Backers(amount="1.02")
        self.assertEqual(str(amount), amount.amount)
