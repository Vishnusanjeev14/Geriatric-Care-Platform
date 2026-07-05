# CareConnect V2 MySQL SQL Files

Run these files in order when setting up MySQL manually:

```powershell
mysql -u root -p < sql\00_create_database.sql
mysql -u root -p careconnect_v2 < sql\01_schema.sql
```

Then set this in `.env`:

```text
DATABASE_URL=mysql+pymysql://<mysql-user>:<mysql-password>@localhost:3306/careconnect_v2?charset=utf8mb4
```

After the schema is loaded, start Flask. With `AUTO_BOOTSTRAP_DEMO=true`, the application will insert demo data when the database is empty.
