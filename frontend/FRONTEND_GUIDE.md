# 🎨 Frontend Integration Guide

## Overview

The **Chandas-UI** is a production-ready React frontend that connects to the Chandas Identifier backend API. It provides:

- ✅ Sanskrit verse analysis with real-time feedback
- ✅ Visual confidence scores and alternatives
- ✅ SHAP explainability visualizations
- ✅ Responsive design (mobile, tablet, desktop)
- ✅ Dark mode support
- ✅ Backend status monitoring
- ✅ Comprehensive error handling

---

## 🚀 Quick Start

### Prerequisites
- Node.js 16+ and npm (or yarn)
- Backend running on `http://127.0.0.1:8000`

### Installation

```bash
cd frontend/chandas-ui

# Install dependencies
npm install

# Start development server
npm run dev
```

Visit: `http://localhost:5173`

---

## 📁 Project Structure

```
chandas-ui/
├── .env                          # Environment configuration (local)
├── .env.example                  # Example environment variables
├── vite.config.js               # Vite build configuration
├── package.json                 # Dependencies & scripts
│
├── src/
│   ├── App.jsx                  # Main app component
│   ├── main.jsx                 # Entry point
│   │
│   ├── api/
│   │   └── chandasApi.js        # Backend API client (axios)
│   │
│   ├── pages/
│   │   └── SingleAnalysis.jsx   # Main verse analysis page
│   │
│   ├── components/
│   │   ├── ResultCard.jsx       # Display analysis results
│   │   ├── SingleVerseForm.jsx  # (Optional) Reusable form
│   │   └── ExplainabilityPanel/ # (Optional) SHAP visualization
│   │
│   └── styles/
│       ├── App.css              # Global styles
│       ├── SingleAnalysis.css   # Page-specific styles
│       └── ResultCard.css       # Component styles
│
└── index.html                   # HTML template
```

---

## 🔧 Configuration

### Environment Variables

Create `.env` file in `chandas-ui/`:

```bash
# Development (local backend)
VITE_API_URL=http://127.0.0.1:8000
VITE_REQUEST_TIMEOUT=30000

# Production (Render backend)
# VITE_API_URL=https://chandas-api.onrender.com
# VITE_REQUEST_TIMEOUT=45000
```

- **VITE_API_URL**: Backend API base URL
- **VITE_REQUEST_TIMEOUT**: Request timeout in milliseconds

### For Production Deployment

Update `.env` when deploying to production:

```bash
VITE_API_URL=https://chandas-api.onrender.com
```

Then build:
```bash
npm run build
```

---

## 🛠️ Development

### Available Scripts

```bash
# Start development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview

# Run linter
npm run lint
```

### Hot Module Replacement (HMR)

Changes are automatically reflected in the browser without page reload.

---

## 🔌 API Integration

### Backend API Client

All API calls go through `src/api/chandasApi.js`:

```javascript
import { analyzeVerse, healthCheck, getApiUrl } from "./api/chandasApi";

// Analyze single verse
const result = await analyzeVerse("यो वै स परम ब्रह्म तस्य नाम सत्यम्।");

// Check if backend is running
const status = await healthCheck();

// Get configured API URL
const url = getApiUrl();
```

### Features

- ✅ Environment-based configuration
- ✅ Request/response interceptors
- ✅ Error handling with meaningful messages
- ✅ Timeout handling
- ✅ Console logging for debugging

### Error Handling

Errors from the API are caught and user-friendly messages are displayed:

```javascript
try {
  const result = await analyzeVerse(verse);
} catch (error) {
  // error.status: HTTP status code
  // error.message: User-friendly message
  // error.data: Full response data
}
```

---

## 🎯 Components

### SingleAnalysis Page

Main page component (`src/pages/SingleAnalysis.jsx`):

**Features:**
- Backend status indicator
- Verse input textarea with example buttons
- Analysis button with loading state
- Error messages with helpful hints
- Result display with SHAP explanations
- Keyboard shortcuts (Ctrl+Enter)

**Example Usage:**
```jsx
<SingleAnalysis />
```

### ResultCard Component

Display analysis results (`src/components/ResultCard.jsx`):

**Props:**
- `result`: Analysis result object from backend
- `loading`: Boolean for loading state

**Displays:**
- Verse and syllable pattern
- Main prediction with confidence bar
- Alternative meters
- Top 5 SHAP features
- Decision paths (first 2)

**Example:**
```jsx
<ResultCard result={analysisResult} loading={isLoading} />
```

---

## 🎨 Styling

### CSS Structure

- **Global**: `App.css` - Typography, layout, utilities
- **Page**: `SingleAnalysis.css` - Form, inputs, status
- **Component**: `ResultCard.css` - Results display

### Design System

**Colors:**
- Primary: `#3b82f6` (Blue)
- Success: `#10b981` (Green)
- Error: `#ef4444` (Red)
- Warning: `#f59e0b` (Amber)

**Spacing:**
- Small: `0.5rem`
- Medium: `1rem`
- Large: `1.5rem`
- XL: `2rem`

**Responsive:**
- Mobile: < 768px
- Tablet: 768px - 1024px
- Desktop: > 1024px

---

## 🧪 Testing

### Test with Backend

1. **Start Backend:**
   ```bash
   cd backend
   python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
   ```

2. **Start Frontend:**
   ```bash
   cd frontend/chandas-ui
   npm run dev
   ```

3. **Test Examples:**
   - Click "Quick Examples" buttons
   - Try different Sanskrit verses
   - Verify results and SHAP values
   - Check backend status indicator

### Manual Testing Verses

```
1. यो वै स परम ब्रह्म तस्य नाम सत्यम्।
2. मा गमो यातन प्रिये भरत।
3. नमो देवाय सर्वज्ञाय प्रभवे।
4. रामराज्यं नृपतेः कृतं।
```

### Browser DevTools

- **Network Tab**: Monitor API calls
- **Console**: Check for JavaScript errors
- **React DevTools**: Inspect component state

---

## 🚀 Deployment

### Build for Production

```bash
npm run build
```

Creates optimized build in `dist/` directory.

### Deploy to Vercel

```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
vercel
```

### Deploy to Netlify

```bash
# Install Netlify CLI
npm i -g netlify-cli

# Deploy
netlify deploy --prod --dir=dist
```

### Important: Update API URL

Before deployment, update `.env` to point to production backend:

```bash
VITE_API_URL=https://chandas-api.onrender.com
```

Then rebuild and deploy.

---

## 🔒 Security Considerations

✅ **Already Implemented:**
- Input validation (empty verse check)
- Error message sanitization (no sensitive info leaked)
- CORS properly configured on backend
- No hardcoded credentials in frontend code

📝 **For Production:**
1. Use HTTPS only
2. Implement CORS properly:
   ```javascript
   // Backend should have:
   app.add_middleware(
       CORSMiddleware,
       allow_origins=["https://yourdomain.com"],
       allow_credentials=True,
       allow_methods=["*"],
       allow_headers=["*"],
   )
   ```

3. Add rate limiting on backend
4. Implement API key authentication if needed

---

## 🐛 Troubleshooting

### Backend Not Connecting

**Error:** "Cannot connect to API at http://127.0.0.1:8000"

**Solution:**
1. Verify backend is running:
   ```bash
   cd backend
   python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
   ```
2. Check `.env` has correct `VITE_API_URL`
3. Check firewall/network settings
4. Try health check: `curl http://127.0.0.1:8000/`

### CORS Errors

**Error:** "Access to XMLHttpRequest blocked by CORS policy"

**Solution:**
- Backend CORS is already configured
- For local dev, should work automatically
- For production, update backend `main.py` with correct frontend URL

### Verse Not Analyzing

**Steps:**
1. Check browser console for errors
2. Check network tab for API request/response
3. Verify verse is in Devanagari script
4. Check backend logs for errors

### Building for Production

**If build fails:**
```bash
# Clear cache
rm -rf node_modules package-lock.json
npm install
npm run build
```

---

## 📊 Performance

### Optimization

- ✅ Code splitting with Vite
- ✅ CSS minification
- ✅ Image optimization
- ✅ Lazy loading (if routes added)

### Load Times

- **Development**: ~1s (with HMR)
- **Production**: ~500ms (first load)
- **API Response**: ~300-500ms per analysis

---

## 📚 API Response Example

```json
{
  "verse": "यो वै स परम ब्रह्म तस्य नाम सत्यम्।",
  "laghu_guru_pattern": "GGLLLLGGLGGLLGG",
  "best_prediction": {
    "class_index": 1,
    "chandas": "इन्द्रवज्रा",
    "confidence": 0.1956
  },
  "alternatives": [
    {
      "class_index": 5,
      "chandas": "मन्दाक्रान्ता",
      "confidence": 0.1879
    }
  ],
  "explainability": {
    "top_features": [
      {
        "feature": "gl_count",
        "value": 3.8996,
        "shap_value": 0.04666
      }
    ],
    "decision_paths": [
      [
        "pattern_length > -0.862",
        "entropy_bigram ≤ -0.005"
      ]
    ]
  }
}
```

---

## 🔐 Environment Setup for Different Environments

### Local Development
```bash
VITE_API_URL=http://127.0.0.1:8000
VITE_REQUEST_TIMEOUT=30000
```

### Staging
```bash
VITE_API_URL=https://chandas-api-staging.onrender.com
VITE_REQUEST_TIMEOUT=45000
```

### Production
```bash
VITE_API_URL=https://chandas-api.onrender.com
VITE_REQUEST_TIMEOUT=45000
```

---

## 📞 Support

For issues or questions:

1. Check console for errors: F12 → Console
2. Check network requests: F12 → Network
3. Verify backend is running
4. Review backend logs for API errors
5. Check `.env` configuration

---

## ✨ Future Enhancements

Possible improvements:

- [ ] Add analysis history
- [ ] Batch verse analysis
- [ ] Export results to PDF
- [ ] User authentication
- [ ] API key management
- [ ] Multi-language support
- [ ] Advanced filtering options
- [ ] Data visualization dashboard

---

## 📝 License

Same as main project. See main `README.md`.

---

**Frontend is production-ready and fully integrated with backend! 🚀**
