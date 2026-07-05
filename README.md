# CareConnect V2

CareConnect V2 is a fresh Flask application built from the approved architecture package. Version 0.2 is a polished functional MVP focused on modern healthcare SaaS UX, realistic demo data, Excel-backed medicine catalogue data, connected portal workflows, and accessible navigation.

## Version 0.2 Scope

- Authentication, signup, login, logout, session protection
- Redesigned Family Workspace answering "Who needs attention today?"
- Profile dashboards, emergency cards, timeline, editing, and sharing prototype
- Excel-backed pharmacy catalogue with 1,200 demo medicine records
- Shopping cart, profile/address review, simulated ordering, and order history
- Hospital search, appointment booking, OpenStreetMap preview, and live browser lookup
- Prescription OCR mock workflow with manual review and add-to-cart path
- Expanded caretaker requests and care notes
- Home service booking and history
- Healthcare portal with dashboard, branch operations, inventory, and order status management
- Caretaker portal with profile, calendar-style daily schedule, availability, requests, and visit notes
- Browser speech recognition voice assistant with typed fallback
- Large text and high contrast accessibility toggles

## Project Structure

```text
app/
  blueprints/
    errors/
    main/
  models/
  permissions/
  repositories/
  services/
  static/
  templates/
migrations/
tests/
config.py
run.py
```

## Local Setup

1. Create and activate a virtual environment if `.venv` does not already exist.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Copy `.env.example` to `.env` and update values.
4. Run the application:

```bash
flask --app run.py run
```

Or on Windows PowerShell without activating:

```powershell
.\.venv\Scripts\python.exe -m flask --app run.py run
```

Open `http://127.0.0.1:5000`.

## Demo Accounts

All demo accounts use this password:

```text
CareConnect@123
```

```text
family@careconnect.test
healthcare@careconnect.test
caretaker@careconnect.test
```

Demo identities:

```text
Emma Wilson - family account
William Wilson, Oliver Carter, Emma Wilson - managed profiles
Sophia Brown - caretaker account
Northstar Health Operations - healthcare account
```

## Medicine Master Workbook

The pharmacy catalogue is seeded from:

```text
data/medicine_master.xlsx
```

Regenerate it with:

```powershell
.\.venv\Scripts\python.exe scripts\generate_medicine_master.py
```

## Database

The application reads `DATABASE_URL` from the environment. CareConnect V2 is configured for MySQL through the `mysql+pymysql` SQLAlchemy driver.

Use the included SQL files for manual MySQL setup:

```powershell
mysql -u root -p < sql\00_create_database.sql
mysql -u root -p careconnect_v2 < sql\01_schema.sql
```

Set this in `.env`:

```text
DATABASE_URL=mysql+pymysql://<mysql-user>:<mysql-password>@localhost:3306/careconnect_v2?charset=utf8mb4
```

For local prescription OCR, optionally set the Tesseract executable path in `.env`:

```text
TESSERACT_CMD=<optional-full-path-to-tesseract-executable>
```

When `AUTO_BOOTSTRAP_DEMO=true`, the app inserts demo data into an empty database on startup. Automated tests still use an isolated in-memory database.

Regenerate the MySQL schema files after model changes with:

```powershell
.\.venv\Scripts\python.exe scripts\generate_mysql_schema.py
```

## Development Boundary

Version 0.2 prioritizes polished breadth before production depth. Advanced OCR, real fulfillment, payment, public emergency QR access, production notification channels, and full map/provider integrations remain Version 1.0+ work.


