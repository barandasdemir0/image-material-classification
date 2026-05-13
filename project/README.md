# AI Waste Classification

Project scaffold: simple frontend and Flask backend for classifying material images (Glass, Metal, Paper, Plastic).

Project structure:

project/
├── web/                # Frontend (static)
│   ├── index.html
│   ├── style.css
│   ├── script.js
│   └── assets/
│       ├── images/
│       └── icons/
├── api/                # Flask backend
│   ├── app.py
│   ├── requirements.txt
│   ├── uploads/
│   ├── static/
│   ├── model/
│   │   └── model.h5  (placeholder)
│   └── utils/
│       └── predictor.py
└── README.md

Quick start (backend):

1. Create and activate a Python virtual environment.

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Install dependencies

```powershell
pip install -r project\api\requirements.txt
```

3. Run the API

```powershell
python project\api\app.py
```

The API will run on `http://127.0.0.1:5000` and expose POST `/predict`.

Quick start (frontend):

- Open `project/web/index.html` in your browser (for local testing) or serve via a static server.
- Click or drag an image into the upload area and press `Run AI Scan`.

Notes:
- Replace `project/api/model/model.h5` with your trained Keras model for real predictions.
- `predictor.py` will fallback to a deterministic fake prediction if a model is not found.
- The frontend uses Fetch API to POST the image to `http://127.0.0.1:5000/predict`.

Would you like me to run the backend in the integrated terminal or update the UI further? 
