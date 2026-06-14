## Step-by-Step Deployment

### Step 1: Push to GitHub

1. Create GitHub repository:
   - Go to https://github.com
   - Click "New repository"
   - Name: fake-news-detector
   - Make it public
   - Don't initialize with README

2. Upload your files:
   ```bash
   cd "c:\Users\hasin\OneDrive\Desktop\Fake News Detector"
   git init
   git add .
   git commit -m "Initial commit - Fake News Detector"
   git remote add origin https://github.com/YOUR-USERNAME/fake-news-detector.git
   git push -u origin main
   ```

### Step 2: Deploy to Streamlit Cloud

1. Sign up: https://share.streamlit.io (free)

2. Connect GitHub:
   - Click "New app"
   - Connect your GitHub account
   - Select your fake-news-detector repository

3. Configure deployment:
   - Main file path: main_app.py
   - Requirements file: streamlit_requirements.txt
   - Click "Deploy"

4. Wait 2-3 minutes for deployment

5. Your app is live!
   - URL: https://YOUR-USERNAME-fake-news-detector.streamlit.app

---

## Test the Deployed App

Visit the deployed URL and test with these examples:

### Example 1: Fake News (Low Score)
```
BREAKING: Scientists discover aliens living among us!
This shocking truth will change everything you know!
```

### Example 2: Real News (High Score)
```
According to a peer-reviewed study published in Nature,
researchers found evidence of climate change impact on ecosystems.
```

## Alternative Free Deployments

### Option 2: Railway 
1. Sign up: https://railway.app
2. Connect GitHub repo
3. Deploy automatically
4. URL: your-app.railway.app

### Option 3: Render 
1. Sign up: https://render.com
2. Create Web Service
3. Point to your main_app.py
4. URL: your-app.onrender.com

---

## Commands Reference

```bash
# 1. Setup virtual environment
python -m venv venv
venv\Scripts\activate

# 2. Install dependencies
pip install -r streamlit_requirements.txt

# 3. Test locally
streamlit run main_app.py

# 4. Deploy to GitHub
git add .
git commit -m "Update for deployment"
git push origin main
```
---

## Next Steps After Deployment

1. Test your deployed app with the examples
2. Share the URL with friends and classmates
3. Add a README to your GitHub repo
4. Set up custom domain (optional)
5. Monitor usage in Streamlit Cloud dashboard

---