# BookHaven Render Deployment TODO
Status: In Progress

## Approved Plan Steps:
1. [x] Create TODO.md (current)
2. [] Create .gitignore
3. [] Create .env.example (with user DB creds)
4. [] Update requirements.txt (+gunicorn)
5. [] Edit db.py (use os.getenv)
6. [] Edit app.py (production config)
7. [] Create render.yaml
8. [] Test local: pip install -r requirements.txt && python app.py
9. [] git init, add/commit all files
10. [] Create GitHub repo 'BookHaven-Final', push main branch
11. [] User: Link Render dashboard to GitHub repo, set DATABASE_URL env var
12. [] Deploy on Render, verify live site
13. [] Post-deploy: Run migrate.py on Render shell if needed

Next: Step 2-7 (parallel file creates/edits)

