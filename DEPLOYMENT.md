# نشر مشروع mhesham على Linux باستخدام Docker

هذا المشروع يعمل بـ Django وGunicorn على المنفذ الداخلي `8000`. يشغّل Compose قاعدة PostgreSQL خاصة ودائمة، ويحفظ ملفات الرفع في Docker volume دائم. لا يُنشر منفذ التطبيق على الإنترنت افتراضيًا؛ يصل إليه Nginx داخل Docker عبر شبكة مشتركة واسم `mhesham-web`.

## متطلبات السيرفر

- Docker Engine
- Docker Compose Plugin (`docker compose`)
- Git
- Nginx وCertbot بحسب بنية السيرفر (لا يتم تشغيلهما داخل هذا المشروع)

## التشغيل الحالي بدون دومين

يمكن تشغيل الموقع عبر عنوان IP العام للسيرفر وبروتوكول HTTP. استبدل `SERVER_IP` في `.env` وملف Nginx بعنوان السيرفر الفعلي، مثل `203.0.113.10`. لا تضف `http://` داخل `ALLOWED_HOSTS`.

الإعدادات الحالية المقصودة لهذه المرحلة هي:

```env
DEBUG=False
ALLOWED_HOSTS=SERVER_IP
CSRF_TRUSTED_ORIGINS=http://SERVER_IP
SECURE_SSL_REDIRECT=False
SESSION_COOKIE_SECURE=False
CSRF_COOKIE_SECURE=False
SECURE_HSTS_SECONDS=0
```

بهذا يمكن فتح الموقع على `http://SERVER_IP/` وتعمل جلسات لوحة التحكم والنماذج من دون شهادة SSL.

## العمل بجانب موقع Django موجود بالفعل

لا تغيّر إعداد الموقع الموجود ولا توقف حاوياته. هذا المشروع معزول كالتالي:

- اسم Compose مستقل: `mhesham`.
- حاويات وvolumes بأسماء تبدأ بـ `mhesham`.
- alias فريد داخل شبكة Nginx: `mhesham-web`.
- PostgreSQL موجود على شبكة داخلية ولا يشارك الموقع الآخر.
- لا يوجد نشر لمنفذ Gunicorn على host في السيناريو الأساسي.

إذا كان Nginx الحالي داخل Docker، اعرف اسم شبكته الحالية:

```bash
docker inspect NGINX_CONTAINER_NAME --format '{{range $name, $_ := .NetworkSettings.Networks}}{{$name}}{{println}}{{end}}'
```

ضع اسم الشبكة الناتج في `PROXY_NETWORK_NAME` بدل إنشاء شبكة جديدة. إذا كانت الشبكة المناسبة موجودة بالفعل، لا تنفذ `docker network create`. إعداد الموقع القديم يبقى كما هو، وأضف Server Block جديدًا فقط لهذا المشروع يستخدم:

```nginx
server_name SERVER_IP;
proxy_pass http://mhesham-web:8000;
```

وجود موقع آخر له `server_name` خاص بالدومين لا يتعارض مع Server Block الخاص بعنوان IP؛ Nginx يختار الموقع حسب قيمة `Host` في الطلب.

## القيم التي يجب ضبطها

بعد نسخ `.env.example` إلى `.env` غيّر القيم التالية على الأقل:

- `SECRET_KEY`: قيمة طويلة وفريدة. يمكن توليدها بالأمر الموضح أدناه.
- `ALLOWED_HOSTS`: عنوان IP العام فقط في المرحلة الحالية، من دون `http://`.
- `CSRF_TRUSTED_ORIGINS`: العنوان الكامل مثل `http://SERVER_IP`.
- `DB_PASSWORD`: كلمة مرور قوية لقاعدة PostgreSQL.
- `PROXY_NETWORK_NAME`: اسم شبكة Nginx المشتركة؛ القيمة الافتراضية `proxy_network`.
- `MHESHAM_HOST_PORT`: منفذ loopback مخصص لهذا المشروع عند تشغيل Nginx على host؛ الافتراضي `8001` لتجنب تعارض شائع مع الموقع الآخر.
- إعدادات البريد إذا أردت إرسال رسائل فعلية. الإعداد الافتراضي يكتب البريد في logs فقط.

اترك `DEBUG=False` في الإنتاج. اترك إعدادات SSL وsecure cookies معطلة حتى تركيب الدومين والشهادة. أبقِ `SERVE_MEDIA=True` عندما يكون Nginx منفصلًا ولا يستطيع mount للـ media volume؛ سيخدم Django الوسائط من الـ volume. في بنية تخزين خارجي أو Nginx يستطيع قراءة الـ volume، اضبطها إلى `False`.

## النشر الأول — Nginx داخل Docker (المسار المفضل)

```bash
cd /var/www
git clone REPOSITORY_URL mhesham
cd mhesham
cp .env.example .env
python3 -c 'import secrets; print(secrets.token_urlsafe(64))'
nano .env
```

افحص الشبكات، وأنشئ الشبكة فقط إن لم تكن موجودة:

```bash
docker network ls
docker network inspect proxy_network >/dev/null 2>&1 || docker network create proxy_network
```

إذا غيّرت `PROXY_NETWORK_NAME` فاستخدم الاسم نفسه بدل `proxy_network` في الأمر السابق وفي Compose الخاص بـ Nginx.

ابنِ وشغّل الخدمات، ثم نفّذ مهام Django صراحة بعد التشغيل:

```bash
docker compose -p mhesham config
docker compose -p mhesham build
docker compose -p mhesham up -d
docker compose -p mhesham exec web python manage.py migrate
docker compose -p mhesham exec web python manage.py collectstatic --noinput
docker compose -p mhesham exec web python manage.py check --deploy
docker compose -p mhesham ps
docker compose -p mhesham logs --tail=100 web
```

لإنشاء مستخدم إدارة عند الحاجة:

```bash
docker compose -p mhesham exec web python manage.py createsuperuser
```

انسخ `deploy/nginx.example.conf` إلى إعدادات Nginx، واستبدل `SERVER_IP` بعنوان IP العام. يجب أن تكون حاوية Nginx متصلة أيضًا بالشبكة الخارجية نفسها؛ عندها سيعمل:

```nginx
proxy_pass http://mhesham-web:8000;
```

اختبر إعداد Nginx ثم أعد تحميله بالطريقة المناسبة لطريقة تشغيله. إذا كان Nginx داخل Compose آخر، تكون الأوامر عادةً شبيهة بـ:

```bash
docker network connect proxy_network NGINX_CONTAINER_NAME
docker exec NGINX_CONTAINER_NAME nginx -t
docker exec NGINX_CONTAINER_NAME nginx -s reload
```

الأمر الأول مطلوب مرة واحدة فقط إذا لم تكن خدمة Nginx مرتبطة بالشبكة في ملف Compose الخاص بها.

## إذا كان Nginx مثبتًا على الـ host

Docker DNS مثل `mhesham-web` لا يعمل من host. استخدم ملف override المرفق لينشر التطبيق على loopback فقط. المنفذ الافتراضي لهذا المشروع هو `8001` وليس `8000` لتجنب التعارض مع الموقع الموجود:

```bash
docker compose -p mhesham -f docker-compose.yml -f docker-compose.host-nginx.yml up -d --build
```

ثم غيّر `proxy_pass` في إعداد Nginx إلى:

```nginx
proxy_pass http://127.0.0.1:8001;
```

إذا كان `8001` مستخدمًا أيضًا، غيّر `MHESHAM_HOST_PORT` في `.env` إلى منفذ loopback حر، واستخدم القيمة نفسها في `proxy_pass`. لا تغيّر الربط إلى `0.0.0.0`؛ loopback يمنع كشف Gunicorn مباشرة للإنترنت.

## إضافة الدومين وHTTPS لاحقًا

بعد توجيه DNS إلى السيرفر، غيّر القيم التالية:

```env
ALLOWED_HOSTS=YOUR_DOMAIN,www.YOUR_DOMAIN
CSRF_TRUSTED_ORIGINS=https://YOUR_DOMAIN,https://www.YOUR_DOMAIN
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
SECURE_HSTS_SECONDS=31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS=True
SECURE_HSTS_PRELOAD=True
```

وغيّر `server_name` في Nginx إلى `YOUR_DOMAIN www.YOUR_DOMAIN`. بعد التأكد أن الموقع يعمل عبر HTTP، يمكن إصدار الشهادة إذا كان Certbot مثبتًا على host:

```bash
sudo certbot --nginx -d YOUR_DOMAIN -d www.YOUR_DOMAIN
```

طريقة SSL الفعلية تعتمد على مكان تشغيل Nginx وCertbot. إذا كان Nginx داخل Docker، استخدم آلية الشهادات الخاصة بذلك الـ stack. لا تُشغّل Certbot محليًا في هذا المشروع.

## التحديثات اللاحقة

من داخل `/var/www/mhesham`:

```bash
git pull
docker compose -p mhesham up -d --build
docker compose -p mhesham exec web python manage.py migrate
docker compose -p mhesham exec web python manage.py collectstatic --noinput
docker compose -p mhesham exec web python manage.py check --deploy
docker compose -p mhesham ps
docker compose -p mhesham logs --tail=100 web
```

في سيناريو Nginx على host، أضف ملف override إلى أمر `up`:

```bash
docker compose -p mhesham -f docker-compose.yml -f docker-compose.host-nginx.yml up -d --build
```

## الفحص واستكشاف المشاكل

```bash
docker compose -p mhesham ps
docker compose -p mhesham logs -f web
docker compose -p mhesham logs --tail=100 db
docker network inspect proxy_network
docker inspect mhesham-web-1
docker compose -p mhesham exec web python manage.py check
docker compose -p mhesham exec web python manage.py showmigrations
docker compose -p mhesham exec web python -c "import socket; socket.create_connection(('127.0.0.1', 8000), 3); print('web port OK')"
```

ومن حاوية Nginx المتصلة بالشبكة يمكن اختبار الوصول، بحسب الأدوات المتاحة في image:

```bash
docker exec NGINX_CONTAINER_NAME wget -qO- http://mhesham-web:8000/ >/dev/null && echo OK
```

حالة `healthy` تعني أن Gunicorn يقبل اتصالات TCP. افحص logs إذا كانت الخدمة `unhealthy`. لا تستخدم `docker compose down -v` في الإنتاج؛ الخيار `-v` يحذف volumes وقاعدة البيانات والوسائط.

## النسخ الاحتياطي

قبل التحديثات الكبيرة، خذ نسخة PostgreSQL:

```bash
docker compose -p mhesham exec -T db pg_dump -U portfolio portfolio > mhesham-backup.sql
```

إذا غيّرت `DB_USER` أو `DB_NAME` فاستخدم القيم الفعلية بدل `portfolio`. كما يجب نسخ volume الوسائط احتياطيًا وفق سياسة النسخ الاحتياطي على السيرفر.

## ملاحظة عن البيانات المحلية الحالية

التطوير المحلي الافتراضي يستخدم `db.sqlite3` عند غياب `DB_HOST` و`DATABASE_URL`. نشر Docker يستخدم PostgreSQL جديدًا ودائمًا؛ migrations تنشئ الجداول لكنها لا تنقل بيانات SQLite تلقائيًا. إذا كانت البيانات المحلية مطلوبة في الإنتاج، صدّرها واستوردها بخطة ترحيل بيانات منفصلة قبل فتح الموقع.
