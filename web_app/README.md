Quick guide — project/api

Purpose: this folder contains both the serving code (API + web demo) and development helpers
for dataset preparation, training and result analysis. Files have been organized for clarity
into small, focused folders to keep the top-level tidy while preserving full functionality.

Layout now
- `app.py` — web API server (Flask/FastAPI). Keep this for running the service.
- `utils/` — shared helpers (e.g. `predictor.py`).
- `model/` — trained model artifacts (ignored by git).
- `static/`, `uploads/` — web static files and runtime uploads.
- `train/` — training and dataset scripts (e.g. `train_transfer.py`, `fine_tune_resnet.py`).
- `tools/` — analysis & debug utilities (e.g. `analyze_results.py`, `visualize_misclassified.py`).
- `demo/` — demos (e.g. `streamlit_app.py`).

Quick usage notes
- Run the API: `python app.py` (ensure `requirements.txt` installed).
- Run Streamlit demo (from `project/api`):
	```powershell
	cd project/api
	streamlit run demo/streamlit_app.py
	```
- Run training scripts (from `project/api`):
	```powershell
	cd project/api
	python train/train_transfer.py
	```

Notes
- Model weights remain in `model/` and are ignored by `.gitignore` to avoid large files in git.
- If you move files again, search for `os.path` or `Path(__file__)` usages and update parent
	references accordingly — the moved scripts already include updated relative-path logic.

If you'd like, I can next:
- Create a small `deploy/` snapshot containing only `app.py`, `utils/`, `requirements.txt`, and a
	slim `README` for running locally, or
- Add small convenience scripts to run the common commands above.
 
Sync helper
- `sync_model.py`: small helper that copies `model_finetuned.h5` or `model.h5` into the canonical
	serving filename `project/api/model/model.h5`. Use when you trained the model somewhere else and
	want to quickly make it available to the API:

	```powershell
	python project/api/sync_model.py --src C:\path\to\latest_model.h5
	# or simply:
	python project/api/sync_model.py
	```
	The latter will prefer `model_finetuned.h5` if present, otherwise `model.h5` in the same folder.