# 🚀 Deployment Guide — Hugging Face Spaces

## Step 1: Create your Hugging Face Space

1. Go to [huggingface.co/spaces](https://huggingface.co/spaces)
2. Sign in (or create a free account)
3. Click **"Create new Space"**
4. Fill in:
   - **Space name**: `resume-matcher-ats`
   - **License**: MIT
   - **SDK**: **Docker** ← Important!
   - **Visibility**: Public
5. Click **"Create Space"**

---

## Step 2: Push Your Code to HF Spaces

HF Spaces uses a git repository. Push your existing GitHub code to it.

### Option A – Link GitHub repo (easiest)
In your HF Space settings, go to **Settings → Repository → Add source repository** and link `adityapanda045/resume-matcher-ats`.

### Option B – Push directly via git
```bash
# Add HF Spaces as a remote (replace YOUR_USERNAME with your HF username)
git remote add hf https://huggingface.co/spaces/adityapanda045/resume-matcher-ats

# Push
git push hf main
```

---

## Step 3: Set Your API Key Secret

In your HF Space dashboard:
1. Go to **Settings → Repository Secrets**
2. Add a new secret:
   - **Name**: `GOOGLE_API_KEY`
   - **Value**: Your Gemini API key from [aistudio.google.com](https://aistudio.google.com/apikey)
3. Click **Save**

The `Dockerfile` in the repo will auto-build and start the server on port 7860. HF Spaces will expose this automatically.

---

## Step 4: Your Live URL

Once deployed:
```
https://adityapanda045-resume-matcher-ats.hf.space
```

(Format: `https://<username>-<space-name>.hf.space`)

---

## How to Update Daily (for LinkedIn Activity)

Every day, make a small change, then:
```bash
git add .
git commit -m "feat: add [small feature]"
git push origin main
git push hf main   # This triggers HF Space rebuild
```

Then add one line to `CHANGELOG.md` and post on LinkedIn!

---

## Free Tier Details

| Feature | Hugging Face Free |
|---------|------------------|
| Monthly cost | **$0** |
| Cold starts | None (always warm) |
| RAM | 16 GB |
| CPU | 2 vCPUs |
| Custom domain | ✅ |
| Sleep after inactivity | No |
