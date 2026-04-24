# BookHaven Render Deployment TODO
Status: Fixing database URL parsing bug causing "Name or service not known"

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

## Completed Fix:
14. [x] **Fix db.py URL parsing bug**
    - Root cause: string-slice logic for `@` encoding stripped `aws-1-ap-southeast-1.` from hostname
    - Fix: used `urllib.parse` for robust URL encoding (preserves full hostname, encodes only password)
    - Added startup connection validation and better `create_engine` settings
    - Added clearer user-facing error messages in `app.py`

## Remaining:
15. [ ] Commit & push fix to GitHub
16. [ ] Verify Render auto-deploy
17. [ ] Re-test placing an order on live site
18. [ ] Run `python migrate.py` in Render Shell if needed

