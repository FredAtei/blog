import unittest
from app.models import User,Comment
from app import db


class Commenttest(unittest.TestCase):
    def setUp(self):
        self.user_charles = User(username='fred', password='goat', email='test@test.com')
        self.new_blog = Comment(id=1, title='Test', content='This is a test blog', user_id=self.user_fred.id)

    def test_save_blog(self):
        self.new_blog.save()
        self.assertTrue(len(Comment.query.all()) > 0)    

    def test_get_comment(self):
        self.new_blog.save()
        get_comment = Comment.get_blog(1)
        self.assertTrue(get_comment is not None)

    def tearDown(self):
        Comment.query.delete()
        User.query.delete() 