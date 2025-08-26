🍽️ **NutriPlate**

Scan your plate. Know your nutrition. Instantly.

NutriPlate is a food detection and nutrition analysis app powered by computer vision + AI models.
Upload or scan your meal, and NutriPlate will:
✅ Detect the food items
✅ Classify them (e.g., strawberry, rice, chicken)
✅ Estimate freshness
✅ Provide nutritional insights (calories, protein, carbs, fats)

🚀 **Features**

📷 Food Detection – Identify multiple items from an image of your plate
🧠 Classification – Deep learning models for food recognition
🍏 Nutrition Estimation – Macro breakdown: calories, proteins, carbs, fats
🌱 Freshness Check – Estimate how fresh the food looks
💻 Interactive Web UI – Clean card-style dashboard built with HTML/CSS/JS
🔄 API Support – Use /scan endpoint for programmatic access

📂 **Project Structure**
```bash
food_detector/
│── app/                 # Flask app entry
│   └── app.py
│── classification/       # Food classifier
│   └── classifier.py
│── detection/            # Object detection pipeline
│   └── detector.py
│── freshness/            # Freshness estimator
│   └── freshness.py
│── nutrition/            # Nutrition lookup
│   └── nutrition.py
│── training/             # Training scripts (Food-101 dataset)
│   └── train_food101.py
│── models/               # Pretrained models
│── utils/                # Helper functions
│── data/                 # Sample data
│── main.py               # Core orchestrator (detect + classify + nutrition)
│── requirements.txt      # Dependencies
```
⚡**Installation & Setup**

1️⃣ Clone this repo
```bash
git clone https://github.com/yourusername/nutriplate.git
cd nutriplate
```
2️⃣ Create & activate virtual environment
```bash
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows
```
3️⃣ Install dependencies
```bash
pip install -r requirements.txt
```
4️⃣ Run Flask server
```bash
python app/app.py
```
5️⃣ Open browser
```bash
http://127.0.0.1:5000/
```
🎯 **Usage**
Web App
*Click Start Scanning
*Upload a food image
*Get instant nutrition insights

🧠 **Tech Stack**
🎯Backend: Flask, Python
🎯Frontend: HTML5, CSS3, Vanilla JS
🎯AI Models: Food-101 classification, freshness estimation models
🎯Data: Nutrition datasets

🤝 **Contributing**
Contributions are welcome!
1.Fork the repo
2.Create a feature branch (git checkout -b feature-name)
3.Commit changes (git commit -m "Added new feature")
4.Push to branch (git push origin feature-name)
5.Open a Pull Request

📜 **License**
This project is licensed under the MIT License – feel free to use & modify.

👨‍💻 **Author**

Developed by Harini ✨
If you like this project, don’t forget to ⭐ the repo!
