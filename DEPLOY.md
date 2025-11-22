# Deployment Guide

## Push to GitHub

### Step 1: Create a GitHub Repository

1. Go to https://github.com/new
2. Repository name: `multi-agent-tourism-system` (or your preferred name)
3. Description: "Multi-Agent Tourism System - Fast, intelligent trip planning with weather and tourist attractions"
4. Choose Public or Private
5. **DO NOT** initialize with README, .gitignore, or license (we already have these)
6. Click "Create repository"

### Step 2: Push to GitHub

Run these commands (replace YOUR_USERNAME with your GitHub username):

```bash
git remote add origin https://github.com/YOUR_USERNAME/multi-agent-tourism-system.git
git branch -M main
git push -u origin main
```

Or if you prefer SSH:

```bash
git remote add origin git@github.com:YOUR_USERNAME/multi-agent-tourism-system.git
git branch -M main
git push -u origin main
```

## Deploy to Cloud Platforms

### Option 1: Heroku (Recommended)

1. Install Heroku CLI: https://devcenter.heroku.com/articles/heroku-cli
2. Login: `heroku login`
3. Create app: `heroku create your-app-name`
4. Deploy: `git push heroku main`
5. Open: `heroku open`

### Option 2: Railway

1. Go to https://railway.app
2. Click "New Project"
3. Select "Deploy from GitHub repo"
4. Choose your repository
5. Railway auto-detects Python and deploys
6. Your app will be live at: `https://your-app-name.railway.app`

### Option 3: Render

1. Go to https://render.com
2. Click "New +" → "Web Service"
3. Connect your GitHub repository
4. Settings:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python app.py`
5. Click "Create Web Service"
6. Your app will be live at: `https://your-app-name.onrender.com`

### Option 4: PythonAnywhere

1. Go to https://www.pythonanywhere.com
2. Create a free account
3. Upload files via Files tab
4. Create a new Web App
5. Configure WSGI file to point to app.py
6. Reload web app

## Environment Variables

No environment variables needed! The app uses open-source APIs that don't require keys.

## Post-Deployment

After deployment, your app will be accessible at the provided URL. Test it with queries like:
- "I'm going to go to Paris"
- "visit tokyo, what is the temperature there"
- "trip to new york"

