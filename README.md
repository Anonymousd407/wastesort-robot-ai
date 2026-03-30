# ♻️ WasteSort AI - Smart Waste Sorting & Analysis

Welcome to **WasteSort AI**, an intelligent platform to automate waste sorting and provide impact analysis using AI-powered image detection.  

---

## 🚀 Features

- 🖼️ Upload images of waste (plastic, paper, metal, organic, etc.)  
- 🤖 AI-based object detection with **YOLOv11 model**  
- ⏳ Estimate approximate age of waste  
- ⚠️ Hazard check for dangerous materials  
- ♻️ Suggest proper recycling methods  
- 🛠️ Provide actionable solutions for handling waste  

---

## 🖼️ How It Works

1. Upload one or multiple images via the frontend panel.  
2. Images are sent to the **FastAPI backend**.  
3. WasteSort AI analyzes images using **Oxlo AI detection API**.  
4. Results returned:  
   - **Type of waste**  
   - **Estimated age**  
   - **Hazard check**  
   - **Recommended recycling method**  
   - **Handling solution**  
5. Frontend displays results with a **clean, interactive UI**.  

---

## 🛠️ Tech Stack

- **Frontend:** HTML, CSS, JavaScript  
- **Backend:** Python, FastAPI, Pillow  
- **AI Model:** YOLOv11 via Oxlo AI API  
- **Deployment:** Localhost (dev) / Cloud-ready  

---

## ⚙️ Installation

```bash
# Clone the repo
git clone https://github.com/Anonymousd407/wastesort-robot-ai.git
cd wastesort-robot-ai

# Setup Python virtual environment
python3 -m venv venv
source venv/bin/activate  # Linux / macOS
# venv\Scripts\activate    # Windows

# Install dependencies
pip install -r backend/requirements.txt

# Create .env file in backend/
echo "OXLO_API_KEY=your_oxlo_api_key_here" > backend/.env

# Run backend server
uvicorn backend.main:app --reload --host 127.0.0.1 --port 8000

# Open frontend/index.html in browser

📝 Usage
Open the frontend in your browser.
Upload images.
Click Analyze.
View Analysis Results panel:
Image #1: Plastic Bottle
Estimated Age: 2 years
Hazard Check: No hazard
Recommended Recycling Method: Clean and recycle
Solution: Dispose at nearest recycling facility
🏗️ Project Structure
wastesort-ai/
├─ backend/             # FastAPI backend
│  ├─ main.py           # API server
│  └─ venv/             # Python virtual environment
├─ frontend/            # Frontend UI
│  └─ index.html
└─ README.md            # This file
🌟 Contributing

Contributions welcome: features, bug fixes, UI improvements.
Create a pull request and describe your changes clearly.

📜 License

MIT License © 2026
