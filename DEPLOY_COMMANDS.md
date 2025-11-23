# Deployment Guide

## 1. Push to GitHub
You need to create a new repository on GitHub first.
Then run these commands in your terminal (I can run them if you provide the URL):

```bash
git remote add origin <YOUR_GITHUB_REPO_URL>
git branch -M main
git push -u origin main
```

## 2. Deploy to Render (Free & Easy)
1. Go to [dashboard.render.com](https://dashboard.render.com)
2. Click **New +** -> **Web Service**
3. Connect your GitHub repository
4. Use these settings:
   - **Name**: tourism-planner
   - **Runtime**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
5. Click **Create Web Service**

Your app will be live in minutes! 🚀
