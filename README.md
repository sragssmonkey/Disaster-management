# Disaster-management

**Disaster Management Geoportal (Django + Cesium)**

An India-centric disaster-management geoportal.

**Stack:**

* Django (backend & APIs)
* HTML/CSS/JS + Cesium (frontend)
* scikit-learn / LightGBM (ML)
* PostgreSQL / PostGIS (later)

---

## Branches Used

* **main** → stable, deployable
* **Frontend** → UI work (templates/static/JS)
* **Backend** → APIs, models, business logic
* **ML-model** → ML training/inference
* **Database** → DB/PostGIS, migrations (optional)

> **Rule:** Don’t push to `main` directly. Always use Pull Requests (PRs).

---

## Prerequisites

* Git
* Python 3.10+ (works with 3.13 too)

---

## 🚀 Quick Start (Local Setup)

### 1. Clone the repo

```bash
git clone https://github.com/sragssmonkey/Disaster-management.git
cd Disaster-management
```

### 2. Pick your working branch

* **Frontend (Sragvi, Avinash, Darshan, Anugrah):**

  ```bash
  git checkout Frontend
  ```
* **Backend (Sragvi):**

  ```bash
  git checkout Backend
  ```
* **Machine Learning (Yash, Anugrah):**

  ```bash
  git checkout ML-model
  ```
* **Database (Anugrah):**

  ```bash
  git checkout Database
  ```

---

## 💻 Workflow

### To Commit Changes

```bash
git status
git add <files-or-folders>   # or: git add .
git commit -m "feat(frontend): add Cesium globe on landing page"
```

### Commit Style (Recommended)

* `feat:` → new feature
* `fix:` → bug fix
* `docs:` → docs/README changes
* `chore:` → non-code/infra
* `refactor:` → internal code changes

### Push Your Branch

```bash
git push -u origin <YourBranch>
```

---

## 📥 Downloads Needed

* [Python](https://www.python.org/downloads/)
* [Django](https://www.djangoproject.com/)
* [VS Code](https://code.visualstudio.com/)

---

## ⚙️ Local Development Setup

### 1. Create Virtual Environment & Install Dependencies

**Windows (PowerShell):**

```powershell
py -m venv venv
venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

**macOS/Linux:**

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

👉 If `requirements.txt` is empty, install basics and then freeze:

```bash
pip install django djangorestframework
pip freeze > requirements.txt
```

---

### 2. Configure Environment (Dev)

Create `.env` file (if used in settings) and add:

```ini
DJANGO_DEBUG=1
DJANGO_SECRET_KEY=change-me
DATABASE_URL=sqlite:///db.sqlite3
```

---

### 3. Run the Project

```bash
python manage.py migrate
python manage.py runserver
```

---



