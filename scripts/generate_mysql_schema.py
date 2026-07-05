from pathlib import Path
import sys

from sqlalchemy.dialects import mysql
from sqlalchemy.schema import CreateIndex, CreateTable

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app import create_app
from app.extensions import db
from config import TestingConfig


OUTPUT_DIR = Path("sql")


def main():
    app = create_app(TestingConfig)
    dialect = mysql.dialect()

    database_sql = """-- CareConnect V2 MySQL database bootstrap
-- This creates the local development database.
-- The app is configured to use MySQL root/root on this PC.

CREATE DATABASE IF NOT EXISTS `careconnect_v2`
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;
"""

    with app.app_context():
        metadata = db.metadata
        schema_lines = [
            "-- CareConnect V2 MySQL schema",
            "-- Generated from SQLAlchemy models. Keep this in sync with migrations.",
            "",
            "SET NAMES utf8mb4;",
            "USE `careconnect_v2`;",
            "SET FOREIGN_KEY_CHECKS = 0;",
            "",
        ]

        for table in reversed(metadata.sorted_tables):
            schema_lines.append(f"DROP TABLE IF EXISTS `{table.name}`;")

        schema_lines.extend(["", "SET FOREIGN_KEY_CHECKS = 1;", ""])

        for table in metadata.sorted_tables:
            schema_lines.append(str(CreateTable(table).compile(dialect=dialect)).rstrip() + ";")
            schema_lines.append("")

        for table in metadata.sorted_tables:
            for index in table.indexes:
                schema_lines.append(str(CreateIndex(index).compile(dialect=dialect)).rstrip() + ";")

    OUTPUT_DIR.mkdir(exist_ok=True)
    (OUTPUT_DIR / "00_create_database.sql").write_text(database_sql, encoding="utf-8")
    (OUTPUT_DIR / "01_schema.sql").write_text("\n".join(schema_lines) + "\n", encoding="utf-8")
    print("Generated sql/00_create_database.sql and sql/01_schema.sql")


if __name__ == "__main__":
    main()
