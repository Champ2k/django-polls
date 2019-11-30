
from django.test import LiveServerTestCase
from django.contrib.auth.models import User
from django.utils import timezone
from selenium import webdriver
from seleniumlogin import force_login
from polls.models import Question, Choice
import datetime, time

def create_question(question_text, days):
    """
    Create a question with the given `question_text` and published the
    given number of `days` offset to now (days < 0 for questions published
    in the past, days > 0 for questions published in the future).
    """
    time = timezone.now() + datetime.timedelta(days=days)
    question = Question.objects.create(
        question_text=question_text, pub_date=time)
    return question

class SeleniumTestCase(LiveServerTestCase):
    
    
    def setUp(self):
        self.username = "testuser"
        self.userpass = "123$*HCfjdksla"
        self.user = User.objects.create_user(self.username,password=self.userpass)
        self.question = create_question('Hello?', days=0)
        self.choice = Choice.objects.create(choice_text='world', question=self.question)
        self.browser = webdriver.Chrome(
            executable_path='/Users/zexal/Downloads/chromedriver'
            )
        super(SeleniumTestCase, self).setUp()
    
    def tearDown(self):
        self.browser.close()
        super(SeleniumTestCase, self).tearDown()
    
    def test_find_heading_tag(self):
        self.browser.get(self.live_server_url + '/polls/')
        element = self.browser.find_element_by_tag_name("h2")
        self.assertEquals('Hot Topics', element.text)
    
    def test_find_polls_question(self):
        self.browser.get(self.live_server_url + '/polls/')
        element = self.browser.find_element_by_id(f"{self.question.id}")
        self.assertEquals('Hello?', element.text)
    
    def test_polls_hyperlink(self):
        self.browser.get(self.live_server_url + '/polls/')
        element = self.browser.find_elements_by_tag_name("a")
        element[1].click()
        self.assertEquals(self.browser.current_url, self.live_server_url + '/polls/' + f'{self.question.id}/')

    
    def test_voting_result(self):
        self.browser.get(self.live_server_url + '/accounts/login/')
        self.browser.find_element_by_id("id_username").send_keys(self.username)
        self.browser.find_element_by_id("id_password").send_keys(self.userpass)
        self.browser.find_element_by_id("login").click()
        self.browser.get(self.live_server_url + '/polls/')
        self.browser.find_element_by_tag_name('a').click()
        self.browser.find_element_by_id(f"{self.choice.id}").click()
        self.browser.find_element_by_id('vote').click()
        self.assertEqual(self.browser.current_url, self.live_server_url + '/polls/' + f'{self.question.id}/results/')



        
