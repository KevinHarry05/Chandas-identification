# 🧪 Frontend-Backend Integration Testing Guide

## Pre-Integration Checklist

- [x] Backend is running on `http://127.0.0.1:8000`
- [x] Backend models are loaded correctly
- [x] Frontend dependencies installed (`npm install`)
- [x] `.env` file configured correctly
- [x] No hardcoded paths in either project

---

## Step 1: Verify Backend is Running

### Terminal 1: Start Backend

```bash
cd backend
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

**Expected Output:**
```
INFO:     Started server process [XXXX]
INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:8000
```

### Verify Backend Health

```bash
# In another terminal
curl http://127.0.0.1:8000/

# Expected Response:
# {"message": "Chandas Identifier API - Ready for Sanskrit Meter Analysis"}
```

---

## Step 2: Start Frontend Development Server

### Terminal 2: Start Frontend

```bash
cd frontend/chandas-ui
npm run dev
```

**Expected Output:**
```
  VITE v7.1.14  ready in XXX ms

  ➜  Local:   http://localhost:5173/
```

Visit: `http://localhost:5173`

---

## Step 3: Integration Testing

### Test 1: Backend Connection Status

**What to check:**
1. ✅ Green status indicator says "Backend Connected"
2. ✅ Shows API URL: `http://127.0.0.1:8000`

**If failing:**
- Verify backend is running
- Check `.env` VITE_API_URL value
- Check browser console for errors

---

### Test 2: Analyze Single Verse

**Input verse:**
```
यो वै स परम ब्रह्म तस्य नाम सत्यम्।
```

**Expected result:**
- ✅ Confidence badge shows percentage (e.g., "19.56%")
- ✅ Meter name displays (e.g., "इन्द्रवज्रा")
- ✅ Syllable pattern shows (e.g., "GGLLLLGGLGGLLGG")
- ✅ Alternative meters listed below
- ✅ Top 5 SHAP features visible

**If failing:**
- Check Network tab (F12 → Network)
- Look for POST request to `/analyze-verse`
- Check response status (should be 200)
- Check browser console for JavaScript errors

---

### Test 3: Quick Example Buttons

**Actions:**
1. Click first example button (Indravajra)
2. Verify verse populates in textarea
3. Click "Analyze Verse" button
4. Verify result appears

**Expected:**
- ✅ Textarea fills with example text
- ✅ Analysis completes successfully
- ✅ Results display correctly

---

### Test 4: Error Handling

**Test empty verse:**
1. Leave textarea empty
2. Try to click "Analyze Verse"
3. Button should be disabled (grayed out)

**Test invalid input:**
1. Paste non-Sanskrit text: `"hello world"`
2. Click "Analyze Verse"
3. Should still complete (may not identify correct meter)

**Test backend down:**
1. Stop backend server (Ctrl+C)
2. Try to analyze verse
3. Should show error message with helpful hint

---

### Test 5: Keyboard Shortcuts

**Test Ctrl+Enter submit:**
1. Type a verse in textarea
2. Press Ctrl+Enter (or Cmd+Enter on Mac)
3. Should submit analysis automatically

**Expected:**
- ✅ Analysis starts without clicking button
- ✅ Loading spinner appears
- ✅ Results display when complete

---

### Test 6: Clear Button

**Steps:**
1. Analyze a verse
2. Click "Clear" button
3. Textarea and result should clear

**Expected:**
- ✅ Verse text removed
- ✅ Results removed
- ✅ Character count resets to 0

---

### Test 7: SHAP Explanations

**Check results contain:**

1. **Top 5 Features:**
   - Feature name, value, SHAP value
   - Colors indicate positive/negative

2. **Decision Paths:**
   - Shows decision tree conditions
   - 2-3 paths displayed

3. **Notes:**
   - Explanatory text about SHAP values

**If not displaying:**
- Check backend response includes `explainability` object
- Check browser console for render errors

---

### Test 8: API Documentation Link

**Steps:**
1. Click "📚 API Docs" button
2. Should open in new tab
3. Should see Swagger UI interface

**Expected:**
- ✅ Swagger page loads at `http://127.0.0.1:8000/docs`
- ✅ Can see all endpoints
- ✅ Can test endpoints directly

---

## Step 4: Performance Testing

### Response Time Benchmark

Measure from clicking "Analyze" to results displaying:

**Expected:**
- **First request**: 300-600ms (cold start)
- **Subsequent requests**: 200-400ms
- **Loading indicator**: Should be visible for most of this time

**If slower:**
- Check network latency (F12 → Network)
- Check if backend is running on same machine
- Monitor system resources (CPU, RAM)

---

## Step 5: Browser Compatibility Testing

### Chrome/Edge
- ✅ Test latest version
- ✅ Check DevTools (F12) for errors

### Firefox
- ✅ Test latest version
- ✅ Check console for errors

### Safari
- ✅ Test on macOS/iOS
- ✅ Check if Devanagari displays correctly

---

## Step 6: Responsive Design Testing

### Test on Different Screen Sizes

Use browser DevTools:

**Mobile (375px):**
- ✅ Buttons stack vertically
- ✅ Textarea full width
- ✅ Result card readable
- ✅ No horizontal scroll

**Tablet (768px):**
- ✅ Two-column layout works
- ✅ All elements visible
- ✅ Touch-friendly buttons

**Desktop (1200px+):**
- ✅ Max-width 1000px container
- ✅ Proper spacing
- ✅ Good use of space

---

## Step 7: Accessibility Testing

### Keyboard Navigation

1. Tab through form elements
2. Enter to activate buttons
3. Space to click buttons
4. Ctrl+Enter to submit

**Expected:**
- ✅ All interactive elements reachable
- ✅ Focus indicators visible
- ✅ Proper button/link semantics

### Screen Reader

Using browser accessibility inspector:
- ✅ Form labels associated with inputs
- ✅ Button text meaningful
- ✅ Error messages announced
- ✅ Results structure clear

---

## Debugging Checklist

If tests fail, check these in order:

### Network Issues

```bash
# Check backend is responding
curl -X POST http://127.0.0.1:8000/analyze-verse \
  -H "Content-Type: application/json" \
  -d '{"verse": "यो वै स परम ब्रह्म तस्य नाम सत्यम्।"}'
```

### Frontend Console Errors

Press F12 → Console → Look for red errors

### Backend Logs

Check terminal where backend is running for error messages

### API Configuration

Verify `.env` file:
```bash
cat frontend/chandas-ui/.env
```

Should show:
```
VITE_API_URL=http://127.0.0.1:8000
```

---

## Integration Test Report Template

```markdown
# Integration Test Report - [Date]

## Backend Status
- [ ] Backend running on 127.0.0.1:8000
- [ ] Health check passes
- [ ] Models loaded

## Frontend Status
- [ ] Frontend running on localhost:5173
- [ ] Dependencies installed
- [ ] .env configured

## Test Results

### Connection
- [ ] Backend connected indicator shows green
- [ ] API URL correct

### Verse Analysis
- [ ] Test verse 1: PASS/FAIL
- [ ] Test verse 2: PASS/FAIL
- [ ] Results display correctly: PASS/FAIL

### Error Handling
- [ ] Empty verse shows error: PASS/FAIL
- [ ] Backend down shows error: PASS/FAIL
- [ ] Helpful hints provided: PASS/FAIL

### Performance
- [ ] First request: ___ms
- [ ] Subsequent: ___ms
- [ ] Acceptable: PASS/FAIL

### Features
- [ ] SHAP visualization: PASS/FAIL
- [ ] Decision paths: PASS/FAIL
- [ ] Alternatives: PASS/FAIL
- [ ] Quick examples: PASS/FAIL
- [ ] Keyboard shortcuts: PASS/FAIL

### UI/UX
- [ ] Responsive design: PASS/FAIL
- [ ] Dark mode: PASS/FAIL
- [ ] Accessibility: PASS/FAIL

## Issues Found
(List any bugs or problems)

## Notes
(Any other observations)
```

---

## Common Issues & Solutions

### Issue: "Cannot connect to API"

**Solutions:**
1. Verify backend is running: `ps aux | grep uvicorn`
2. Check port 8000 is listening: `lsof -i :8000`
3. Verify .env: `VITE_API_URL=http://127.0.0.1:8000`
4. Reload frontend page: Ctrl+Shift+R (hard refresh)

### Issue: Verse not analyzing

**Solutions:**
1. Check network tab (F12 → Network → analyze-verse)
2. Look for 200 response status
3. Check response body for errors
4. Verify verse is valid Devanagari

### Issue: SHAP values not showing

**Solutions:**
1. Check backend response includes `explainability` key
2. Verify backend didn't encounter error
3. Check browser console for render errors
4. Verify 41 features were extracted

### Issue: Styling looks broken

**Solutions:**
1. Clear cache: Ctrl+Shift+Delete
2. Hard refresh: Ctrl+Shift+R
3. Check CSS files loaded (F12 → Network → CSS)
4. Check for console errors

---

## Production Readiness Checklist

Before deploying both frontend and backend:

- [ ] All integration tests pass
- [ ] No console errors
- [ ] No network errors
- [ ] Performance acceptable
- [ ] Environment variables updated
- [ ] Backend deployment ready
- [ ] Frontend build created (`npm run build`)
- [ ] CORS configured for production domain
- [ ] API URL points to production endpoint
- [ ] Error messages user-friendly
- [ ] Security review completed

---

## Performance Metrics

### Target Metrics

| Metric | Target | Actual |
|--------|--------|--------|
| Frontend build size | < 500KB | _____ |
| First API call | < 600ms | _____ |
| Subsequent calls | < 400ms | _____ |
| Page load time | < 2s | _____ |
| SHAP computation | < 500ms | _____ |

---

## Sign Off

- **Tested By:** _______________
- **Date:** _______________
- **Status:** ☐ Pass ☐ Fail
- **Notes:** _______________

**Integration testing complete!** ✅

