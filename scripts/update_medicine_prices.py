from decimal import Decimal
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app import create_app
from app.extensions import db
from app.models import Medicine, MedicineCategory
from app.services.medicine_excel import load_master_medicines


def truthy(value):
    return str(value).strip().lower() in {"yes", "true", "1"}


def main():
    app = create_app()
    rows = load_master_medicines()
    with app.app_context():
        categories = {category.name: category for category in MedicineCategory.query.all()}
        for row in rows:
            category_name = row["Category"]
            if category_name not in categories:
                categories[category_name] = MedicineCategory(name=category_name)
                db.session.add(categories[category_name])
        db.session.flush()

        updated = 0
        inserted = 0
        seen_names = set()
        for row in rows:
            name = row["Medicine Name"]
            if name in seen_names:
                continue
            seen_names.add(name)
            medicines = Medicine.query.filter_by(name=name).all()
            if not medicines:
                medicines = [Medicine(name=name)]
                db.session.add(medicines[0])
                inserted += 1
            else:
                updated += len(medicines)

            for medicine in medicines:
                medicine.category_id = categories[row["Category"]].id
                medicine.generic_name = row["Generic Name"]
                medicine.brand = row["Brand"]
                medicine.strength = row["Strength"]
                medicine.form = row["Form"]
                medicine.pack_size = row["Pack Size"]
                medicine.manufacturer = row["Manufacturer"]
                medicine.unit_price = Decimal(str(row["Price"]))
                medicine.requires_prescription = truthy(row["Prescription Required"])
                medicine.stock_remaining = int(row["Available Stock"])
                medicine.minimum_stock = int(row["Minimum Stock"])
                medicine.barcode = str(row["Barcode"])
                medicine.expiry_placeholder = row["Expiry Placeholder"]

        db.session.commit()
        print(f"Updated {updated} medicines and inserted {inserted} missing medicines")


if __name__ == "__main__":
    main()
