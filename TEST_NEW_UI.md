# 🧪 How to Test the New UI

## Quick Start (5 minutes)

### Step 1: Start Backend
```bash
cd backend
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

### Step 2: Start Frontend
```bash
cd frontend/chandas-ui
npm run dev
```

### Step 3: Open Browser
```
http://localhost:5173
```

---

## What to Look For

### 1. Main Prediction Card ✅

**Visual Checks:**
- ✓ Green gradient background on main card
- ✓ Meter icon (🎭) bounces when displayed
- ✓ Confidence percentage shows (e.g., "26%")
- ✓ Confidence bar fills smoothly with animation
- ✓ Main meter name is large and prominent
- ✓ Description text explains the result

**Test Verse:**
Copy and paste:
```
यो वै स परम ब्रह्म तस्य नाम सत्यम्।
```
Click "Analyze Verse"

**Expected Results:**
- ✓ Blue "Backend Connected" status appears
- ✓ Loading spinner shows briefly
- ✓ Results slide in smoothly
- ✓ Confidence indicator shows in top right
- ✓ Syllable pattern displays with colored boxes

---

### 2. Syllable Pattern Display ✅

**Visual Checks:**
- ✓ Pattern shows as colored boxes (not text)
- ✓ Yellow boxes = Guru (G)
- ✓ Blue boxes = Laghu (L)
- ✓ Proper spacing between syllables
- ✓ Pattern matches the verse

**What to Verify:**
- Hover over boxes → they should highlight
- Verify pattern makes sense for the verse
- Check that it matches the main prediction

---

### 3. Alternative Meters Section ✅

**Visual Checks:**
- ✓ Section title: "📊 Other Possible Meters"
- ✓ Intro text: "These meters also match reasonably well:"
- ✓ Cards have purple left border
- ✓ Numbered badges (②, ③, ④)
- ✓ Purple confidence badges
- ✓ Progress bars show confidence

**Interaction Tests:**
- Hover over cards → they should lift and change color
- Verify confidence percentages are in order (highest first)
- Check that bar lengths match percentages

---

### 4. Feature Importance (SHAP) - THE KEY TEST! ✅

**Visual Checks:**
- ✓ Section title: "🔍 Why This Meter?"
- ✓ Subtitle: "These features are most important..."
- ✓ 5 features displayed with rankings (①②③④⑤)
- ✓ Green checkmark (✓) for supporting features
- ✓ Red X (✗) for features that don't support

**Check Each Feature Card:**

**Feature #1 (Top):**
- [ ] Ranked #1 with green badge
- [ ] Feature name is readable (e.g., "LARGE GURU COUNT")
- [ ] Impact badge shows (e.g., "✓ strongly increases")
- [ ] Value displayed (e.g., "Value: 3.90")
- [ ] Impact score displayed (e.g., "Impact: +0.048")
- [ ] Green gradient bar shown (supporting feature)
- [ ] Card has light green background

**Feature #2:**
- [ ] Different color (might be blue or pink based on strength)
- [ ] If negative impact: ✗ red badge, red bar
- [ ] Card background color differs from #1
- [ ] Text explains the impact direction

**Check Color Coding:**
- ✓ Green backgrounds = strong positive impact
- ✓ Blue backgrounds = positive impact
- ✓ Pink backgrounds = negative impact
- ✓ Gray backgrounds = weak impact

**Check Explanation Text:**
Text should say something like:
- "✓ strongly increases the prediction" (green)
- "✓ moderately increases the prediction" (blue)
- "✗ moderately decreases the prediction" (red)
- "✓ slightly increases the prediction" (weak green)

**The SHAP Explanation Box:**
At the bottom should say:
> 💡 How to read: Each feature is ranked by how much it helped or hurt
> the model's decision. Green ✓ features support the prediction, while
> Red ✗ features suggest other meters might fit better.

---

### 5. Decision Paths Section ✅

**Visual Checks:**
- ✓ Title: "🌳 How the Model Decided"
- ✓ Subtitle: "Step-by-step decision logic"
- ✓ Dark header bar for each path
- ✓ Numbered steps (①②③...)
- ✓ Blue left border on steps
- ✓ White boxes for conditions
- ✓ Dark background (contrasts with white boxes)

**Interaction Tests:**
- Hover over steps → background should change to light blue
- Verify steps make sense
- Check that conditions are readable

---

### 6. Metadata Section ✅

**Should Show:**
- [ ] 🤖 AI Model: Ensemble (Random Forest + Gradient Boosting)
- [ ] 📊 Features Analyzed: 41
- [ ] 🔍 Explanation Method: SHAP

**Verification:**
- Information is accurate
- Icons display properly
- Text is readable

---

## Responsive Testing

### Mobile (375px)
Test on phone or DevTools (F12 → Click device icon)

**Checklist:**
- [ ] Results card full width (no overflow)
- [ ] Buttons stacked vertically
- [ ] Text remains readable
- [ ] No horizontal scrolling needed
- [ ] Features stack properly
- [ ] Pattern visualization doesn't overflow

```bash
# In DevTools, press Ctrl+Shift+M to toggle mobile view
```

### Tablet (768px)
**Checklist:**
- [ ] Layout is optimized for tablet
- [ ] Proper spacing between sections
- [ ] Cards have good size
- [ ] Touch targets are large (≥44px)

### Desktop (1200px+)
**Checklist:**
- [ ] Optimal spacing
- [ ] Full feature set visible
- [ ] All hover effects work
- [ ] Perfect typography

---

## Dark Mode Testing

### Enable Dark Mode
**On Mac:**
- System Preferences → General → Dark

**On Windows:**
- Settings → Personalization → Colors → Dark

**In Browser (DevTools):**
```
F12 → More tools → Rendering → Emulate CSS media feature prefers-color-scheme
```

**Checklist:**
- [ ] Colors adjust automatically
- [ ] Text still readable
- [ ] Backgrounds are dark
- [ ] Gradients look good
- [ ] All sections properly themed
- [ ] No white text on light backgrounds

---

## Animation & Interaction Testing

### Result Slide-In Animation
- [ ] When results appear, they slide in from top
- [ ] Animation is smooth (not jerky)
- [ ] Duration ~0.4s
- [ ] Opacity fades in while sliding

### Meter Icon Animation
- [ ] Icon bounces when displayed
- [ ] Bounce is smooth and playful
- [ ] Animates once when results appear

### Hover Effects
- [ ] Prediction card lifts slightly on hover
- [ ] Shadow increases on hover
- [ ] Alternative cards slide right slightly
- [ ] Feature cards transform left
- [ ] Smooth transitions (no jumps)

### Progress Bars
- [ ] Bars fill smoothly with animation
- [ ] Duration ~0.6s
- [ ] Easing function is smooth
- [ ] No jank or stuttering

### Loading Spinner
- [ ] Spins smoothly
- [ ] Rotates 360° continuously
- [ ] Border color is visible
- [ ] Stops when results appear

---

## Keyboard Navigation

**Test with Tab Key:**
- [ ] Tab through all interactive elements
- [ ] Focus visible on buttons (ring or outline)
- [ ] Focus order makes sense
- [ ] Can activate buttons with Enter
- [ ] Shortcuts work (Ctrl+Enter to submit)

---

## Color Contrast Testing

**For Accessibility:**
- [ ] Text on buttons readable
- [ ] All text meets WCAG AA standard
- [ ] Light text on dark backgrounds (≥4.5:1 contrast)
- [ ] Color not the only indicator (use symbols like ✓ and ✗)

Test with:
```
Browser: Built-in DevTools → Accessibility
Or: https://webaim.org/resources/contrastchecker/
```

---

## Performance Testing

### Load Time
```
DevTools → Performance tab → Click "Record"
1. Analyze verse
2. Stop recording
Expected: < 2 seconds total
```

### API Response Time
```
DevTools → Network tab
Look at /analyze-verse request
Expected: 300-600ms
```

### Frame Rate
```
DevTools → Rendering → Frame Rate Monitor
While hovering/animating
Expected: 60 FPS (smooth)
```

---

## Browser Compatibility Testing

**Test on:**
- [ ] Chrome 120+
- [ ] Firefox 121+
- [ ] Safari 17+
- [ ] Edge 120+

**Check:**
- [ ] Layout correct
- [ ] Animations smooth
- [ ] Colors display properly
- [ ] No console errors

---

## Common Issues & Solutions

| Issue | Solution |
|-------|----------|
| Features not showing | Refresh page, check API response |
| Colors look wrong | Check dark mode is not enabled (or is) |
| Text overlapping | Zoom out (Ctrl+-) or try mobile view |
| Animations stuttering | Close other browser tabs, GPU acceleration enabled |
| Bars not filling | Wait for animation to complete |
| Pattern not showing | Refresh page, check API response |

---

## Success Criteria

✅ **Core Features:**
- [x] SHAP values shown in human-readable format
- [x] Features color-coded by strength
- [x] Confidence indicator prominent
- [x] Pattern visualization works
- [x] Alternative meters display

✅ **Design:**
- [x] Professional appearance
- [x] Smooth animations
- [x] Proper spacing
- [x] Good typography
- [x] Color hierarchy clear

✅ **Responsive:**
- [x] Works on mobile
- [x] Works on tablet
- [x] Works on desktop
- [x] No overflow
- [x] Touch-friendly

✅ **Accessibility:**
- [x] Dark mode support
- [x] Proper contrast
- [x] Keyboard navigation
- [x] Semantic HTML
- [x] WCAG compliant

✅ **Performance:**
- [x] Fast load times
- [x] Smooth animations (60 FPS)
- [x] No lag
- [x] Proper caching

---

## Quick Test Command

Run all tests in sequence:

```bash
# 1. Start backend
cd backend && python -m uvicorn app.main:app --reload &

# 2. Start frontend
cd ../frontend/chandas-ui && npm run dev

# 3. In browser: http://localhost:5173
# Test verse from TEST_EXAMPLES.md
```

---

## Expected Output Example

When you analyze: `यो वै स परम ब्रह्म तस्य नाम सत्यम्।`

You should see:
```
🎭 इन्द्रवज्रा (26.74% confidence)

Alternatives:
② मन्दाक्रान्ता (23.08%)
③ अनुष्टुभ (13.60%)

Top Features:
① LARGE GURU COUNT ✓ strongly increases
② LARGE LAGHU COUNT ✗ moderately decreases
③ LAGHU COUNT ✓ slightly increases
...

Decision paths with steps
Model info
```

**If you see all this, the UI is working perfectly!** ✅

---

## Need Help?

Check these files for more info:
- `FRONTEND_GUIDE.md` - Complete frontend docs
- `INTEGRATION_TESTING.md` - Detailed testing guide
- `UI_IMPROVEMENTS.md` - What was improved
- `BEFORE_AFTER_COMPARISON.md` - Visual changes

---

**Ready to test? Start with the Quick Start section!** 🚀
