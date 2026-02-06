# 🚀 Quick Start Reference Card

## 5-Second Setup

```bash
# Terminal 1: Backend
cd backend && python -m uvicorn app.main:app --host 127.0.0.1 --port 8000

# Terminal 2: Frontend
cd frontend/chandas-ui && npm install && npm run dev

# Browser: http://localhost:5173
```

---

## Frontend Stack

| Tool | Version | Purpose |
|------|---------|---------|
| **React** | 19.1.1 | UI framework |
| **Vite** | 7.1.14 | Build tool |
| **Axios** | 1.13.2 | HTTP client |
| **Node** | 16+ | Runtime |

---

## API Endpoints

| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | `/` | Health check |
| POST | `/analyze-verse` | Analyze single verse |
| GET | `/docs` | Swagger UI |

---

## Test Verses (Copy-Paste Ready)

1. **यो वै स परम ब्रह्म तस्य नाम सत्यम्।** (Indravajra)
2. **मा गमो यातन प्रिये भरत।** (Mandakranta)
3. **नमो देवाय सर्वज्ञाय प्रभवे।** (Vasantatilaka)
4. **रामराज्यं नृपतेः कृतं।** (Indravajra)

---

## Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Ctrl+Enter` | Submit analysis |
| `F12` | Open DevTools |
| `Ctrl+Shift+R` | Hard refresh |

---

## Configuration

**Development (.env)**
```
VITE_API_URL=http://127.0.0.1:8000
VITE_REQUEST_TIMEOUT=30000
```

**Production (.env)**
```
VITE_API_URL=https://chandas-api.onrender.com
VITE_REQUEST_TIMEOUT=45000
```

---

## npm Scripts

```bash
npm run dev      # Start development server
npm run build    # Build for production
npm run preview  # Preview production build
npm run lint     # Run ESLint
```

---

## Folder Structure

```
frontend/chandas-ui/
├── .env                    # Configuration
├── src/
│   ├── App.jsx            # Main component
│   ├── api/               # API client
│   ├── pages/             # Pages
│   ├── components/        # Components
│   └── styles/            # CSS files
└── package.json
```

---

## Component Overview

| Component | Purpose |
|-----------|---------|
| **SingleAnalysis** | Main page, form handling |
| **ResultCard** | Display results, SHAP |
| **chandasApi** | API communication |

---

## Error Messages

| Error | Solution |
|-------|----------|
| Cannot connect to API | Start backend, check `.env` |
| Verse analysis fails | Verify verse is Devanagari |
| SHAP not showing | Check backend logs |
| Styling broken | Hard refresh (Ctrl+Shift+R) |

---

## Performance Targets

- Frontend load: **< 1s**
- API response: **< 500ms**
- SHAP computation: **< 300ms**

---

## Testing Commands

```bash
# Health check
curl http://127.0.0.1:8000/

# Test verse analysis
curl -X POST http://127.0.0.1:8000/analyze-verse \
  -H "Content-Type: application/json" \
  -d '{"verse": "यो वै स परम ब्रह्म तस्य नाम सत्यम्।"}'

# View Swagger UI
# http://127.0.0.1:8000/docs
```

---

## Browser DevTools

**F12 Tabs to Check:**
- **Console** → JavaScript errors
- **Network** → API requests/responses
- **Elements** → HTML structure
- **Application** → LocalStorage/Cookies

---

## Deployment

```bash
# Build frontend
npm run build

# Deploy to Vercel
vercel --prod

# Deploy to Netlify
netlify deploy --prod --dir=dist

# Deploy backend to Render
# (See RENDER_DEPLOYMENT.md)
```

---

## Important Files

| File | Purpose |
|------|---------|
| `frontend/chandas-ui/.env` | Configuration |
| `src/api/chandasApi.js` | API client |
| `src/pages/SingleAnalysis.jsx` | Main page |
| `src/styles/` | All CSS files |

---

## Resources

- 📘 [Frontend Guide](frontend/FRONTEND_GUIDE.md)
- 🧪 [Integration Testing](INTEGRATION_TESTING.md)
- 🚀 [Render Deployment](RENDER_DEPLOYMENT.md)
- ✅ [Integration Complete](FRONTEND_INTEGRATION_COMPLETE.md)

---

## Quick Links

- Frontend: http://localhost:5173
- Backend: http://127.0.0.1:8000
- Swagger UI: http://127.0.0.1:8000/docs
- API Base: http://127.0.0.1:8000

---

## Status Checklist

- [ ] Backend running
- [ ] Frontend running
- [ ] Green connection indicator
- [ ] Example buttons work
- [ ] Analysis completes
- [ ] SHAP values show
- [ ] No console errors
- [ ] Results display correctly

---

## Common Commands

```bash
# Start fresh
rm -rf node_modules package-lock.json && npm install

# Check backend status
curl http://127.0.0.1:8000/

# View recent commits
git log --oneline -5

# Hard refresh frontend
# In browser: Ctrl+Shift+R (Cmd+Shift+R on Mac)
```

---

## Need Help?

1. Check **console** (F12 → Console)
2. Check **network** (F12 → Network)
3. Check **backend logs** (Terminal 1)
4. Read **FRONTEND_GUIDE.md**
5. Read **INTEGRATION_TESTING.md**

---

**Everything is ready to go! Happy analyzing! 🎉**

_Last updated: Feb 5, 2026_
