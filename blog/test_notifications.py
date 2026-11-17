from django.test import TestCase
from blog.models import Post
from blog.test_crud import DATA


class NotificationTests(TestCase):
    def test_create_feedback(self):
        response = self.client.post('/add/', DATA, follow=True)
        self.assertContains(response, 'تم نشر المقال بنجاح.')
        self.assertContains(response, 'data-autohide="true"')
        self.assertContains(response, 'data-toast-close')

    def test_edit_feedback_once_after_redirect(self):
        post = Post.objects.create(**DATA)
        response = self.client.post(f'/post/{post.pk}/edit/', {
            **DATA, 'title': 'عنوان معدل للاختبار',
        }, follow=True)
        self.assertRedirects(response, '/home/')
        self.assertContains(response, 'تم تعديل المقال بنجاح.')
        self.assertNotContains(self.client.get('/home/'), 'تم تعديل المقال بنجاح.')

    def test_delete_feedback_once_after_redirect(self):
        post = Post.objects.create(**DATA)
        response = self.client.post(f'/post/{post.pk}/delete/', follow=True)
        self.assertContains(response, 'تم حذف المقال بنجاح.')
        self.assertNotContains(self.client.get('/home/'), 'تم حذف المقال بنجاح.')

    def test_invalid_edit_has_no_success_notification(self):
        post = Post.objects.create(**DATA)
        response = self.client.post(f'/post/{post.pk}/edit/', {**DATA, 'title': ''})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['form'].errors)
        self.assertNotContains(response, 'تم تعديل المقال بنجاح.')
