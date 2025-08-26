NutriPlate frontend (static)

How to deploy to Vercel

1. Edit vercel.json and set BACKEND_URL to your deployed backend (e.g., https://your-backend.onrender.com).
2. Push this folder to GitHub and connect the repository in Vercel.
3. In Vercel dashboard, create a new project, select this repo, set the root directory to `frontend`.
4. Deploy; the site will be served as static files. The frontend will POST to `${BACKEND_URL}/scan`.

Notes: The backend must accept CORS from the frontend origin. The backend should be hosted on a Python-friendly host (Render, Fly, Railway) and expose a public URL.
