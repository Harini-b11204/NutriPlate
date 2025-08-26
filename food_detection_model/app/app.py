from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
from flask_cors import CORS
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from main import detect_food, classify_food, estimate_freshness, get_nutrition

from werkzeug.utils import secure_filename
import tempfile
from datetime import datetime

# Flask app and version stamp
app = Flask(__name__)
CORS(app)
CORS(app)  # allow all origins during testing; tighten for production
VERSION = datetime.utcnow().isoformat()

UPLOAD_HTML = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>NutriPlate</title>
    <style>
        *{box-sizing:border-box;margin:0;padding:0}
        body{font-family:Segoe UI, Tahoma, Geneva, Verdana, sans-serif;background:linear-gradient(135deg,#667eea 0%,#764ba2 100%);min-height:100vh;display:flex;align-items:center;justify-content:center;padding:24px}
        .card{width:360px;background:#fff;border-radius:20px;overflow:hidden;box-shadow:0 20px 40px rgba(0,0,0,.12)}
        .card .header{background:linear-gradient(135deg,#4CAF50,#45a049);padding:28px 20px;color:#fff;text-align:center}
        .card .header h1{font-size:20px;margin-bottom:6px}
        .card .header p{font-size:13px;opacity:.95}
        .scan{padding:22px;text-align:center}
        .camera{height:210px;border-radius:12px;border:3px dashed #e6e6e6;display:flex;align-items:center;justify-content:center;flex-direction:column;background:#fafafa;cursor:pointer}
        .camera:hover{border-color:#cfead1;background:#f6fff6}
        .camera .icon{font-size:42px;color:#767676;margin-bottom:10px}
        .camera p{color:#666;font-size:13px}
        .btn{display:inline-block;margin-top:16px;background:#fff;color:#2e7d32;padding:12px 34px;border-radius:28px;border:none;font-weight:700;box-shadow:0 8px 18px rgba(0,0,0,.08);cursor:pointer}
        .btn:active{transform:translateY(1px)}
        .results{padding:18px}
        .ingredient{background:#fbfeff;border-radius:12px;padding:14px;margin-bottom:12px;box-shadow:0 6px 18px rgba(37,78,79,0.03)}
        .ingredient .name{font-weight:700;color:#1f5d3b;margin-bottom:10px}
        .grid{display:grid;grid-template-columns:repeat(4,1fr);gap:8px}
        .tile{background:#fff;padding:8px;border-radius:8px;text-align:center;font-size:12px}
        .tile .val{font-weight:700;color:#2e7d32;margin-bottom:4px}
        .freshness{display:flex;align-items:center;gap:10px;margin-top:10px}
        .bar{flex:1;height:8px;background:#eee;border-radius:6px;overflow:hidden}
        .fill{height:100%;background:#4caf50;width:70%}
        .total{margin-top:12px;background:linear-gradient(135deg,#667eea,#764ba2);color:#fff;padding:16px;border-radius:12px;text-align:center}
        .total .cals{font-size:26px;font-weight:800}
        .footer{padding:12px;text-align:center}
        .scan-another{background:#fff;border-radius:20px;padding:10px 20px;border:none;color:#4CAF50;font-weight:700;cursor:pointer}
        @media(max-width:420px){.card{width:320px}}
    </style>
</head>
<body>
    <div class="card">
        <div class="header">
            <h1>🍽️ NutriPlate</h1>
            <p>Scan your food for instant nutrition analysis</p>
        </div>
        <div class="scan">
            <div class="camera" id="camera" onclick="fileInput.click()">
                <div class="icon">📷</div>
                <p>Tap to scan your plate</p>
                <p style="font-size:11px;color:#9aa">Point camera at your food</p>
            </div>
            <input type="file" id="fileInput" accept="image/*" style="display:none">
            <div><button class="btn" onclick="fileInput.click()">Start Scanning</button></div>
        </div>
        <div class="results" id="results" style="display:none">
            <div id="ingredients"></div>
            <div class="total">
                <div class="cals" id="totalCals">0</div>
                <div style="opacity:.9;font-size:13px">Total Calories</div>
            </div>
        </div>
        <div class="footer" id="footer">
            <div style="font-size:11px;color:#888;margin-bottom:6px">Version: {{ version }}</div>
            <button class="scan-another" onclick="resetScan()" style="display:none">Scan Another Plate</button>
        </div>
    </div>

    <script>
        const fileInput = document.getElementById('fileInput');
        const camera = document.getElementById('camera');
        const results = document.getElementById('results');
        const ingredients = document.getElementById('ingredients');
        const totalCals = document.getElementById('totalCals');
        const footer = document.getElementById('footer');
        const API = 'https://your-backend.onrender.com';

        fileInput.addEventListener('change', async (e)=>{
            const f = e.target.files[0];
            if(!f) return;
            camera.innerHTML = '<div style="padding:40px 10px;color:#4caf50;">Scanning...</div>';
            const fd = new FormData(); fd.append('file', f);
            try{
                        const r = await fetch(`${API}/scan`, { method:'POST', body: fd });
                        console.log('[NET] /scan status', r.status, 'ok=', r.ok);
                        // If server returned non-2xx, read text and show error (avoid reading body twice)
                        if(!r.ok){
                            const txt = await r.text().catch(()=>null);
                            console.warn('[NET] /scan non-ok response', txt);
                            camera.innerHTML = `<div style="padding:20px;color:#c62828;">Server error: ${r.status}</div>`;
                            return;
                        }
                        let j = null;
                        try{
                            j = await r.json();
                            console.log('[NET] /scan json', j);
                        }catch(jsonErr){
                            const txt = await r.text().catch(()=>null);
                            console.warn('[NET] /scan invalid json', txt, jsonErr);
                            camera.innerHTML = '<div style="padding:20px;color:#c62828;">Server returned invalid JSON</div>';
                            return;
                        }
                        render(j.results||[]);
            }catch(err){
                camera.innerHTML = '<div style="padding:40px 10px;color:#c62828;">Upload failed</div>';
                console.error(err);
            }
        });

        function render(items){
            ingredients.innerHTML=''; let total=0;
            items.forEach(it=>{
                const c = (it.nutrition && it.nutrition.calories)||0; total+=Number(c||0);
                const p = (it.nutrition&&it.nutrition.macros&&it.nutrition.macros.protein)||'-';
                const cb = (it.nutrition&&it.nutrition.macros&&it.nutrition.macros.carbs)||'-';
                const f = (it.nutrition&&it.nutrition.macros&&it.nutrition.macros.fat)||'-';
                const div = document.createElement('div'); div.className='ingredient';
                div.innerHTML = `
                    <div class='name'>${it.food}</div>
                    <div class='grid'>
                        <div class='tile'><div class='val'>${c}</div><div class='lbl'>Calories</div></div>
                        <div class='tile'><div class='val'>${p}</div><div class='lbl'>Protein</div></div>
                        <div class='tile'><div class='val'>${cb}</div><div class='lbl'>Carbs</div></div>
                        <div class='tile'><div class='val'>${f}</div><div class='lbl'>Fat</div></div>
                    </div>
                    <div class='freshness'><div style='font-size:13px;color:#666'>Freshness</div><div class='bar'><div class='fill'></div></div><div style='font-weight:700;color:#2e7d32'>${it.freshness}</div></div>
                `;
                ingredients.appendChild(div);
            });
            totalCals.textContent = total;
            results.style.display='block'; footer.querySelector('.scan-another').style.display='inline-block';
            camera.style.display='none';
        }

        function resetScan(){
            results.style.display='none'; ingredients.innerHTML=''; totalCals.textContent=0; camera.style.display='flex'; footer.querySelector('.scan-another').style.display='none';
        }
    </script>
</body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def index():
    results = None
    if request.method == 'POST':
        if 'file' not in request.files:
            results = "No file part"
        else:
            file = request.files['file']
            if file.filename == '':
                results = "No selected file"
            else:
                filename = secure_filename(file.filename)
                with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(filename)[1]) as temp:
                    file.save(temp.name)
                    image_path = temp.name
                detected_items = detect_food(image_path)
                output = []
                for item in detected_items:
                    food_type = classify_food(item['image'])
                    portion = item['portion']
                    freshness = estimate_freshness(item['image'])
                    nutrition = get_nutrition(food_type, portion)
                    # Debug logs for diagnosis
                    print(f"[DEBUG] detected item: {item}")
                    print(f"[DEBUG] classified as: {food_type}")
                    print(f"[DEBUG] portion={portion} freshness={freshness}")
                    print(f"[DEBUG] nutrition lookup: {nutrition}")
                    output.append({
                        "food": food_type,
                        "portion": portion,
                        "freshness": freshness,
                        "nutrition": nutrition
                    })
                os.remove(image_path)
                results = output
    return render_template_string(UPLOAD_HTML, results=results, version=VERSION)

@app.route('/scan', methods=['POST'])
def scan_plate():
    print('[DEBUG] /scan called')
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    filename = secure_filename(file.filename)
    print(f"[DEBUG] /scan received file: {filename}")
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(filename)[1]) as temp:
            file.save(temp.name)
            image_path = temp.name

        detected_items = detect_food(image_path)
        results = []
        for item in detected_items:
            food_type = classify_food(item['image'])
            portion = item['portion']
            freshness = estimate_freshness(item['image'])
            nutrition = get_nutrition(food_type, portion)
            # Debug logs for diagnosis
            print(f"[DEBUG] detected item: {item}")
            print(f"[DEBUG] classified as: {food_type}")
            print(f"[DEBUG] portion={portion} freshness={freshness}")
            print(f"[DEBUG] nutrition lookup: {nutrition}")
            results.append({
                "food": food_type,
                "portion": portion,
                "freshness": freshness,
                "nutrition": nutrition
            })
        print(f"[DEBUG] /scan returning results: {results}")
        os.remove(image_path)
        return jsonify({"results": results})
    except Exception as e:
        import traceback
        tb = traceback.format_exc()
        print('[ERROR] /scan exception:\n', tb)
        # try to cleanup file if exists
        try:
            if 'image_path' in locals() and os.path.exists(image_path):
                os.remove(image_path)
        except Exception:
            pass
        return jsonify({"error": str(e), "trace": tb}), 500


@app.route('/ping', methods=['GET'])
def ping():
    return jsonify({"version": VERSION})


@app.route('/debug-sample', methods=['GET'])
def debug_sample():
    sample = [{
        "food": "Grilled Chicken Breast",
        "portion": "medium",
        "freshness": "fresh",
        "nutrition": {"calories": 165, "macros": {"protein": 31, "carbs": 0, "fat": 3.6}}
    }]
    return jsonify({"results": sample})


@app.route('/debug-top5', methods=['POST'])
def debug_top5():
    """Accepts an uploaded image and returns classifier top-5 predictions for debugging."""
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    filename = secure_filename(file.filename)
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(filename)[1]) as temp:
            file.save(temp.name)
            image_path = temp.name
        # call classifier.get_topk if available
        try:
            from classification.classifier import get_topk
        except Exception:
            return jsonify({"error": "classifier.get_topk not available"}), 500
        top5 = get_topk(image_path, k=5)
        os.remove(image_path)
        return jsonify({"top5": top5})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=False)
