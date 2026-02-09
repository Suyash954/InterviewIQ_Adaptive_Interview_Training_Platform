## InterviewIQ – Adaptive Interview Training Platform

Lightweight Django app to practice interview questions, organized by skill and difficulty.

### 1. Requirements

- Python 3.11+ (3.13 works fine)
- pip

### 2. Setup (first time)

From the project root (`InterviewIQ – Adaptive Interview Training Platform`):

```bash
python -m pip install -r requirements.txt
python manage.py migrate
```

Optional (recommended):

```bash
python manage.py createsuperuser
```

Seed some example data:

```bash
python manage.py seed_data
```

### 3. Run the development server

```bash
python manage.py runserver
```

Then open `http://127.0.0.1:8000/` in your browser.

### 4. Admin & data

- Admin panel: `http://127.0.0.1:8000/admin/`
- Models:
  - `Skill` – e.g., "Data Structures", "System Design"
  - `Question` – the actual interview question text, linked to a skill and difficulty
  - `Attempt` – a user’s attempt and score for a given question

You can manage all of these from the Django admin; the home page automatically lists questions for practice.

