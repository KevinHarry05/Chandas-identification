# ✅ Render Deployment Checklist

Run through this checklist before uploading to Render.

## 1. Repository Setup

- [ ] Git repository initialized (`git init`)
- [ ] All changes committed (`git status` shows clean)
- [ ] Remote added: `git remote add origin <your-repo-url>`
- [ ] Code pushed to GitHub/GitLab

### Verify Model Files in Git:
```bash
# Run from project root
git ls-files | grep "models/.*\.pkl"
```

**Expected Output:**
```
backend/models/labels.pkl
backend/models/labels_enhanced.pkl
backend/models/random_forest.pkl
backend/models/random_forest_enhanced.pkl
backend/models/scaler_enhanced.pkl
```

If empty, add models:
```bash
git add backend/models/
git commit -m "Add trained ML models"
git push origin main
```

---

## 2. File Structure Verification

- [ ] `backend/app/` directory exists
- [ ] `backend/app/main.py` exists
- [ ] `backend/requirements.txt` exists
- [ ] `backend/models/random_forest_enhanced.pkl` exists (8.7 MB)
- [ ] `.gitignore` exists and models are NOT ignored

### Verify Structure:
```bash
ls -la backend/
ls -la backend/app/
ls -la backend/models/
cat backend/requirements.txt | head -5
```

---

## 3. Requirements Check

**These must be in `backend/requirements.txt`:**

- [ ] fastapi==0.115.0
- [ ] uvicorn[standard]==0.32.0
- [ ] scikit-learn==1.5.2
- [ ] shap==0.46.0
- [ ] pandas==2.2.3
- [ ] numpy==2.1.3
- [ ] joblib==1.4.2
- [ ] pydantic==2.9.2

Verify:
```bash
grep -E "(fastapi|uvicorn|scikit-learn|shap)" backend/requirements.txt
```

---

## 4. Code Configuration

Check these are correct:

- [ ] No hardcoded absolute paths (should use relative paths)
- [ ] No hardcoded port 8000 in startup (should use `$PORT` env var)
- [ ] Model loading uses relative paths: `models/random_forest_enhanced.pkl`
- [ ] CORS enabled for frontend domain

### Check File Paths:
```bash
grep -r "C:\\Users" backend/app/ || echo "✅ No absolute paths found"
grep -r "random_forest" backend/app/core/ml/model_loader.py | head -3
```

---

## 5. Environment Variables

- [ ] `.env` file is gitignored (✓ already in .gitignore)
- [ ] No sensitive data in code
- [ ] All config comes from environment or defaults

---

## 6. Deployment Commands

### For Render Dashboard:

**Build Command:**
```
pip install -r backend/requirements.txt
```

**Start Command:**
```
cd backend && python -m uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

### Test Before Deploying:

```bash
# From project root
cd backend
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

Visit: `http://localhost:8000/docs` → Should see Swagger UI

---

## 7. Test Verses Ready

- [ ] Test verse #1: `यो वै स परम ब्रह्म तस्य नाम सत्यम्।`
- [ ] Test verse #2: `मा गमो यातन प्रिये भरत।`
- [ ] TEST_EXAMPLES.md in root directory
- [ ] RENDER_DEPLOYMENT.md in root directory

---

## 8. Git Push Ready

```bash
# Before pushing to Render
git status                              # Should be clean
git log --oneline | head -5             # Show recent commits
git remote -v                           # Show connected repo
```

Then push:
```bash
git push origin main
```

---

## 9. Render Configuration

**Go to [render.com](https://render.com):**

1. Create new Web Service
2. Connect GitHub repo
3. Fill in:
   - **Name:** `chandas-api`
   - **Environment:** Python 3
   - **Build Command:** `pip install -r backend/requirements.txt`
   - **Start Command:** `cd backend && python -m uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - **Plan:** Free (for testing) or Starter (recommended)

4. Click "Create Web Service"

---

## 10. Post-Deployment Verification

Once deployed (URL will be like `https://chandas-api-xxx.onrender.com`):

### Health Check:
```bash
curl https://chandas-api-xxx.onrender.com/
```

Expected: `{"message": "Chandas Identifier API - Ready for Sanskrit Meter Analysis"}`

### Test API:
```bash
curl -X POST https://chandas-api-xxx.onrender.com/analyze-verse \
  -H "Content-Type: application/json" \
  -d '{"verse": "यो वै स परम ब्रह्म तस्य नाम सत्यम्।"}'
```

Expected: Full JSON response with predictions and SHAP values

### Swagger UI:
Visit: `https://chandas-api-xxx.onrender.com/docs`

---

## 11. Common Issues & Fixes

| Issue | Solution |
|-------|----------|
| Build fails: "No module named 'app'" | Change build command to: `pip install -r backend/requirements.txt` |
| Model not found error | Ensure models are in git: `git add backend/models/ && git push` |
| Port binding error | Verify start command has `--port $PORT` (not `--port 8000`) |
| 502 Bad Gateway | Check Render logs for error details |
| Slow first request | Normal - Free tier cold start is 30-50s. Upgrade to Starter. |

---

## 12. Performance Targets

After deployment, you should see:

- ✅ Health check responds in <1s
- ✅ Verse analysis takes 200-400ms
- ✅ SHAP explanations computed with 41 features
- ✅ No crashes or 500 errors
- ✅ Logs show successful requests

---

## 🎯 Final Checklist

```
Setup:
  [ ] Git repo configured
  [ ] All code committed
  [ ] Models in git

Files:
  [ ] requirements.txt complete
  [ ] No absolute paths
  [ ] Relative paths used
  [ ] Model files present

Render:
  [ ] Account created
  [ ] Build command correct
  [ ] Start command correct
  [ ] Environment set (if needed)

Testing:
  [ ] Local test passing
  [ ] Health check works
  [ ] Verse analysis works
  [ ] Swagger UI accessible

Documentation:
  [ ] RENDER_DEPLOYMENT.md created
  [ ] TEST_EXAMPLES.md updated
  [ ] README.md has API docs
```

---

## 🚀 Ready to Deploy!

If all checkboxes ✅, you're ready to push to Render:

```bash
git push origin main
# Then create Web Service on render.com
```

Your API will be live in 2-3 minutes! 🎉

---

## 📞 Deployment Support

**If stuck:**
1. Check Render logs: Dashboard → Your Service → Logs
2. Verify build command has `backend/` path
3. Ensure model files are in git
4. Test locally first
5. Review RENDER_DEPLOYMENT.md for detailed guide

**Good luck!** 🚀
