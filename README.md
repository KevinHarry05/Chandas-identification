# 🕉️ Chandas Identifier - Sanskrit Meter Recognition System

AI-Powered Sanskrit Poetic Meter (Chandas) Identification with Explainable AI

## 🎯 Overview

Chandas Identifier automatically identifies Sanskrit poetic meters (chandas/छन्द) from Devanagari text using Machine Learning. The system uses ensemble learning with 41 engineered features and SHAP explainability.

## 📸 Live Demo

![Chandas Identifier UI - Prediction Example](docs/images/ui-prediction-example.png)

*The interface showing meter identification with confidence scores, alternative possibilities, and SHAP-based explainability features*

### Key Features

- ✨ **10 Sanskrit Meters** - Anuṣṭubh, Indravajrā, Mandākrāntā, Vasantatilakā, and more
- ⚡ **Fast Predictions** - Real-time meter identification  
- 🔍 **Explainable AI** - SHAP feature importance analysis
- 🌐 **REST API** - Easy integration via FastAPI
- 📊 **Calibrated Confidence** - Meaningful probability scores
- 🧪 **Production Ready** - Comprehensive error handling

## 📂 Project Structure

```
chandas_project/
├── backend/                              # FastAPI Backend
│   ├── app/
│   │   ├── main.py                      # Application entry point
│   │   ├── api/routes.py                # API endpoints
│   │   └── core/
│   │       ├── ml/                      # Machine Learning
│   │       │   ├── model_loader.py      # Model initialization
│   │       │   ├── enhanced_features.py # 41-feature extraction
│   │       │   ├── predict.py           # Prediction engine
│   │       │   └── *_xai.py             # Explainability (SHAP)
│   │       ├── text/                    # Text Processing
│   │       │   ├── laghu_guru.py        # Syllable pattern extraction
│   │       │   └── normalize.py         # Text normalization
│   │       └── db/                      # Database operations
│   ├── models/                          # Pre-trained models
│   │   ├── random_forest_enhanced.pkl   # Ensemble model (8.7 MB)
│   │   ├── labels_enhanced.pkl          # Class labels
│   │   └── scaler_enhanced.pkl          # Feature scaler
│   └── requirements.txt                 # Python dependencies
│
├── frontend/                             # Vue.js Frontend
│   └── chandas-ui/
│       ├── src/
│       │   ├── api/chandasApi.js        # API client
│       │   ├── components/              # React components
│       │   └── pages/                   # Page components
│       ├── package.json                 # NPM dependencies
│       └── vite.config.js               # Build configuration
│
├── data/                                 # Training & Example Data
│   ├── processed_data.csv               # Dataset (300 samples)
│   └── examples.json                    # Example verses
│
└── README.md                            # This file
```

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- Node.js 14+ (for frontend)
- pip & npm

### Installation

```bash
# Backend Setup
cd backend
pip install -r requirements.txt

# Frontend Setup (optional)
cd frontend/chandas-ui
npm install
```

### Running the Backend

```bash
cd backend
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

Access the API:
- **Health Check**: GET http://localhost:8000/
- **Analyze Verse**: POST http://localhost:8000/analyze-verse
- **Swagger Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Running the Frontend

```bash
cd frontend/chandas-ui
npm run dev
```

Access the frontend at: http://localhost:5173

## 💻 API Usage

### Request Format

```json
{
  "verse": "यो वै स परम ब्रह्म तस्य नाम सत्यम्।"
}
```

### Response Format

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
  ]
}
```

### Python Example

```python
import requests

url = "http://localhost:8000/analyze-verse"
verse = "यो वै स परम ब्रह्म तस्य नाम सत्यम्।"

response = requests.post(url, json={"verse": verse})
result = response.json()

print(f"Meter: {result['best_prediction']['chandas']}")
print(f"Confidence: {result['best_prediction']['confidence']:.1%}")
```

### cURL Example

```bash
curl -X POST http://localhost:8000/analyze-verse \
  -H "Content-Type: application/json" \
  -d '{"verse":"यो वै स परम ब्रह्म तस्य नाम सत्यम्।"}'
```

## 🔧 Model Details

### Features (41 Total)
- Pattern length, Guru/Laghu counts & ratios
- N-gram frequencies (bigrams, trigrams, 4-grams)
- Pattern entropy and complexity metrics
- Position-based features
- Rhythm pattern analysis

### Architecture
- **Ensemble**: Random Forest (500 trees) + Gradient Boosting (300 trees)
- **Calibration**: 5-fold cross-validation sigmoid calibration
- **Scaling**: StandardScaler normalization
- **Explainability**: SHAP TreeExplainer for feature importance

### Performance
- **Inference**: ~100-300ms per verse
- **SHAP Computation**: ~50-100ms per request
- **Memory**: ~500MB (model + features)

## 📊 Supported Meters

1. अनुष्टुभ् (Anuṣṭubh) - 8 syllables
2. इन्द्रवज्रा (Indravajrā) - 11 syllables
3. उपेन्द्रवज्रा (Upendravajrā) - 11 syllables
4. वसन्ततिलका (Vasantatilakā) - 14 syllables
5. मालिनी (Mālinī) - 15 syllables
6. मन्दाक्रान्ता (Mandākrāntā) - 17 syllables
7. शिखरिणी (Śikhariṇī) - 17 syllables
8. शार्दूलविक्रीडितम् (Śārdūlavikrīḍitam) - 19 syllables
9. द्रुतविलम्बितम् (Drutavilambita) - 15 syllables
10. भुजङ्गप्रयातम् (Bhujaṅgaprayāta) - 14 syllables

## 🔍 Technical Stack

**Backend**
- FastAPI - Web framework
- Scikit-learn - Machine learning
- SHAP - Model explainability
- SQLAlchemy - Database ORM
- Uvicorn - ASGI server

**Frontend**
- React/Vue.js - UI framework
- Axios - HTTP client
- Vite - Build tool

**Data Processing**
- Pandas - Data manipulation
- NumPy - Numerical computing

## 📝 Notes

- Confidence scores reflect true model uncertainty (15-50% typical)
- Multiple meters often score within 5-10% of each other due to overlapping patterns
- SHAP values identify which syllable patterns most influenced predictions

## 🎓 References

- Sanskrit Prosody: https://en.wikipedia.org/wiki/Sanskrit_metre
- SHAP: https://github.com/slundberg/shap
- FastAPI: https://fastapi.tiangolo.com/

---

**Status**: ✅ Production Ready | **Last Updated**: 2026-02-05



# Chandas-identification
