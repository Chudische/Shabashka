import unittest
from selenium import webdriver

from .. import models

class SingUpTestCase(unittest.TestCase):

    def setUp(self):        
        self.driver = webdriver.Chrome()
            

    def test_1_success(self):
        self.driver.get('http://localhost:8000/accounts/register/')
        self.driver.find_element_by_id('id_username').send_keys('test_user_0')
        self.driver.find_element_by_id('id_email').send_keys('test@mail.com')
        self.driver.find_element_by_id('id_password1').send_keys('test_password')
        self.driver.find_element_by_id('id_password2').send_keys('test_password')        
        self.driver.find_element_by_id('id_submit').click()
        self.assertIn('http://localhost:8000/accounts/register/done',  self.driver.current_url)       
        try:
            self.test_user = models.ShaUser.objects.get(username='test_user_0')
        except models.ShaUser.DoesNotExist:
            self.test_user = None                
        self.test_user.is_activated = True
        self.test_user.save()
    
    def test_2_password_missmatch(self):
        self.driver.get('http://localhost:8000/accounts/register/')
        self.driver.find_element_by_id('id_username').send_keys('test_user_1')
        self.driver.find_element_by_id('id_email').send_keys('test@mail.com')
        self.driver.find_element_by_id('id_password1').send_keys('test_password')
        self.driver.find_element_by_id('id_password2').send_keys('test_password1')        
        self.driver.find_element_by_id('id_submit').click()
        self.assertIn('http://localhost:8000/accounts/register',  self.driver.current_url)

    def tearDown(self):        
        self.driver.close()

    @classmethod
    def tearDownClass(cls):
        cls.test_user = models.ShaUser.objects.get(username='test_user_0')
        cls.test_user.delete()


class LoginTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome()
        cls.driver.get('http://localhost:8000/accounts/register/')
        cls.driver.find_element_by_id('id_username').send_keys('test_user_0')
        cls.driver.find_element_by_id('id_email').send_keys('test@mail.com')
        cls.driver.find_element_by_id('id_password1').send_keys('test_password')
        cls.driver.find_element_by_id('id_password2').send_keys('test_password')        
        cls.driver.find_element_by_id('id_submit').click()
        cls.test_user = models.ShaUser.objects.get(username='test_user_0')
        cls.test_user.is_activated = True
        cls.test_user.save()
        cls.driver.close()

    def setUp(self):        
        self.driver = webdriver.Chrome()


    def test_1_success(self):
        self.driver.get('http://localhost:8000/accounts/login/')
        self.driver.find_element_by_id('id_username').send_keys('test_user_0')
        self.driver.find_element_by_id('id_password').send_keys('test_password')
        self.driver.find_element_by_id('id_submit').click()
        self.assertIn('http://localhost:8000/', self.driver.current_url)
        self.test_user = models.ShaUser.objects.get(username='test_user_0')
        self.assertTrue(self.test_user.is_authenticated)

    def tearDown(self):        
        self.driver.close()

    @classmethod
    def tearDownClass(cls):
        cls.test_user = models.ShaUser.objects.get(username='test_user_0')
        cls.test_user.delete()
    

if __name__ == '__main__':
    unittest.main()

    