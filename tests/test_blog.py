import unittest
from app.models import Blog,User
from app import db


class Blogest(unittest.TestCase):
    def setUp(self):
        self.user_charles = User(username='fred', password='goat', email='test@test.com')
        self.new_blog = Blog(id=1, title='Test', content='This is a test blog', user_id=self.user_fred.id)

    def test_save_blog(self):
        self.new_blog.save()
        self.assertTrue(len(Blog.query.all()) > 0)    

    def test_get_blog(self):
        self.new_blog.save()
        got_blog = Blog.get_blog(1)
        self.assertTrue(get_blog is not None)

    def tearDown(self):
        Blog.query.delete()
        User.query.delete()    
