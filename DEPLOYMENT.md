# نشر مشروع mhesham على Linux باستخدام Docker

هذا المشروع يعمل بـ Django وGunicorn على المنفذ الداخلي `8000`. يشغّل Compose قاعدة PostgreSQL خاصة ودائمة، ويحفظ ملفات الرفع في Docker volume دائم. لا يُنشر منفذ التطبيق على الإنترنت افتراضيًا؛ يصل إليه Nginx داخل Docker عبر شبكة مشتركة واسم `mhesham-web`.

## متطلبات السيرفر

- Docker Engine
- Docker Compose Plugin (`docker compose`)
- Git
- Nginx وCertbot بحسب بنية السيرفر (لا يتم تشغيلهما داخل هذا المشروع)

## القيم التي يجب ضبطها

بعد نسخ `.env.example` إلى `.env` غيّر القيم التالية على الأقل:

- `SECRET_KEY`: قيمة طويلة وفريدة. يمكن توليدها بالأمر الموضح أدناه.
- `ALLOWED_HOSTS`: الدومين فقط من دون protocol.
- `CSRF_TRUSTED_ORIGINS`: عناوين HTTPS كاملة.
- `DB_PASSWORD`: كلمة مرور قوية لقاعدة PostgreSQL.
- `PROXY_NETWORK_NAME`: اسم شبكة Nginx المشتركة؛ القيمة الافتراضية `proxy_network`.
- إعدادات البريد إذا أردت إرسال رسائل فعلية. الإعداد الافتراضي يكتب البريد في logs فقط.

اترك `DEBUG=False` في الإنتاج. أبقِ `SERVE_MEDIA=True` عندما يكون Nginx منفصلًا ولا يستطيع mount للـ media volume؛ سيخدم Django الوسائط من الـ volume. في بنية تخزين خارجي أو Nginx يستطيع قراءة الـ volume، اضبطها إلى `False`.

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

انسخ `deploy/nginx.example.conf` إلى إعدادات Nginx، واستبدل `YOUR_DOMAIN`. يجب أن تكون حاوية Nginx متصلة أيضًا بالشبكة الخارجية نفسها؛ عندها سيعمل:

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

Docker DNS مثل `mhesham-web` لا يعمل من host. استخدم ملف override المرفق لينشر التطبيق على loopback فقط:

```bash
docker compose -p mhesham -f docker-compose.yml -f docker-compose.host-nginx.yml up -d --build
```

ثم غيّر `proxy_pass` في إعداد Nginx إلى:

```nginx
proxy_pass http://127.0.0.1:8000;
```

لا تغيّر الربط إلى `0.0.0.0:8000`؛ loopback يمنع كشف Gunicorn مباشرة للإنترنت.

## HTTPS

بعد توجيه DNS وتفعيل إعداد HTTP الصحيح، يمكن إصدار الشهادة إذا كان Certbot مثبتًا على host:

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
