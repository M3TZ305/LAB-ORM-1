# 📝 Blogger — مشروع معمل LAB-ORM-1

مشروع تطبيقي متكامل لبناء منصة تدوين باستخدام إطار العمل **Django**، تم إنشاؤه وتطويره لتغطية وتطبيق كافة مفاهيم المساق الأكاديمي المتعلقة بهيكلية MVT، ووراثة القوالب، وملفات Static، واستبانة الروابط، ونظام إدارة قواعد البيانات Django ORM، والهجرات (Migrations)، ومعاملات المسار والاستعلام (Path & Query Parameters)، وتفضيلات المستخدم عبر ملفات تعريف الارتباط (Cookies).

---

## 📋 نظرة عامة على المشروع (Project Overview)

موقع **Blogger** هو تطبيق ويب يتيح للمستخدمين:
- استعراض أحدث التدوينات المنشورة مع عرض العنوان والمحتوى وتاريخ ووقت النشر بالتوقيت المحلي (`Asia/Riyadh`).
- إضافة تدوينات جديدة عبر استمارة تفاعلية محمية ضد هجمات تزوير الطلبات عبر المواقع (CSRF).
- استعراض التفاصيل الكاملة لأي تدوينة منشورة عبر رابط فريد يعتمد على المعرّف (`id`).
- البحث في العناوين ومحتوى المقالات وتصفيتها بالترتيب (الأحدث أولاً / الأقدم أولاً).
- التبديل الفوري بين المظهر الفاتح (Light Mode) والمظهر الداكن (Dark Mode) مع حفظ التفضيل داخل كوكي المتصفح (`theme`) لمدة 30 يوماً.

---

## 🛠️ إعداد البيئة الافتراضية (Environment Setup)

تم إنشاء واستخدام بيئة افتراضية معزولة باسم `.venv` لضمان عدم تثبيت الحزم على مستوى النظام العالمي.

### على أنظمة Windows (PowerShell):
```powershell
# إنشاء البيئة الافتراضية
python -m venv .venv

# تفعيل البيئة الافتراضية
.\.venv\Scripts\Activate.ps1
```

### على أنظمة Linux / macOS:
```bash
# إنشاء البيئة الافتراضية
python3 -m venv .venv

# تفعيل البيئة الافتراضية
source .venv/bin/activate
```

---

## 📦 تثبيت الاعتماديات (Dependencies)

تثبيت الاعتماديات الخاصة بالمشروع باستخدام ملف `requirements.txt`:

```bash
# ترقية مدير الحزم pip
python -m pip install --upgrade pip

# تثبيت الحزم المطلوبة
python -m pip install -r requirements.txt
```

---

## 🚀 تشغيل المشروع (Project Execution)

لتشغيل خادم التطوير المحلي:

```bash
python manage.py runserver
```

بعد التشغيل، يمكنك فتح المتصفح والتوجه إلى الرابط:
[http://127.0.0.1:8000/](http://127.0.0.1:8000/)

---

## 🗺️ خريطة مفاهيم المساق ومواضع تطبيقها (Course Concepts Mapping)

| المفهوم (Concept) | الملف المنفّذ فيه (File) | طريقة التطبيق والهدف (Implementation Details) |
|---|---|---|
| **Apps & Views** | `blog/views.py` | تم استخدام Function-based Views (`home`, `add_post`, `post_detail`, `set_theme`) لإبقاء الشيفرة واضحة ومباشرة للتعلم. |
| **Templates** | `blog/templates/blog/` | استخدام وسوم قوالب دجانغو مثل `{% if %}`, `{% for %}`, `{{ variable }}`, `{% url %}`, `{% load static %}` مع ميزة الهروب التلقائي للرموز (Auto-escaping). |
| **Static Files** | `blog/static/blog/css/style.css` و `main.js` | إدارة وتضمين ملفات التنسيق والجافاسكريبت محلياً دون الاعتماد على مكتبات خارجية. |
| **Resolving URLs** | `blog/templates/blog/*.html` و `views.py` | استبانة الروابط ديناميكياً باستخدام الوسم `{% url 'blog:route_name' %}` والدوال `redirect` و `reverse`. |
| **MVT Architecture** | كامل مجلد `blog/` | تطبيق فصل المسؤوليات بالكامل: Model (`models.py`) ➔ View (`views.py`) ➔ Template (`templates/`). |
| **URL Mapping** | `blog/urls.py` و `blogger_project/urls.py` | توجيه المسارات باستخدام `path()` وتضمينها عبر `include()` مع تحديد مساحة الأسماء `app_name = "blog"`. |
| **Template Inheritance** | `blog/templates/blog/base.html` | توحيد الهيكل المشترك والشريط العلوي والتذييل والروابط وتوريثها لجميع الصفحات عبر `{% extends "blog/base.html" %}`. |
| **Cookies** | `blog/views.py` (`set_theme`, `home`, `add_post`) | قراءة تفضيل مظهر الموقع عبر `request.COOKIES.get('theme')` وحفظه عبر `response.set_cookie` بصلاحية 30 يوماً وإعداد `samesite='Lax'`. |
| **Path Parameters** | `blog/urls.py` و `blog/views.py` | استخراج المتغيرات من مسار الرابط مثل `post/<int:post_id>/` لتفاصيل التدوينة و `theme/<str:mode>/` لتحديد النمط. |
| **Query Parameters** | `blog/views.py` (`home`) | قراءة معاملات الاستعلام من الرابط `request.GET.get('search')` للبحث و `request.GET.get('sort')` لتحديد نمط الترتيب بأمان. |
| **Django ORM** | `blog/views.py` و `blog/models.py` | إدارة بيانات التدوينات بواسطة استعلامات كائنية بدلاً من Raw SQL عبر دوال `filter`, `order_by`, `get_object_or_404`, `create`. |
| **Django Migrations** | `blog/migrations/0001_initial.py` | تتبع التغييرات على بنية النموذج البرمجي وترجمتها إلى جداول SQL وتطبيقها على قاعدة البيانات `db.sqlite3`. |

---

## 🗄️ شرح عمليات الـ ORM (Django ORM Explanation)

تم تطبيق جميع عمليات الاسترجاع والتخزين عبر الـ ORM المدمج:
1. **إنشاء التدوينات (Create):**
   يتم حفظ التدوينة عبر استمارة `PostForm` أو برمجياً باستخدام `Post.objects.create(title=..., content=...)`، مع إسناد القيمة `True` لحقل `is_published` تلقائياً.
2. **استرجاع التدوينات المنشورة فقط (Filter):**
   ```python
   posts = Post.objects.filter(is_published=True)
   ```
3. **الترتيب الأحدث أولاً (Ordering):**
   ```python
   posts = posts.order_by('-published_at', '-id')
   ```
   وفي حال اختيار الأقدم:
   ```python
   posts = posts.order_by('published_at', 'id')
   ```
4. **البحث في العنوان والمحتوى (Search):**
   ```python
   posts = posts.filter(
       Q(title__icontains=search_query) | Q(content__icontains=search_query)
   )
   ```
5. **استرجاع تدوينة محددة مع إرجاع 404 إذا كانت غير موجودة أو غير منشورة:**
   ```python
   post = get_object_or_404(Post, pk=post_id, is_published=True)
   ```

---

## 🔄 شرح الهجرات (Django Migrations Explanation)

الهجرات (Migrations) هي طريقة دجانغو لنقل وتطبيق التعديلات التي تجريها على النماذج (`models.py`) إلى بنية جداول قاعدة البيانات.

### الأوامر المنفذة والغرض منها:
1. `python manage.py makemigrations blog`:
   تقوم بفحص نموذج `Post` وتوليد ملف هجرة جديد (`blog/migrations/0001_initial.py`) يصف التغييرات برمجياً بلغة بايثون دون التأثير على قاعدة البيانات بعد.
2. `python manage.py sqlmigrate blog 0001`:
   تعرض أوامر SQL الدقيقة التي سيقوم دجانغو بتنفيذها على قاعدة البيانات لإنشاء جدول `blog_post`، مما يسمح بمراجعة الاستعلامات قبل تطبيقها.
3. `python manage.py migrate`:
   تنفذ ملفات الهجرة المعلقة على قاعدة البيانات (`db.sqlite3`)، حيث تنشئ الجداول وتعدل الأعمدة وتحدث سجل جدول `django_migrations`.
4. `python manage.py showmigrations blog`:
   تعرض حالة ملفات الهجرة الخاصة بالتطبيق؛ وظهور علامة `[X]` بجانب الهجرة يعني أنها مطبقة بنجاح في قاعدة البيانات.

---

## 🌐 أمثلة الروابط المدعومة في الموقع (URL Examples)

- **الصفحة الرئيسية:**
  `/`
- **صفحة إضافة مقال جديد:**
  `/add/`
- **صفحة تفاصيل المقال (Path Parameter):**
  `/post/1/`
- **البحث باستخدام كلمة مفتاحية (Query Parameter):**
  `/?search=django`
- **الترتيب من الأقدم للأحدث (Query Parameter):**
  `/?sort=oldest`
- **البحث مع الترتيب معاً (Combined Query Parameters):**
  `/?search=django&sort=oldest`
- **تغيير المظهر (Cookies):**
  `/theme/dark/` أو `/theme/light/`

---

## 🧪 التحقق والاختبارات الآلية (Verification & Automated Tests)

لإجراء الفحص الشامل للنظام وتشغيل الاختبارات الآلية المكتوبة:

```bash
# فحص تكامل النظام
python manage.py check

# التحقق من عدم وجود هجرات غير مولدة
python manage.py makemigrations --check --dry-run

# تشغيل الاختبارات الآلية الشاملة
python manage.py test
```

جميع الاختبارات الـ 16 تنفذ بنجاح وتغطي كافة متطلبات النموذج، والحقول، والتحقق، والروابط، والـ ORM، والكوكيز، وحالات الخطأ 404.

---

## 🎓 إرشادات العرض للمشرف الأكاديمي (Lab Presentation Notes)

عند مناقشة المشروع مع أستاذ المادة، يمكن للطالب استعراض المفاهيم عبر الخطوات التالية:
1. **نموذج ORM (`blog/models.py`):** استعراض كلاس `Post` وتوضيح حقل `title` بحد أقصى 2048 حرفاً، وحقل `is_published` بقيمته الافتراضية `True`، وحقل `published_at` المزود بخاصية `auto_now_add=True`.
2. **الهجرات (`blog/migrations/`):** إظهار ملف `0001_initial.py` وشرح كيف تم تحويله إلى جدول بواسطة أمر `migrate` واستعراض الجدول في لوحة تحكم المسؤول أو بواسطة `sqlmigrate`.
3. **وراثة القوالب (`blog/templates/blog/`):** فتح ملف `base.html` وتوضيح الهيكل المشترك وروابط التنسيق، ثم فتح `home.html` و `add_post.html` وتوضيح استخدام `{% extends %}` و `{% block content %}` وتجنب التكرار.
4. **معاملات المسار (`post/<int:post_id>/`):** الدخول إلى أي تدوينة وتوضيح كيف يستقبل العرض `post_id` ويبحث عنه عبر `get_object_or_404`، وتجربة إدخال رقم تدوينة غير موجود لإظهار خطأ 404.
5. **معاملات الاستعلام (`?search=` و `?sort=`):** إجراء بحث وترتيب في الصفحة الرئيسية وتوضيح كيف يقرأ الـ View هذه المعاملات من `request.GET`.
6. **ملفات تعريف الارتباط (Cookies):** الضغط على زر "🌙 مظهر ليلي" في أعلى الصفحة، وتوضيح تغير المظهر وثباته عند التنقل أو تحديث الصفحة، ثم فتح أدوات المطور (F12) في المتصفح وإظهار كوكي `theme` المخزن بقيمة `dark` وصلاحيته لمدة 30 يوماً.
