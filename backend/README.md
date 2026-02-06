# Chandas Identifier - Backend API

AI-powered Sanskrit Chandas (meter) identification system with Explainable AI capabilities.

## 🎯 Overview

This backend provides RESTful APIs for identifying Sanskrit poetic meters (chandas) from Devanagari text using Machine Learning with explainability features through SHAP values, decision paths, and counterfactual explanations.

## 🏗️ Architecture

```
backend/
├── app/
│   ├── main.py                 # FastAPI application with CORS
│   ├── api/
│   │   └── routes.py           # API endpoints with validation
│   └── core/
│       ├── text/
│       │   ├── laghu_guru.py   # Syllable pattern extraction
│       │   └── normalize.py    # Text normalization
│       ├── ml/
│       │   ├── model_loader.py      # Model loading
│       │   ├── predict.py           # Prediction engine
│       │   ├── features.py          # Feature engineering
│       │   ├── load_full_data.py    # Dataset loader
│       │   ├── train_full_model.py  # Training script
│       │   ├── shap_xai.py          # SHAP explainability
│       │   ├── decision_path_xai.py # Decision paths
│       │   └── counterfactual_xai.py # Counterfactuals
│       └── db/
│           ├── db_config.py    # Database configuration
│           └── db_utils.py     # Database operations (SQL-injection safe)
├── models/
│   ├── random_forest.pkl       # Trained ML model
│   ├── labels.pkl              # Class labels
│   └── model_metadata.json     # Training metrics
├── requirements.txt            # Python dependencies
├── .env                        # Environment configuration
└── README.md                   # This file
```

## 🚀 Quick Start

### Prerequisites

- Python 3.9+
- PostgreSQL 13+ (optional, for database features)
- pip or conda

### Installation

1. **Clone the repository**
```bash
cd backend
```

2. **Create virtual environment**
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure environment**
```bash
# Copy example env file
copy .env.example .env  # Windows
cp .env.example .env    # Linux/Mac

# Edit .env with your configuration
```

5. **Train the model** (first time only)
```bash
python -m backend.app.core.ml.train_full_model
```

This will:
- Load all examples from `data/examples.json`
- Extract Laghu-Guru patterns from Sanskrit text
- Train Random Forest classifier
- Perform cross-validation
- Save model to `models/` directory

6. **Run the server**
```bash
uvicorn backend.app.main:app --reload --host 0.0.0.0 --port 8000
```

API will be available at: `http://localhost:8000`

## 📡 API Endpoints

### POST /analyze-verse

Analyze a Sanskrit verse and identify its chandas (meter).

**Request:**
```json
{
  "verse": "यदा यदा हि धर्मस्य\nग्लानिर्भवति भारत।\nअभ्युत्थानमधर्मस्य\nतदात्मानं सृजाम्यहम्॥"
}
```

**Response:**
```json
{
  "verse": "यदा यदा हि धर्मस्य...",
  "laghu_guru_pattern": "LLGLGLLG",
  "best_prediction": {
    "class_index": 0,
    "chandas": "अनुष्टुभ्",
    "confidence": 0.95
  },
  "alternatives": [
    {
      "class_index": 1,
      "chandas": "इन्द्रवज्रा",
      "confidence": 0.03
    },
    {
      "class_index": 2,
      "chandas": "उपेन्द्रवज्रा",
      "confidence": 0.02
    }
  ]
}
```

**Validation:**
- Verse must contain Devanagari characters (U+0900 to U+097F)
- Length: 1-5000 characters
- Automatically removes invalid characters
- Raises 400 error for invalid input

### API Documentation

Interactive API docs available at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## 🧠 Machine Learning Pipeline

### 1. Text Processing
```python
from backend.app.core.text.laghu_guru import extract_laghu_guru_pattern

pattern = extract_laghu_guru_pattern("यदा यदा हि धर्मस्य")
# Returns: "LLGLGLLG"
```

**Rules:**
- **Guru (G)**: Long vowels (आ, ई, ऊ, ए, ऐ, ओ, औ), consonant clusters (halant), anusvara (ं), visarga (ः)
- **Laghu (L)**: Short vowels (अ, इ, उ, ऋ)

### 2. Feature Engineering
```python
from backend.app.core.ml.features import build_feature_df

features = build_feature_df("LLGLGLLG")
# Returns DataFrame with:
# - pattern_length: 8.0
# - guru_count: 3.0
# - laghu_count: 5.0
# - guru_laghu_ratio: 0.6
```

### 3. Model Training

**Algorithm:** Random Forest Classifier
- **Trees:** 200 estimators
- **Max Depth:** 20
- **Class Weight:** Balanced (handles imbalance)
- **Features:** 4 numerical features
- **Validation:** 5-fold cross-validation + 20% test split

**Performance Metrics:**
```bash
python -m backend.app.core.ml.train_full_model
```

Outputs:
- Test accuracy
- Cross-validation scores
- Feature importance
- Classification report
- Confusion matrix

### 4. Prediction
```python
from backend.app.core.ml.predict import predict_proba_with_labels

predictions = predict_proba_with_labels("LLGLGLLG")
# Returns sorted list of predictions with confidence scores
```

## 🔍 Explainable AI (XAI)

### SHAP Values
```python
from backend.app.core.ml.shap_xai import compute_shap_values

shap_values = compute_shap_values(feature_df, class_index=0)
# Returns feature contributions to prediction
```

### Decision Paths
```python
from backend.app.core.ml.decision_path_xai import extract_decision_paths

paths = extract_decision_paths(model, feature_vector, feature_names)
# Returns decision rules from Random Forest trees
```

### Counterfactuals
```python
from backend.app.core.ml.counterfactual_xai import generate_counterfactuals

counterfactuals = generate_counterfactuals(model, feature_vector, original_pred)
# Returns minimal feature changes for different predictions
```

## 🗄️ Database Setup (Optional)

The backend supports PostgreSQL for storing prediction history.

### 1. Create Database
```sql
CREATE DATABASE chandas_db;
\c chandas_db

CREATE TABLE chandas_predictions (
    id SERIAL PRIMARY KEY,
    pattern VARCHAR(1000) NOT NULL,
    predicted_chandas VARCHAR(100) NOT NULL,
    confidence FLOAT,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_predicted_chandas ON chandas_predictions(predicted_chandas);
CREATE INDEX idx_created_at ON chandas_predictions(created_at);
```

### 2. Configure .env
```bash
DB_NAME=chandas_db
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
```

### 3. Test Connection
```python
from backend.app.core.db.db_utils import test_connection

test_connection()  # Should return True if successful
```

## 🔒 Security Features

✅ **SQL Injection Prevention**: Parameterized queries  
✅ **Input Validation**: Pydantic validators  
✅ **CORS Protection**: Configured allowed origins  
✅ **Character Filtering**: Only Devanagari + punctuation allowed  
✅ **Length Limits**: Max 5000 characters per verse  

## 📊 Supported Chandas

The model currently identifies these meters:

1. **अनुष्टुभ्** (Anuṣṭubh)
2. **इन्द्रवज्रा** (Indravajrā)
3. **उपेन्द्रवज्रा** (Upendravajrā)
4. **वसन्ततिलका** (Vasantatilakā)
5. **शार्दूलविक्रीडितम्** (Śārdūlavikrīḍitam)
6. **शिखरिणी** (Śikhariṇī)
7. **मालिनी** (Mālinī)
8. **मन्दाक्रान्ता** (Mandākrāntā)
9. **भुजङ्गप्रयातम्** (Bhujaṅgaprayātam)
10. **द्रुतविलम्बितम्** (Drutavilam bitam)

*Note: Expand by adding more examples to `data/examples.json` and retraining.*

## 🧪 Testing

```bash
# Test pattern extraction
python -m backend.app.core.text.laghu_guru

# Test model loading
python -m backend.app.core.ml.model_loader

# Test prediction
python -m backend.app.core.ml.predict

# Test data loading
python -m backend.app.core.ml.load_full_data

# Test database connection
python -m backend.app.core.db.test_db
```

## 🔧 Configuration

### Environment Variables (.env)

```bash
# Database
DB_NAME=chandas_db
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432

# API
API_HOST=0.0.0.0
API_PORT=8000
API_RELOAD=True

# Model
MODEL_PATH=models/random_forest.pkl
LABELS_PATH=models/labels.pkl

# Logging
LOG_LEVEL=INFO
```

### CORS Origins

Edit [main.py](app/main.py) to add allowed origins:

```python
allow_origins=[
    "http://localhost:5173",  # Vite dev
    "http://localhost:3000",  # React dev
    "https://yourdomain.com", # Production
]
```

## 📈 Performance Optimization

**Tips for production:**

1. **Use gunicorn** instead of uvicorn
```bash
pip install gunicorn
gunicorn -w 4 -k uvicorn.workers.UvicornWorker backend.app.main:app
```

2. **Enable model caching** (already implemented in model_loader.py)

3. **Add Redis** for caching predictions

4. **Database connection pooling**
```python
# Use pgbouncer or SQLAlchemy connection pool
```

5. **Async database queries**
```python
# Use asyncpg instead of psycopg2
```

## 🐛 Troubleshooting

### Model not found
```bash
python -m backend.app.core.ml.train_full_model
```

### Database connection fails
- Check PostgreSQL is running
- Verify credentials in `.env`
- Test: `python -m backend.app.core.db.test_db`

### CORS errors
- Add your frontend URL to `allow_origins` in `main.py`
- Check frontend is using correct API URL

### Import errors
- Ensure working directory is project root
- Use absolute imports: `from backend.app...`

## 📚 Dependencies

See [requirements.txt](requirements.txt) for full list:

**Core:**
- fastapi 0.115.0
- uvicorn 0.32.0
- pandas 2.2.3
- scikit-learn 1.5.2
- shap 0.46.0

**Database:**
- psycopg2-binary 2.9.10
- python-dotenv 1.0.1

**Validation:**
- pydantic 2.9.2

## 🤝 Contributing

To add new chandas types:

1. Add examples to `data/examples.json`
2. Run retraining: `python -m backend.app.core.ml.train_full_model`
3. Model automatically saved to `models/`

## 📄 License

MIT License - See LICENSE file

## 👥 Authors

AI/ML Sanskrit Prosody Research Team

## 📞 Support

For issues or questions:
- Open GitHub issue
- Check API docs: `http://localhost:8000/docs`
- Review code comments

---

**Note:** This is an AI/ML-based system with NO HARDCODING. All predictions are data-driven from the training corpus in `examples.json`.
