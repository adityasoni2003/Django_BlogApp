from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
# Create your tests here.
from .models import Post


class BlogTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username='testuser',password='secret'
        )
        cls.post = Post.objects.create(
            title="A test Title",
            body="i am very smart boyi am very smart boyi am very smart boyi am very smart boyi am very smart boyi am very smart boyi am very smart boyi am very smart boy",
            author=cls.user
        )
    
    def test_post_model(self):
        self.assertEqual(self.post.title,"A test Title")
        self.assertEqual(self.post.body,"i am very smart boyi am very smart boyi am very smart boyi am very smart boyi am very smart boyi am very smart boyi am very smart boyi am very smart boy")
        self.assertEqual(self.post.author.username,"testuser")
        self.assertEqual(str(self.post),"A test Title")
        self.assertEqual(self.post.get_absolute_url(),'/post/1')
    
    def test_url_exists_listview(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code , 200)
    def test_url_exists_detailview(self):
        response = self.client.get("/post/1")
        self.assertEqual(response.status_code,200)
    
    def test_post_listview(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code,200)
        # self.assertContains(response,"A test Title")
        self.assertTemplateUsed(response,"home.html")
    
    def test_post_detailview(self):
        response = self.client.get(reverse("post_detail",kwargs={"pk":self.post.pk}))
        no_response = self.client.get(self.client.get("post/121"))
        
        
        self.assertEqual(response.status_code,200)
        self.assertEqual(no_response.status_code,404)
        
        self.assertContains(response,"A test Title")
        self.assertTemplateUsed(response,"post_detail.html")
    
    def test_post_createview(self):
        response = self.client.post(
            reverse('post_new'),
            {"title":"New Title","body":"A new body","author":self.user.id}
            
        )
        self.assertEqual(response.status_code,302)
        self.assertEqual(Post.objects.last().title,"New Title")
        self.assertEqual(Post.objects.last().body,"A new body")
    
    def test_post_updateview(self):
        response = self.client.post(
            reverse("post_edit",args='1'),
            {"title":'new updated title',"body":'new updated body'}
        )
        self.assertEqual(response.status_code,302)
        self.assertEqual(Post.objects.last().title,"new updated title")
        self.assertEqual(Post.objects.last().body,"new updated body")
    
    def test_post_deleteview(self):
        response = self.client.post(reverse("post_delete",args="1"))
        self.assertEqual(response.status_code,302)
        
        