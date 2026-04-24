# BookHaven Render Deployment TODO
Status: Code ready & pushed to GitHub — Render deployment pending

## Completed Steps:
1. [x] Create TODO.md
2. [x] Create .gitignore
3. [x] Create .env.example
4. [x] Update requirements.txt (+gunicorn/dotenv)
5. [x] Edit db.py (env vars, secured)
6. [x] Edit app.py (production config: host/port/debug=False)
7. [x] Create render.yaml
8. [x] Test local: deps installed, app runs on http://127.0.0.1:5000
9. [x] git init, add ., commit "Initial commit"
10. [x] Create GitHub repo & push main branch
11. [x] Clean up order.py duplicate imports
12. [x] Update render.yaml (add SECRET_KEY, DATABASE_URL env config)
13. [x] Create local .env for development

## Remaining (Manual — Must do on Render Dashboard):
14. [ ] **Connect Render to GitHub repo**
    - Go to https://dashboard.render.com/
    - Click "New +" → "Web Service"
    - Connect your GitHub account and select `BookHaven` repo
    - Render will auto-detect `render.yaml`

15. [ ] **Set DATABASE_URL environment variable on Render**
    - In Render dashboard → BookHaven service → Environment
    - Add: `DATABASE_URL` = `postgresql://postgres.bsharmqqbwqcxmmchyeu:@bookhavenproject@aws-1-ap-southeast-1.pooler.supabase.com:5432/postgres`
    - **Note:** The `@` in the password is handled correctly by SQLAlchemy

16. [ ] **Deploy & verify**
    - Click "Manual Deploy" or push a commit to trigger auto-deploy
    - Wait for build to complete (pip install + gunicorn start)
    - Visit the provided `.onrender.com` URL
    - Test: search books, add to cart, checkout

17. [ ] **Seed DB on Render (run once)**
    - In Render dashboard → BookHaven service → Shell
    - Run: `python migrate.py`
    - This creates tables and seeds 100 books

## Post-Deployment Checklist:
- [ ] Homepage loads without errors
- [ ] Book images display
- [ ] Search & category filters work
- [ ] Add to cart works
- [ ] Checkout page loads with cart items
- [ ] Place order saves to Supabase
- [ ] Payment record saves to Supabase

