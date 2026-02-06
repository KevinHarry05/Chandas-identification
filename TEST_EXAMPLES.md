# 🧪 MANUAL TEST EXAMPLES FOR API
# Use these to test the backend manually with curl, Python, or Postman

## Example 1: Indravajra Meter
{
  "verse": "यो वै स परम ब्रह्म तस्य नाम सत्यम्।"
}

---

## Example 2: Mandakranta Meter
{
  "verse": "मा गमो यातन प्रिये भरत।"
}

---

## Example 3: Vasantatilaka Meter
{
  "verse": "नमो देवाय सर्वज्ञाय प्रभवे।"
}

---

## Example 4: Anushtubh Meter
{
  "verse": "रामराज्यं नृपतेः कृतं।"
}

---

## Example 5: Malini Meter
{
  "verse": "आदित्यो जगतो जन्मदो विष्णुः।"
}

---

## Example 6: Shikhariṇī Meter
{
  "verse": "त्वं देवो दिवि रमणीय धरणे।"
}

---

## Example 7: Upendravajra Meter
{
  "verse": "देवदेव महायोगी जगन्नाथ।"
}

---

## Example 8: Bhujaṅgaprayāta Meter
{
  "verse": "भगवान भवसागरोद्धारक।"
}

---

## Example 9: Drutavilambita Meter
{
  "verse": "सर्वे मिलित्वा गीतं गायन्ति।"
}

---

## Example 10: Saradula Vikridita Meter
{
  "verse": "ज्ञानी ज्ञानमयं ब्रह्ममयीं वाचं पश्यति।"
}

---

# 🔧 HOW TO TEST MANUALLY

## Using cURL (Windows PowerShell):

```powershell
# Example 1
$body = @{
    verse = "यो वै स परम ब्रह्म तस्य नाम सत्यम्।"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/analyze-verse" `
  -Method POST `
  -Headers @{"Content-Type"="application/json"} `
  -Body $body | Format-Table
```

## Using Python:

```python
import requests
import json

# Start backend first: python -m uvicorn app.main:app --host 127.0.0.1 --port 8000

verses = [
    "यो वै स परम ब्रह्म तस्य नाम सत्यम्।",
    "मा गमो यातन प्रिये भरत।",
    "नमो देवाय सर्वज्ञाय प्रभवे।",
    "रामराज्यं नृपतेः कृतं।",
]

for verse in verses:
    response = requests.post(
        "http://localhost:8000/analyze-verse",
        json={"verse": verse},
        timeout=10
    )
    
    if response.status_code == 200:
        data = response.json()
        print(f"\n📖 Verse: {verse}")
        print(f"📊 Meter: {data['best_prediction']['chandas']}")
        print(f"📈 Confidence: {data['best_prediction']['confidence']:.2%}")
        print(f"🔤 Pattern: {data['laghu_guru_pattern']}")
    else:
        print(f"Error: {response.status_code}")
```

## Using Postman / Thunder Client:

1. **Method**: POST
2. **URL**: http://localhost:8000/analyze-verse
3. **Headers**:
   ```
   Content-Type: application/json
   ```
4. **Body (raw JSON)**:
   ```json
   {
     "verse": "यो वै स परम ब्रह्म तस्य नाम सत्यम्।"
   }
   ```

---

# 📊 EXPECTED RESPONSES

## Success Response (200 OK):

```json
{
  "verse": "यो वै स परम ब्रह्म तस्य नाम सत्यम्।",
  "laghu_guru_pattern": "GGLLLLGGLGGLLGG",
  "best_prediction": {
    "class_index": 1,
    "chandas": "इन्द्रवज्रा",
    "confidence": 0.19558406067564707
  },
  "alternatives": [
    {
      "class_index": 5,
      "chandas": "मन्दाक्रान्ता",
      "confidence": 0.18787941921517695
    },
    {
      "class_index": 7,
      "chandas": "वसन्ततिलका",
      "confidence": 0.12917352537967322
    }
  ],
  "explainability": {
    "shap_values": [...],
    "decision_paths": [...],
    "top_features": [...]
  }
}
```

## Error Response (400 Bad Request):

```json
{
  "detail": "Verse cannot be empty"
}
```

---

# 🎯 TESTING CHECKLIST

✅ Test with each verse
✅ Verify confidence scores are between 0 and 1
✅ Check that alternatives are present
✅ Confirm pattern extraction works (L and G characters)
✅ Validate SHAP explanations are included
✅ Test error handling (empty verse, very long text, etc.)

---

# 🌐 API ENDPOINTS AVAILABLE

- **GET** http://localhost:8000/ → Health check
- **POST** http://localhost:8000/analyze-verse → Analyze verse
- **GET** http://localhost:8000/docs → Swagger UI (interactive)
- **GET** http://localhost:8000/redoc → ReDoc documentation
