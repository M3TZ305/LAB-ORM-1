from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from .models import Post


class PostModelTests(TestCase):
    def test_post_creation_and_attributes(self):
        post = Post.objects.create(
            title="تدوينة تجريبية",
            content="محتوى تفصيلي للتدوينة التجريبية."
        )
        self.assertEqual(post.title, "تدوينة تجريبية")
        self.assertEqual(post.content, "محتوى تفصيلي للتدوينة التجريبية.")
        self.assertTrue(post.is_published)
        self.assertIsNotNone(post.published_at)
        self.assertLessEqual(post.published_at, timezone.now())
        self.assertEqual(str(post), "تدوينة تجريبية")

    def test_title_max_length(self):
        max_title = "أ" * 2048
        post = Post.objects.create(title=max_title, content="محتوى")
        self.assertEqual(len(post.title), 2048)
        self.assertEqual(Post.objects.get(id=post.id).title, max_title)


class BlogViewsTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.post1 = Post.objects.create(
            title="أول تدوينة عن بايثون",
            content="بايثون لغة برمجة قوية وممتعة للجميع."
        )
        self.post2 = Post.objects.create(
            title="تعلم إطار عمل دجانغو",
            content="دجانغو يساعدك على بناء تطبيقات ويب سريعة."
        )
        self.unpublished_post = Post.objects.create(
            title="مسودة غير منشورة",
            content="هذه التدوينة مسودة سرية لا يجب أن تظهر للعامة.",
            is_published=False
        )

    def test_homepage_accessible_and_status(self):
        response = self.client.get(reverse('blog:home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/home.html')
        self.assertTemplateUsed(response, 'blog/base.html')

    def test_homepage_displays_published_posts_only(self):
        response = self.client.get(reverse('blog:home'))
        self.assertContains(response, self.post1.title)
        self.assertContains(response, self.post2.title)
        self.assertNotContains(response, self.unpublished_post.title)

    def test_posts_ordering_newest_first(self):
        response = self.client.get(reverse('blog:home'))
        posts_in_context = list(response.context['posts'])
        self.assertEqual(posts_in_context[0].id, self.post2.id)
        self.assertEqual(posts_in_context[1].id, self.post1.id)

    def test_add_post_page_accessible(self):
        response = self.client.get(reverse('blog:add_post'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/add_post.html')

    def test_valid_post_submission_creates_record(self):
        initial_count = Post.objects.count()
        data = {
            'title': 'تدوينة مضافة عبر الاستمارة',
            'content': 'محتوى التدوينة الجديدة.'
        }
        response = self.client.post(reverse('blog:add_post'), data)
        self.assertRedirects(response, reverse('blog:home'))
        self.assertEqual(Post.objects.count(), initial_count + 1)
        new_post = Post.objects.get(title='تدوينة مضافة عبر الاستمارة')
        self.assertTrue(new_post.is_published)
        self.assertIsNotNone(new_post.published_at)

    def test_invalid_submission_does_not_create_record(self):
        initial_count = Post.objects.count()
        data = {'title': '', 'content': ''}
        response = self.client.post(reverse('blog:add_post'), data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Post.objects.count(), initial_count)
        self.assertTrue(response.context['form'].errors)

    def test_post_detail_valid_id(self):
        response = self.client.get(reverse('blog:post_detail', args=[self.post1.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.post1.title)
        self.assertContains(response, self.post1.content)
        self.assertTemplateUsed(response, 'blog/post_detail.html')

    def test_post_detail_invalid_id_returns_404(self):
        response = self.client.get(reverse('blog:post_detail', args=[9999]))
        self.assertEqual(response.status_code, 404)

    def test_post_detail_unpublished_returns_404(self):
        response = self.client.get(reverse('blog:post_detail', args=[self.unpublished_post.id]))
        self.assertEqual(response.status_code, 404)

    def test_search_query_parameter(self):
        response = self.client.get(reverse('blog:home'), {'search': 'دجانغو'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.post2.title)
        self.assertNotContains(response, self.post1.title)

    def test_sort_query_parameter(self):
        response_oldest = self.client.get(reverse('blog:home'), {'sort': 'oldest'})
        posts_oldest = list(response_oldest.context['posts'])
        self.assertEqual(posts_oldest[0].id, self.post1.id)
        self.assertEqual(posts_oldest[1].id, self.post2.id)

        response_latest = self.client.get(reverse('blog:home'), {'sort': 'latest'})
        posts_latest = list(response_latest.context['posts'])
        self.assertEqual(posts_latest[0].id, self.post2.id)
        self.assertEqual(posts_latest[1].id, self.post1.id)

    def test_theme_cookie_persistence(self):
        response = self.client.post(reverse('blog:set_theme', args=['dark']))
        self.assertIn('theme', response.cookies)
        self.assertEqual(response.cookies['theme'].value, 'dark')

        self.client.cookies['theme'] = 'dark'
        home_res = self.client.get(reverse('blog:home'))
        self.assertEqual(home_res.context['theme'], 'dark')
        self.assertContains(home_res, 'data-theme="dark"')

    def test_invalid_theme_cookie_rejected_safely(self):
        response = self.client.post(reverse('blog:set_theme', args=['invalid_theme_value']))
        self.assertEqual(response.cookies['theme'].value, 'light')

        self.client.cookies['theme'] = 'malicious_value'
        home_res = self.client.get(reverse('blog:home'))
        self.assertEqual(home_res.context['theme'], 'light')

    def test_template_inheritance_and_named_url_resolving(self):
        home_url = reverse('blog:home')
        add_url = reverse('blog:add_post')
        detail_url = reverse('blog:post_detail', args=[self.post1.id])
        self.assertIn(home_url, ['/', '/ar/', '/en/'])
        self.assertIn(add_url, ['/add/', '/ar/add/', '/en/add/'])
        self.assertIn(detail_url, [f'/post/{self.post1.id}/', f'/ar/post/{self.post1.id}/', f'/en/post/{self.post1.id}/'])

    def test_arabic_and_english_localization(self):
        # Arabic homepage
        res_ar = self.client.get('/ar/')
        self.assertEqual(res_ar.status_code, 200)
        self.assertContains(res_ar, 'dir="rtl"')
        self.assertContains(res_ar, 'lang="ar"')
        self.assertContains(res_ar, 'SIYAQ')
        self.assertContains(res_ar, 'سِياق')

        # English homepage
        res_en = self.client.get('/en/')
        self.assertEqual(res_en.status_code, 200)
        self.assertContains(res_en, 'dir="ltr"')
        self.assertContains(res_en, 'lang="en"')
        self.assertContains(res_en, 'SIYAQ')
        self.assertContains(res_en, 'Home')
        self.assertContains(res_en, 'Add Post')
