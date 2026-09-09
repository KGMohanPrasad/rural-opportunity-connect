# 🌐 24/7 Live Deployment & Continuous Uptime Guide
### Rural Opportunity Connect — SDG 10 Platform

This guide provides the exact steps to launch your website on the cloud so it runs **24/7 live, 365 days a year**, accessible by anyone worldwide on phones, tablets, or computers—even when your laptop is turned off.

---

## 📑 Table of Contents
1. [Method 1: Full-Stack Django Web App on Render.com (Recommended)](#method-1-full-stack-django-web-app-on-rendercom)
2. [CRITICAL: How to Keep Free Cloud Servers Awake 24/7 (Never Sleep)](#critical-how-to-keep-free-cloud-servers-awake-247-never-sleep)
3. [Method 2: 60-Second Instant Live Link via Netlify / Vercel](#method-2-60-second-instant-live-link-via-netlify--vercel)
4. [Method 3: Alternative 24/7 Host on PythonAnywhere](#method-3-alternative-247-host-on-pythonanywhere)

---

## Method 1: Full-Stack Django Web App on Render.com

Render offers a generous free tier for Python web services with automated SSL (HTTPS), custom domains, and automatic Git deployments.

### Step 1: Initialize Git and Push to GitHub

1. Open PowerShell / Command Prompt inside the Django project folder:
   ```powershell
   cd "c:\Users\mirut\Downloads\design proto mir\design proto\design proto\Design thinking\rural_opportunity_connect"
   ```

2. Initialize git and commit your files:
   ```powershell
   git init
   git branch -M main
   git add .
   git commit -m "feat: production ready 24/7 cloud configuration with whitenoise and gunicorn"
   ```

3. Create a new repository on [GitHub](https://github.com/new):
   - Repository name: `rural-opportunity-connect`
   - Set to **Public** (or Private)
   - Do **NOT** initialize with README (we already have everything)

4. Link and push your local code:
   ```powershell
   git remote add origin https://github.com/YOUR_GITHUB_USERNAME/rural-opportunity-connect.git
   git push -u origin main
   ```

---

### Step 2: Deploy on Render.com

1. Go to [https://render.com](https://render.com) and click **Get Started for Free** (Sign in with your GitHub account).
2. On your Dashboard, click **New +** → select **Web Service**.
3. Choose **Build and deploy from a Git repository** → click **Next**.
4. Connect your GitHub repository: `rural-opportunity-connect`.
5. Render will automatically detect the settings from `render.yaml` or you can verify these values:
   - **Name**: `rural-opportunity-connect`
   - **Region**: Oregon (US West) or Singapore / Frankfurt
   - **Branch**: `main`
   - **Root Directory**: Leave blank (or `./`)
   - **Runtime**: `Python 3`
   - **Build Command**: `./build.sh`
   - **Start Command**: `gunicorn config.wsgi:application`
   - **Instance Type**: **Free** ($0 / month)
6. Under **Environment Variables**, add:
   - `PYTHON_VERSION` = `3.11.9`
   - `DEBUG` = `False`
   - `SECRET_KEY` = `django-secure-random-key-change-this-in-prod-789`
   - `ALLOWED_HOSTS` = `*`
   - `CSRF_TRUSTED_ORIGINS` = `https://*.onrender.com`
7. Click **Create Web Service**.

Render will now run `build.sh`, install all dependencies, collect static files using WhiteNoise, apply database migrations, and boot Gunicorn. Within 2–3 minutes, you will receive your live URL:
```
https://rural-opportunity-connect.onrender.com
```

---

## ⚡ CRITICAL: How to Keep Free Cloud Servers Awake 24/7 (Never Sleep)

Free tier cloud servers (like Render, Koyeb, Glitch) automatically go to sleep if nobody visits them for 15 minutes. When someone opens the site, it takes ~45 seconds to wake up (cold start).

**Here is the 100% free solution used by developers worldwide to keep it awake 24/7:**

### Setup a 5-Minute Keep-Alive Monitor (Takes 2 minutes)

1. Go to [UptimeRobot.com](https://uptimerobot.com) (or [cron-job.org](https://cron-job.org)).
2. Sign up for a free account.
3. Click **+ Add New Monitor**.
4. Configure the monitor:
   - **Monitor Type**: `HTTP(s)`
   - **Friendly Name**: `Rural Opportunity Connect 24/7 Ping`
   - **URL (or IP)**: `https://rural-opportunity-connect.onrender.com` (your live Render URL)
   - **Monitoring Interval**: Every `5 minutes`
5. Click **Create Monitor**.

### How this works:
- Every 5 minutes, UptimeRobot automatically sends a lightweight HTTP request to your website.
- Render detects continuous traffic and **never spins down or sleeps**.
- Your website stays **100% hot, responsive, and live 24/7/365** at **$0 cost**!

---

## Method 2: 60-Second Instant Live Link via Netlify / Vercel

If you need a live link **right now** to show your professor, client, or team without waiting for server builds, you can deploy the **Interactive Standalone Prototype** (`index.html`) to Netlify or Vercel:

### Option A: Netlify Drop (No Terminal, No Git — 30 Seconds!)
1. Open your browser and go to [https://app.netlify.com/drop](https://app.netlify.com/drop).
2. Open File Explorer to `c:\Users\mirut\Downloads\design proto mir\design proto`.
3. Drag and drop the folder containing `index.html` (or the `Rural_Opportunity_Connect_Live_Web_Prototype.zip` archive) directly into the Netlify Drop box in your browser.
4. Netlify will instantly generate a live HTTPS URL (e.g. `https://rural-opportunity-connect.netlify.app`).
5. **Uptime**: 100% live 24/7 forever on global edge CDN.

### Option B: Vercel CLI (From Terminal)
1. Run in PowerShell:
   ```powershell
   npx vercel deploy --prod
   ```
2. Follow the 3 prompts to link your free Vercel account.
3. You will receive an instant 24/7 live link: `https://design-proto.vercel.app`.

---

## Method 3: Alternative 24/7 Host on PythonAnywhere

If you prefer Python-native hosting without container build steps:
1. Register for free at [PythonAnywhere.com](https://www.pythonanywhere.com).
2. Go to **Web** tab → **Add a new web app** → Select **Django** → choose Python 3.10/3.11.
3. In the **Files** tab, upload the `rural_opportunity_connect` folder or clone it via the Bash console:
   ```bash
   git clone https://github.com/YOUR_GITHUB_USERNAME/rural-opportunity-connect.git
   ```
4. Set the virtualenv path to your project's venv.
5. In the Web tab, click **Reload <username>.pythonanywhere.com**.
6. Your app is live at `https://<username>.pythonanywhere.com` 24/7! (PythonAnywhere free accounts require clicking a 3-month renewal button once every 90 days).

---

## 🛠️ Verification Checklist

| Checkpoint | Status | Note |
| :--- | :---: | :--- |
| **Gunicorn Installed** | ✅ Ready | Listed in `requirements.txt` |
| **WhiteNoise Configured** | ✅ Ready | Active in `MIDDLEWARE` & `STATICFILES_STORAGE` |
| **Procfile Present** | ✅ Ready | `web: gunicorn config.wsgi:application` |
| **Build Script Ready** | ✅ Ready | `build.sh` collects static and runs migrations |
| **Dynamic Host & CSRF** | ✅ Ready | Configured for `*.onrender.com`, `*.railway.app`, etc. |
| **Zero Sleep Keep-Alive** | 📌 User Action | Add free monitor on UptimeRobot to ping every 5 mins |
