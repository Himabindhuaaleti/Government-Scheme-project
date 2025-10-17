# Government Schemes Assistant


## Setup Guide (Run Locally)

### 1. Clone the repository

```bash
git clone <paste github link in here!>
# move to the directory
cd <dir-name>
```

### 2. Create virtual environment

```bash
# On-Linux terminal##########################
python -m venv venv
source venv/bin/activate   
##############################################
# On Windows:#################################
python -m venv venv
venv\Scripts\activate
#############################################
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Setup Gemini API Key

Create a `.env` file in the root directory:

```ini
GEMINI_API_KEY=your_api_key_here
```
Note: IMP-step!
Get your API key from: https://makersuite.google.com/app/apikey

### 5. Run the app

```bash
streamlit run app.py
```

---

## Sample Schemes Included

- Ayushman Bharat (PM-JAY)
- PM KISAN
- Ujjwala Yojana
- NSAP (Old Age/Widow Pension)
- Post Matric Scholarship for Minorities
- Savitribai Phule Fellowship
- Swachh Bharat Mission – Urban

#### Add more scheme later.
---
