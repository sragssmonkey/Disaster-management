# Disaster-management
Disaster Management Geoportal (Django + Cesium)<br>

An India-centric disaster-management geoportal.<br>
Stack: Django (backend & APIs), HTML/CSS/JS + Cesium (frontend), scikit-learn/LightGBM (ML), PostgreSQL/PostGIS (later).<br>


**Branches used:**<br>
main → stable, deployable<br>
Frontend → UI work (templates/static/JS)<br>
Backend → APIs, models, business logic<br>
ML-model → ML training/inference<br>
Database → DB/PostGIS, migrations (optional)<br>
Rule: Don’t push to main directly. Always use PRs.<br>

**Prerequisites:**<br>
Git<br>
Python 3.10+ (works with 3.13 too)<br>

**Quick Start (Local Setup)**<br>
1 Clone the repo<br>
git clone https://github.com/<org-or-username>/Disaster-management.git<br>
cd Disaster-management<br>

2 Pick your working branch:<br>
Sragvi Avinash Darshan Anugrah For Frontend:<br>
git checkout Frontend

Sragvi for Backend:<br>
git checkout Backend

Yash Anugrah for Machine learning:<br>
git checkout ML-model

Anugrah for Database:<br>
git checkout Database

**TO COMMIT CHANGES**<br>
git status<br>
git add <files-or-folders>         # or: git add .<br>
git commit -m "feat(frontend): add Cesium globe on landing page"<br>

**Commit style (recommended):**<br>
feat: … new feature<br>
fix: … bug fix<br>
docs: … docs/README<br>
chore: … non-code/infra<br>
refactor: … internal changes<br>

**Push your branch**<br>
git push -u origin <YourBranch>


**DOWNLOADS:**<br>
Django, Python and VSCODE

Create virtual environment & install deps<br>

Windows (PowerShell):<br>

py -m venv venv<br>
venv\Scripts\Activate.ps1<br>
pip install -r requirements.txt


macOS/Linux:<br>

python3 -m venv venv<br>
source venv/bin/activate<br>
pip install -r requirements.txt


If requirements.txt is empty, install basics and then freeze:<br>

pip install django djangorestframework<br>
pip freeze > requirements.txt<br>

Configure environment (dev)<br>

Create .env (if used in settings) and add things like:<br>

DJANGO_DEBUG=1<br>
DJANGO_SECRET_KEY=change-me<br>
DATABASE_URL=sqlite:///db.sqlite3<br>

Run the project<br>
python manage.py migrate<br>
python manage.py runserver<br>




git checkout Database
