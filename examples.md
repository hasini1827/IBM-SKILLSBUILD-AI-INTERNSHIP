
### 🔴 Example 1: Obvious Fake News (Expected Score: 0-30)

```
BREAKING NEWS: Scientists SHOCKED by discovery of aliens living among us!
You won't believe what government has been hiding for decades in secret underground 
base! This one weird trick will expose the TRUTH they don't want you to know! 
Doctors HATE this! Sources claim that everything you've been told is a LIE! 
Some say this will change EVERYTHING! Click here to learn the shocking truth! Miracle cure discovered! Unbelievable findings that mainstream media refuses to report!
```

**Expected Results:**
- Credibility Score: 15-25/100
- Verdict: Likely Unreliable (Red)
- Flags:
  - Contains excessive sensational language
  - Excessive use of capital letters
  - Excessive exclamation marks
  - Contains vague or unattributed claims

---

### 🟢 Example 2: Credible News (Expected Score: 75-95)

```
Renewable Energy Study Shows Promise for Battery Technology

According to a peer-reviewed study published in the journal Nature Energy, researchers 
at the Massachusetts Institute of Technology have developed a new approach to lithium-ion 
battery storage that could improve efficiency by up to 25 percent.

The research team, led by Dr. Sarah Chen, analyzed data from over 150 experimental 
trials conducted over an 18-month period. The findings were independently verified 
by scientists at Stanford University before publication.

"Our research demonstrates that by modifying the electrode composition, we can 
significantly reduce charging time while maintaining battery longevity," Dr. Chen 
explained in an interview with Science Daily.

The study was funded by the Department of Energy and underwent rigorous peer review. 
The complete methodology and data sets are available in the published paper for 
independent verification.
```

**Expected Results:**
- Credibility Score: 80-90/100
- Verdict: Likely Reliable (Green)
- Flags:
  - References credible sources or research
---

### 🟡 Example 3: Questionable Content (Expected Score: 40-65)

```
New Health Trend Taking Social Media by Storm

A new wellness trend is reportedly sweeping across Instagram and TikTok, with 
influencers claiming amazing results. Some say this simple morning routine can 
boost energy levels and improve overall health.

Many believe that this approach, which allegedly originated from ancient practices, 
could be the answer people have been looking for. Sources claim that thousands 
have already tried it with varying degrees of success.

While some health experts remain skeptical, supporters argue that the anecdotal 
evidence speaks for itself. The trend continues to gain popularity despite the 
lack of scientific studies.
```

**Expected Results:**
- Credibility Score: 45-60/100
- Verdict: Questionable - Verify Claims (Orange)
- Flags:
  - Contains some sensational language

---

### 🟢 Example 4: Academic Research Report (Expected Score: 80-95)

```
Climate Change Impact on Coastal Ecosystems: New Research Findings

A comprehensive study published in the journal Environmental Science & Technology 
has revealed significant impacts of rising sea temperatures on coastal marine 
ecosystems. The research, conducted by an international team from the University 
of California, Berkeley, and the Woods Hole Oceanographic Institution, analyzed 
data collected from 75 coastal sites across five continents over a decade.

Dr. Michael Rodriguez, lead author of the study, stated, "Our data shows a clear 
correlation between temperature increases and changes in species distribution 
patterns." The research utilized advanced statistical methods and was peer-reviewed 
by independent experts in marine biology and climate science.

The study's findings align with previous research published in Nature Climate Change 
and provide additional evidence for the need to address climate-related challenges. 
The complete dataset and methodology are publicly available for scientific scrutiny.

This research was supported by grants from the National Science Foundation and the 
National Oceanic and Atmospheric Administration.
```

**Expected Results:**
- Credibility Score: 85-95/100
- Verdict: Likely Reliable (Green)
- Flags:
  - References credible sources or research

---

### 🔴 Example 5: Conspiracy Theory (Expected Score: 10-30)

```
EXPOSED: The TRUTH About What They're Hiding!

Wake up people! The mainstream media won't tell you this but EVERYTHING you know 
is WRONG! Secret organizations are controlling what you see and hear!

Some say that powerful elites have been manipulating events for centuries. Sources 
claim that the evidence is everywhere if you just OPEN YOUR EYES! This shocking 
revelation will blow your mind!

They don't want you to know the truth! Share this before it gets DELETED! The 
time to act is NOW! Don't be a sheep - do your own research!

BREAKING: Whistleblower reveals what they've been hiding! You won't believe this!
```

**Expected Results:**
- Credibility Score: 10-25/100
- Verdict: Likely Unreliable (Red)
- Flags:
  - Contains excessive sensational language
  - Excessive use of capital letters
  - Excessive exclamation marks
  - Contains vague or unattributed claims

---

### 🟡 Example 6: Opinion Piece (Expected Score: 50-70)

```
Why We Need to Rethink Our Approach to Technology Education

As someone who has worked in education for over 15 years, I believe we need to 
fundamentally change how we teach technology in schools. While I don't have 
empirical data to support every claim, my experience suggests that current methods 
are not preparing students adequately for the digital age.

In my view, the focus should shift from teaching specific software tools to 
developing critical thinking skills around technology use. This is based on 
observations from my own classroom and conversations with fellow educators.

Some might argue that traditional approaches still have value, and I acknowledge 
that perspective. However, I think the rapid pace of technological change demands 
a more adaptive approach to education.
```

**Expected Results:**
- Credibility Score: 55-70/100
- Verdict: Questionable - Verify Claims (Orange)
- Flags:
  - May contain some vague claims
  - Opinion-based rather than evidence-based

---

## URL Examples

### Reliable News Sources (Expected: High Scores)
Try these types of URLs:
- Major news outlets: BBC, Reuters, Associated Press
- Academic institutions: .edu domains
- Government sources: .gov domains
- Scientific journals: Nature, Science, PLOS

### Questionable Sources (Expected: Medium Scores)
- Tabloid websites
- Heavily biased news sites
- Blogs without clear authorship
- Sites with sensational headlines

### Unreliable Sources (Expected: Low Scores)
- Known fake news sites
- Satire sites (The Onion, Babylon Bee)
- Conspiracy theory websites
- Sites with no "About" section

---

## Testing Scenarios

### Scenario 1: Student Homework Verification

**Context**: Student finds an article for a research paper

**Test Article**:
```
According to research published by Harvard Medical School, regular exercise 
has been shown to improve cognitive function in older adults. The study, 
which followed 500 participants over five years, found that those who 
exercised at least three times per week showed better memory retention 
compared to sedentary individuals. The findings were published in the 
Journal of Aging Research.
```

**Expected Outcome**: High credibility score, suitable for academic citation

---

### Scenario 2: Social Media Claim Check

**Context**: Viral post making health claims

**Test Article**:
```
DOCTORS SHOCKED! This one simple trick will cure all diseases! Big Pharma 
doesn't want you to know about this miracle remedy that has been hidden 
for centuries! Click to discover the secret!
```

**Expected Outcome**: Very low credibility score, clear warning signs

---

### Scenario 3: News Article Verification

**Context**: Breaking news story verification

**Test Article**:
```
Local authorities reported today that a traffic accident on Highway 101 
resulted in temporary lane closures. According to Police Chief John Smith, 
no injuries were reported. The highway was reopened to traffic at 3 PM 
following cleanup operations. Drivers are advised to expect minor delays 
in the area.
```

**Expected Outcome**: Moderate to high credibility, factual reporting

---

### Scenario 4: Scientific Claim Evaluation

**Context**: Evaluating a scientific breakthrough claim

**Test Article**:
```
Scientists at CERN announced preliminary results from recent particle 
collision experiments. The data, which is still undergoing peer review, 
suggests potential anomalies in particle behavior. Dr. Elena Martinez, 
lead physicist on the project, emphasized that further analysis is needed 
before drawing conclusions. The team plans to publish their findings in 
Physical Review Letters pending peer review completion.
```

**Expected Outcome**: High credibility, proper scientific process described

---

## Edge Cases to Test

### 1. Very Short Text
```
Breaking news: Something happened.
```
**Expected**: Error message (text too short)

### 2. All Caps Text
```
BREAKING NEWS ALERT EVERYONE NEEDS TO SEE THIS RIGHT NOW SHARE IMMEDIATELY
```
**Expected**: Low score, excessive caps flag

### 3. Mixed Quality Content
```
According to a study, researchers found interesting results. You won't 
believe what they discovered! The peer-reviewed paper shows shocking data 
that will change everything!
```
**Expected**: Medium score, mixed signals

### 4. Satire/Humor
```
In a stunning development, local cat elected mayor after promising more 
nap time for all citizens. The feline candidate won by a landslide, 
receiving 100% of the catnip vote. City officials report that the new 
mayor has already implemented mandatory belly rub sessions.
```
**Expected**: Low-medium score (satire often triggers fake news patterns)

### 5. Technical/Academic Language
```
The implementation of quantum error correction protocols utilizing 
surface codes demonstrates significant improvements in qubit coherence 
times, as evidenced by experimental data from superconducting quantum 
processors operating at millikelvin temperatures.
```
**Expected**: Medium-high score (technical but lacks source attribution)

---

## API Testing with cURL

### Test 1: Analyze Text
```bash
curl -X POST http://localhost:5000/api/analyze \
  -H "Content-Type: application/json" \
  -d '{"text": "According to a peer-reviewed study published in Nature..."}'
```

### Test 2: Analyze URL
```bash
curl -X POST http://localhost:5000/api/analyze \
  -H "Content-Type: application/json" \
  -d '{"url": "https://www.bbc.com/news/example-article"}'
```

### Test 3: Get Tips
```bash
curl http://localhost:5000/api/tips
```

### Test 4: Health Check
```bash
curl http://localhost:5000/api/health
```

---

## Python Testing Script

```python
import requests

API_URL = "http://localhost:5000/api/analyze"

test_cases = [
    {
        "name": "Fake News",
        "text": "BREAKING: Aliens discovered! You won't believe this!",
        "expected_range": (0, 40)
    },
    {
        "name": "Real News",
        "text": "According to a study published in Nature, researchers found...",
        "expected_range": (60, 100)
    }
]

for test in test_cases:
    response = requests.post(API_URL, json={"text": test["text"]})
    result = response.json()
    score = result["credibility_score"]
    
    print(f"\nTest: {test['name']}")
    print(f"Score: {score}")
    print(f"Expected: {test['expected_range']}")
    print(f"Pass: {test['expected_range'][0] <= score <= test['expected_range'][1]}")
```

## Expected Behavior Summary

| Content Type | Score Range | Verdict | Common Flags |
|-------------|-------------|---------|--------------|
| Academic Research | 80-95 | Reliable | Credible sources |
| Mainstream News | 70-85 | Reliable | Some attribution |
| Opinion Pieces | 50-70 | Questionable | Vague claims |
| Tabloid Content | 30-50 | Questionable | Sensational language |
| Conspiracy Theory | 10-30 | Unreliable | Multiple red flags |
| Obvious Fake News | 0-20 | Unreliable | All red flags |

---
