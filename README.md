<div align="center">

<img src="svg/en/hero.svg" alt="Rahgozar — the night route" width="100%"/>

### Rahgozar · SpiderPanel feature set

**English** · [فارسی 🇮🇷](#-فارسی)

</div>

---

## 💡 What is this build?

**Rahgozar** keeps its original visual identity — the night palette, logo,
dashboard composition, login screen, subscription page, bilingual FA/EN UI,
music and original SVG artwork — while the **feature set is exactly the one of
[SpiderPanel](https://github.com/ndnimanima/SpiderPanel)**.

All Rahgozar-only subsystems were removed. The backend is the SpiderPanel
FastAPI application, with only small compatibility adaptations so the existing
Rahgozar pages (routes, session cookie, state filename, dashboard fields) keep
working unchanged.

### Removed (Rahgozar-only, not part of SpiderPanel)

| Removed area | What went away |
|---|---|
| Telegram Web Proxy / MTProto bridge (TWP) | `twp.py`, built-in `Web Proxy` inbound, `/api/v1/*` sessions, extra WS protocols |
| Tunnel Management (TM) | `tm.py`, graph editor, `/api/tm/*`, `/ws/TM/*` |
| Multi-protocol relays | `relays.py`, VMess / Trojan / Shadowsocks relay inbounds |
| Vercel relay + deploy | `vercel_relay.py`, `deploy/vercel/`, `/api/system/vercel-domain` |
| Cloudflare Worker custom domain | `cloudflare_worker_domain.py`, `/api/system/worker-domain*` |
| Self-update & version polling | `VERSION`, `/api/settings/update*`, `/api/public/version`, update UI |
| External proxy pool / speed test | `/api/proxies*`, proxy tab, speed-test tab |
| Bot extras & panel logs | broadcast, auto backup, daily report, `/api/logs` |
| Provider launcher | `app.py`, `run.py`, Shiprr docs |

The visual layer (`static/index.html`, `static/login.html`, `static/sub.html`,
`static/img/`, `static/musix/`, `static/rahgozar-logo.svg`, `svg/`) keeps its
original design: only the menu entries and panels of the removed features were
deleted, and the two SpiderPanel tabs Rahgozar was missing (**Worker** and
**Telegram Bot / Sell Bot**) were added using Rahgozar's own components, CSS
variables, icons and translations — no SpiderPanel visual assets were copied.

## ✨ Features (SpiderPanel)

| Area | Highlights |
|---|---|
| 👤 Users | Create/manage accounts, traffic quota, expiry, concurrent-IP limits, per-user actions |
| 🔗 Subscriptions | Journey-style subscription page, per-config QR, Base64 copy-all, group subscriptions, optional group password |
| 🛰 Inbounds | VLESS + WS + TLS, XHTTP (`packet-up` / `stream-up` / `stream-one`), Reality with auto keygen, Telegram MTProxy inbound |
| 🧩 Config generator | Node configs, scanned/custom-IP configs, worker configs, status config, parser-friendly links |
| 🌐 Nodes | Node management, health checks, refresh and sync, API-key channel |
| ☁️ Worker | Managed `worker/worker.js` deployment to Cloudflare Pages, KV binding, proxy pool, health-check/heartbeat, auto-sync |
| 🧪 Scanner | TCP / IP / SNI checks, Cloudflare subnets, batch ping, fastest-result helpers, copy-friendly mobile results |
| 🤖 Telegram Bot | Channel Bot (create → publish → cleanup) and Sell Bot (plans, receipts, manual approval, subscription delivery) |
| 🟢 Expiry | Automatic expiration handling and cleanup of expired accounts |
| 🛠 Tools | Runtime info, tunnel/reverse status and creation, help settings, backup/restore, activity/connection stats |
| 🎨 Admin UI | Glassmorphism night/light dashboard, live system/bandwidth stats, FA/EN, original Rahgozar artwork |

## 🏗 Architecture

| Component | File | Role |
|---|---|---|
| Core panel | `main.py` | FastAPI: auth, users, inbounds, subscriptions, config generator, worker, scanner, Telegram bot |
| Subscription page renderer | `public_page.py` | Serves `static/sub.html` for `/p/{uuid_key}` |
| Cloudflare template | `worker/worker.js` | Source deployed as `_worker.js` by the Worker setup |
| Notifications | `notif/` | Event pipeline for the bot |
| Installer | `start.sh` | Interactive VPS installer / systemd service |
| Visual layer | `static/`, `svg/` | Rahgozar UI, artwork, music |

State lives in one JSON file inside `DATA_DIR` (default `/data`), named
`rahgozar_state.json` (a legacy `spider_state.json` is read automatically),
written atomically (tmp + rename).

## 🚀 Quick start

**Railway (recommended):** push the repo → *Deploy from GitHub* → attach a
Volume on `/data` → set env vars. `railway.toml` + `Dockerfile` are ready.

**Docker:**
```bash
docker build -t rahgozar .
docker run -d --name rahgozar -p 8080:8080 -v rahgozar_data:/data rahgozar
```

**VPS:**
```bash
bash start.sh        # interactive installer (systemd service included)
```

**Local development:**
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
DATA_DIR=./data python -m uvicorn main:app --host 0.0.0.0 --port 8080
# open http://127.0.0.1:8080/rahgozar
```

| Env var | Default | Purpose |
|---|---|---|
| `ADMIN_USERNAME` / `ADMIN_PASSWORD` | `admin` / `admin` | Panel login — **change immediately** |
| `DATA_DIR` | `/data` | State & backups |
| `SECRET_KEY` | random-ish default | Session signing key (keep equal across replicas) |
| `RAHGOZAR_PANEL_PUBLIC_URL` / `RAHGOZAR_PANEL_PUBLIC_DOMAIN` | — | Explicit public hostname when it is assigned after deploy |
| `MTPROXY_BIN` / `MTPROXY_WORKERS` | `/usr/local/bin/mtproto-proxy` / `1` | Telegram MTProxy runtime |

The panel listens on fixed port **8080** (`0.0.0.0`). Health probe:
`GET /healthz` → `{"ok": true, ...}`.

## 📄 Public routes

| Route | Purpose |
|---|---|
| `/rahgozar`, `/spider`, `/dashboard` | Admin panel (session required) |
| `/login` | Login page |
| `/link/{uuid}` | Base64 export for direct import / subscription page |
| `/p/{uuid_key}` | Group subscription page |
| `/sub-group/{uuid_key}` | Group subscription export |
| `/api/sub/{uuid_key}` | Per-user subscription data |
| `/api/sub/{uuid_key}/qr` | QR of a config |

## 🛰 Inbound types

| Type | Path | Use case |
|---|---|---|
| VLESS + WS + TLS | `/ws/{uuid}` | Most compatible |
| XHTTP | `/xhttp-siz10/...` | Flaky / high-throughput networks |
| Reality | — | Hardened TLS camouflage, auto keygen |
| Tunnel / Reverse | `/tunnel/{uuid}`, `/reverse/{uuid}` | Worker-fronted paths |
| Telegram MTProxy | — | Official `mtproto-proxy` process per inbound |

---

# 🇮🇷 فارسی

<div align="center"><img src="svg/fa/hero.svg" alt="رهگذر" width="100%"/></div>

## ✦ این نسخه چیست؟

**رهگذر** با همان ظاهر همیشگی خود باقی مانده است: پالت شب، لوگو، چیدمان
داشبورد، صفحهٔ ورود، صفحهٔ اشتراک، رابط دوزبانهٔ فارسی/انگلیسی، موسیقی و
طرح‌های SVG اختصاصی. تنها **امکانات پروژه برابر با
[SpiderPanel](https://github.com/ndnimanima/SpiderPanel)** شده است؛ یعنی
بخش‌های اضافه‌ای که فقط در رهگذر وجود داشت حذف شده و بک‌اند همان برنامهٔ
FastAPI اسپایدرپنل است (با چند سازگاری کوچک برای مسیرها، نشست، نام فایل
وضعیت و آمار داشبورد).

### حذف‌شده‌ها (امکانات اضافهٔ رهگذر)

- پروکسی وب تلگرام (TWP) و اینباند `Web Proxy` به همراه `twp.py`
- مدیریت تونل (TM)، ویرایشگر گراف و `tm.py` / `/api/tm/*`
- رله‌های چندپروتکلی `relays.py` (VMess / Trojan / Shadowsocks)
- رله و استقرار Vercel و دامنهٔ اختصاصی Cloudflare Worker
- بروزرسانی خودکار پنل و نمایش/دریافت نسخه از گیت‌هاب
- استخر پروکسی خارجی و تست سرعت
- ابزارهای اضافهٔ ربات (پیام همگانی، بکاپ خودکار، گزارش روزانه) و لاگ پنل
- لانچر مخصوص هاست (`app.py` / `run.py`) و مستندات اضافه

فایل‌های ظاهری (`static/index.html`، `static/login.html`، `static/sub.html`،
`static/img/`، `static/musix/`، `static/rahgozar-logo.svg` و `svg/`) همان طرح
همیشگی را دارند؛ فقط منوها و پنل‌های مربوط به امکانات بالا برداشته شده و دو تب
**Worker** و **ربات تلگرام / ربات فروش** (که در رهگذر نبود و در SpiderPanel
هست) با همان کامپوننت‌ها، رنگ‌ها، آیکون‌ها و ترجمه‌های رهگذر اضافه شده است.
هیچ فایل ظاهری از SpiderPanel کپی نشده است.

## امکانات (SpiderPanel)

| بخش | توضیحات |
|---|---|
| 👤 کاربران | ساخت/مدیریت حساب، حجم، انقضا، محدودیت IP و عملیات هر کاربر |
| 🔗 اشتراک | صفحهٔ اشتراک، لینک کانفیگ، QR، کپی Base64، اشتراک گروهی با رمز |
| 🛰 اینباندها | VLESS+WS+TLS، XHTTP، Reality، MTProxy تلگرام |
| 🌐 نودها | مدیریت، سلامت، Refresh و Sync |
| ☁️ Worker | استقرار `worker.js` روی Cloudflare Pages، KV، لوکیشن‌ها، Heartbeat |
| 🧪 Scanner | TCP / IP / SNI، سابنت‌های کلادفلر، پینگ دسته‌ای |
| 🤖 ربات تلگرام | ربات کانال و ربات فروش (پلن، رسید، تأیید دستی، تحویل اشتراک) |
| 🟢 انقضا | پاک‌سازی خودکار حساب‌های منقضی |
| 🛠 ابزارها | اطلاعات رانتایم، Tunnel/Reverse، تنظیمات، بکاپ/ریستور، آمار |

## نصب

**Railway:** ریپو را Deploy کنید، Volume روی `/data` ببندید و متغیرها را تنظیم
کنید. **Docker:** `docker build -t rahgozar .` سپس اجرا با پورت `8080`.
**VPS:** `bash start.sh`.

پورت پنل `8080` ثابت است. آدرس ورود: `/rahgozar` (نام کاربری/رمز پیش‌فرض
`admin` / `admin` — حتماً عوض کنید). وضعیت سرویس: `GET /healthz`.

<sub>طرح‌های بصری و موسیقی، آثار اختصاصی پروژهٔ رهگذر هستند.</sub>
