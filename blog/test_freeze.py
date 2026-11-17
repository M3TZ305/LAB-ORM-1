from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import resolve, reverse
from .models import Post
from .test_crud import DATA


class FreezeRegressionTests(TestCase):
    def setUp(self):
        self.owner = get_user_model().objects.create_user('author', password='test-pass-123')
        self.other = get_user_model().objects.create_user('reader')
        self.post = Post.objects.create(**DATA, owner=self.owner)

    def test_themes_on_all_public_pages(self):
        self.client.force_login(self.owner)
        for mode in ['dark', 'light']:
            response = self.client.post(reverse('blog:set_theme', args=[mode]), {'next': '/articles/'})
            self.assertEqual(response.cookies['theme'].value, mode)
            for path in ['/home/', '/articles/', '/about/', '/add/',
                         f'/post/{self.post.pk}/', f'/post/{self.post.pk}/edit/']:
                page = self.client.get(path)
                self.assertEqual(page.status_code, 200)
                self.assertContains(page, f'data-theme="{mode}"')
                self.assertContains(page, 'lang="ar" dir="rtl"')
        self.assertEqual(self.client.post('/theme/dark/', {'next':'https://evil.example/'}).url, '/home/')

    def test_urls_and_login(self):
        for name, args in [('home', []), ('articles', []), ('post_detail', [self.post.pk]),
                           ('edit_post', [self.post.pk]), ('delete_post', [self.post.pk])]:
            self.assertEqual(resolve(reverse('blog:' + name, args=args)).url_name, name)
        self.assertEqual(self.client.get('/login/').status_code,404)

    def test_edit_cannot_change_publication_time_or_owner(self):
        original_time, owner_id = self.post.published_at, self.post.owner_id
        self.client.force_login(self.owner)
        response = self.client.post(f'/post/{self.post.pk}/edit/', {
            **DATA, 'title':'عنوان معدل صحيح', 'owner':self.other.pk,
            'published_at':'2000-01-01T00:00:00',
        })
        self.assertRedirects(response, '/home/')
        self.post.refresh_from_db()
        self.assertEqual(self.post.published_at, original_time)
        self.assertEqual(self.post.owner_id, owner_id)

    def test_combined_search_sort(self):
        second = Post.objects.create(**{**DATA, 'title':'اختبار بحث آخر'})
        page = self.client.get('/articles/', {'search':'اختبار', 'sort':'oldest'})
        self.assertEqual(list(page.context['posts']), [second, self.post])

    def test_template_escaping(self):
        self.post.title = '<script>alert(1)</script>'
        self.post.save(update_fields=['title'])
        page = self.client.get(f'/post/{self.post.pk}/')
        self.assertContains(page, '&lt;script&gt;')
        self.assertNotContains(page, '<script>alert(1)</script>')

    def test_homepage_limits_query_to_four_articles(self):
        for number in range(6):
            Post.objects.create(**{**DATA, 'title': f'مقال تجريبي إضافي {number}'})
        Post.objects.create(**{**DATA, 'is_published': False})
        response = self.client.get('/home/')
        expected = list(Post.objects.filter(is_published=True).order_by('-published_at', '-id').values_list('pk', flat=True)[:4])
        self.assertEqual([post.pk for post in response.context['posts']], expected)
        self.assertEqual(response.context['posts'].query.high_mark, 4)
        archive = self.client.get('/articles/')
        self.assertEqual(len(archive.context['posts']), 7)
        self.assertEqual(
            [post.pk for post in archive.context['posts']],
            list(Post.objects.filter(is_published=True).order_by('-published_at', '-id').values_list('pk', flat=True)),
        )

    def test_count_before_slicing_and_after_filtering(self):
        for index in range(5):
            Post.objects.create(**{**DATA,'title':f'عنوان مميز {index}'})
        Post.objects.create(**{**DATA,'title':'عنوان مميز مخفي','is_published':False})
        home = self.client.get('/home/')
        self.assertEqual(home.context['total_count'],6)
        self.assertEqual(len(home.context['posts']),4)
        for path in ['/home/','/articles/']:
            page=self.client.get(path,{'search':'مميز'})
            self.assertEqual(page.context['total_count'],5)
            self.assertIsInstance(page.context['total_count'],int)
            self.assertEqual(self.client.get(path,{'search':'غيرموجودبتاتا'}).context['total_count'],0)
