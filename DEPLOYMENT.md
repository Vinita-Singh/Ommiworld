# 🚀 Mumzworld AI - Deployment Workflow

This document outlines the complete deployment process for the Mumzworld AI Assistant application.

---

## 📋 Table of Contents
1. [Deployment Options](#deployment-options)
2. [Streamlit Cloud (Recommended)](#streamlit-cloud-recommended)
3. [GitHub Actions CI/CD](#github-actions-cicd)
4. [Local Testing Before Deployment](#local-testing-before-deployment)
5. [Troubleshooting](#troubleshooting)

---

## Deployment Options

### 1. **Streamlit Cloud** (Recommended - Free Tier Available)
   - Easiest deployment method
   - Automatic updates from GitHub
   - Built-in sharing and analytics
   - Free tier: 1 app, 1 GB memory

### 2. **Heroku** (Paid)
   - More control over environment
   - Custom domain support
   - Better for high-traffic apps

### 3. **AWS/Azure** (Pay-as-you-go)
   - Enterprise-grade infrastructure
   - Maximum scalability
   - Highest cost

### 4. **Self-hosted** (On-premise)
   - Complete control
   - Higher maintenance
   - Requires server setup

---

## Streamlit Cloud (Recommended)

### Step 1: Prepare Your Repository
```bash
# Make sure all changes are committed
git add .
git commit -m "Ready for deployment"
git push origin main
```

### Step 2: Create Streamlit Cloud Account
1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Click **"Sign up"**
3. Sign in with GitHub account
4. Grant Streamlit permission to access your repositories

### Step 3: Deploy Your App
1. Click **"New app"** button
2. Select **GitHub** as the repository source
3. Choose your repository: `paulamartya25/mumzworld.in`
4. Select branch: `main`
5. Select file path: `app.py`
6. Click **"Deploy"**

### Step 4: Configure Secrets
1. Go to **Settings** in your deployed app
2. Click **"Secrets"** tab
3. Add your `.env` variables:
   ```
   GROQ_API_KEY=your_api_key_here
   ```

### Step 5: Monitor Deployment
- App deploys automatically after each push to `main` branch
- View logs: App settings → Logs
- Share link: Automatically generated

---

## GitHub Actions CI/CD

### Automated Workflow Features
The `.github/workflows/deploy.yml` file provides:

✅ **Testing on Push**
- Runs on Python 3.10 and 3.11
- Installs dependencies
- Checks syntax errors
- Optional linting

✅ **Automatic Deployment**
- Triggers only on `main` branch pushes
- Skips on pull requests
- Prevents broken deployments

### Enable Deployment Action
1. Go to **Settings** → **Secrets and variables** → **Actions**
2. Add new secret: `STREAMLIT_CLOUD_API_TOKEN`
   - Get token from Streamlit Cloud account settings
3. Workflow will auto-deploy on next push

### View Workflow Status
- Go to **Actions** tab in GitHub
- See build and deployment status
- View logs for debugging

---

## Local Testing Before Deployment

### 1. Test Locally First
```bash
# Install dependencies
pip install -r requirements.txt

# Set environment variables
$env:GROQ_API_KEY="your_api_key"

# Run the app
streamlit run app.py
```

### 2. Test All Features
- [ ] Language selector (English/Arabic/Both)
- [ ] Try a sample query
- [ ] Check Arabic translation
- [ ] Verify styling and animations
- [ ] Test on mobile view

### 3. Run Syntax Check
```bash
python -m py_compile app.py
```

### 4. Check Dependencies
```bash
pip freeze > requirements.txt
```

---

## Deployment Checklist

Before pushing to production:

- [ ] All code is tested locally
- [ ] `.env` file is NOT committed
- [ ] `.gitignore` includes sensitive files
- [ ] `requirements.txt` is up to date
- [ ] No hardcoded API keys in code
- [ ] App runs without errors: `streamlit run app.py`
- [ ] All features working (English, Arabic, translations)
- [ ] CSS animations rendering correctly
- [ ] Responsive design tested on mobile

---

## Deployment Workflow Diagram

```
1. Local Development
   ↓
2. Test locally (streamlit run app.py)
   ↓
3. Commit & Push to GitHub
   ↓
4. GitHub Actions runs tests
   ↓
5. If tests pass → Auto-deploy to Streamlit Cloud
   ↓
6. App live at share.streamlit.io
   ↓
7. Monitor logs & user feedback
   ↓
8. Bug fixes → Repeat from Step 2
```

---

## Troubleshooting

### App Won't Deploy
**Error**: "Module not found"
- **Solution**: Ensure all packages are in `requirements.txt`
  ```bash
  pip freeze > requirements.txt
  ```

### API Key Not Found
**Error**: "GROQ_API_KEY not set"
- **Solution**: Add to Streamlit Cloud secrets:
  1. Settings → Secrets
  2. Add: `GROQ_API_KEY=your_key`

### Slow Performance
- **Solution**: Check Streamlit Cloud logs for memory issues
- Streamlit Cloud free tier: 1 GB RAM
- Consider upgraded plan for higher traffic

### CSS Not Loading
**Error**: Styling looks broken
- **Solution**: Clear browser cache and refresh
- Sometimes takes 30 seconds for updates

### Arabic Text Not Displaying
**Error**: Arabic characters showing as boxes
- **Solution**: Browser encoding issue
  - Press `Ctrl+Shift+R` (hard refresh)
  - Check browser language settings

---

## Updating the App

### For Bug Fixes or Small Updates
1. Make changes locally
2. Test: `streamlit run app.py`
3. Commit: `git commit -m "Fix: description"`
4. Push: `git push origin main`
5. Streamlit Cloud auto-deploys (1-2 minutes)

### For Major Features
1. Create feature branch: `git checkout -b feature/new-feature`
2. Develop and test locally
3. Push: `git push origin feature/new-feature`
4. Create Pull Request on GitHub
5. Review and merge to `main`
6. Auto-deployment triggers

### Rollback to Previous Version
```bash
# View commit history
git log --oneline

# Revert to previous commit
git revert <commit_hash>
git push origin main

# Streamlit Cloud will auto-deploy the reverted version
```

---

## Performance Optimization Tips

1. **Cache API Responses**
   ```python
   @st.cache_data
   def get_recommendations():
       # Cache results
   ```

2. **Reduce Model Load Time**
   - Pre-warm API connections
   - Consider API rate limiting

3. **Optimize CSS**
   - Minimize animation complexity
   - Use CSS variables for themes

4. **Monitor Resource Usage**
   - Streamlit Cloud dashboard
   - Check for memory leaks

---

## Security Best Practices

✅ **Do**
- Store API keys in environment variables
- Use `.gitignore` for sensitive files
- Enable 2FA on GitHub and Streamlit Cloud
- Review code before deployment
- Keep dependencies updated

❌ **Don't**
- Commit API keys to repository
- Share `.env` files
- Disable security warnings
- Deploy untested code
- Use hardcoded credentials

---

## Support & Resources

- 📚 [Streamlit Documentation](https://docs.streamlit.io)
- 🔧 [Groq API Docs](https://console.groq.com/docs)
- 🐙 [GitHub Actions Docs](https://docs.github.com/actions)
- 💬 [Streamlit Community Forums](https://discuss.streamlit.io)

---

**Last Updated**: April 2026
**App Version**: 1.0.0
**Deployment Platform**: Streamlit Cloud
