project/web — frontend

Purpose
- Simple static frontend that uploads an image to the API and shows a prediction.

Run locally
1. Serve files from `project/web` with a simple static server. Example using Python 3:

   ```powershell
   cd project/web
   python -m http.server 8000
   ```

2. Open `http://localhost:8000` in your browser.
3. Ensure the backend is running and reachable at `http://127.0.0.1:5000/predict` (default in `script.js`).

Notes
- For production, build or host these static files in your preferred static hosting (NGINX, S3, GitHub Pages) and configure CORS on the API.
- To change the backend URL, edit `script.js` and update the `fetch` URL. I can make this configurable if you prefer.

Would you like me to make the backend URL configurable or to create a `deploy/` build?"