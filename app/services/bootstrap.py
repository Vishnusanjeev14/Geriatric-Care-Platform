from datetime import date, timedelta
from decimal import Decimal

from werkzeug.security import generate_password_hash

from app.extensions import db
from app.models import (
    Account,
    AccountProfilePermission,
    Appointment,
    CareRequest,
    Caretaker,
    EmergencyContact,
    HomeServiceBooking,
    Hospital,
    InventoryItem,
    MedicalCondition,
    Medicine,
    MedicineCategory,
    MedicineSchedule,
    Notification,
    Profile,
    ProfileAddress,
    TimelineEvent,
)
from app.services.medicine_excel import load_master_medicines


DEMO_PASSWORD = "CareConnect@123"


def bootstrap_demo_data():
    db.create_all()
    if Account.query.first():
        return

    family = Account(
        full_name="Emma Wilson",
        email="family@careconnect.test",
        phone="+1 415 555 0142",
        password_hash=generate_password_hash(DEMO_PASSWORD),
        account_type="family",
    )
    healthcare = Account(
        full_name="Northstar Health Operations",
        email="healthcare@careconnect.test",
        password_hash=generate_password_hash(DEMO_PASSWORD),
        account_type="healthcare",
    )
    caretaker_account = Account(
        full_name="Sophia Brown",
        email="caretaker@careconnect.test",
        phone="+1 415 555 0198",
        password_hash=generate_password_hash(DEMO_PASSWORD),
        account_type="caretaker",
    )
    db.session.add_all([family, healthcare, caretaker_account])
    db.session.flush()

    profiles = [
        Profile(
            display_name="William Wilson",
            relationship_label="Father",
            date_of_birth=date(1944, 9, 18),
            gender="male",
            photo_initials="WW",
            blood_group="A+",
            health_status="attention",
            primary_hospital="Northstar Medical Center",
            primary_care_note="Monitor blood pressure and evening medication adherence.",
        ),
        Profile(
            display_name="Oliver Carter",
            relationship_label="Uncle",
            date_of_birth=date(1951, 5, 7),
            gender="male",
            photo_initials="OC",
            blood_group="O-",
            health_status="stable",
            primary_hospital="Lakeside Clinic",
            primary_care_note="Mobility support twice a week.",
        ),
        Profile(
            display_name="Emma Wilson",
            relationship_label="Myself",
            date_of_birth=date(1988, 11, 22),
            gender="female",
            photo_initials="EW",
            blood_group="B+",
            health_status="stable",
            primary_hospital="Northstar Medical Center",
        ),
    ]
    db.session.add_all(profiles)
    db.session.flush()

    addresses = [
        ("Home", "24 Maple Avenue", "San Francisco", "California", "94110"),
        ("Assisted Living", "880 Harbor View Lane", "San Francisco", "California", "94107"),
        ("Home", "24 Maple Avenue", "San Francisco", "California", "94110"),
    ]
    for profile, address in zip(profiles, addresses):
        db.session.add(AccountProfilePermission(account_id=family.id, profile_id=profile.id, role="owner"))
        db.session.add(
            ProfileAddress(
                profile_id=profile.id,
                label=address[0],
                line1=address[1],
                city=address[2],
                state=address[3],
                postal_code=address[4],
                is_default=True,
            )
        )

    db.session.add_all(
        [
            EmergencyContact(profile_id=profiles[0].id, name="Emma Wilson", relationship="Daughter", phone="+1 415 555 0142"),
            EmergencyContact(profile_id=profiles[1].id, name="Charlotte Green", relationship="Sister", phone="+1 415 555 0171"),
            EmergencyContact(profile_id=profiles[2].id, name="Daniel Smith", relationship="Partner", phone="+1 415 555 0166"),
            MedicalCondition(profile_id=profiles[0].id, name="Hypertension", severity="active"),
            MedicalCondition(profile_id=profiles[0].id, name="Type 2 Diabetes", severity="monitoring"),
            MedicalCondition(profile_id=profiles[1].id, name="Post-surgery mobility support", severity="monitoring"),
        ]
    )

    categories = {}
    medicines = []
    for row in load_master_medicines()[:1200]:
        category_name = row["Category"]
        if category_name not in categories:
            categories[category_name] = MedicineCategory(name=category_name)
            db.session.add(categories[category_name])
    db.session.flush()

    for row in load_master_medicines()[:1200]:
        medicine = Medicine(
            category_id=categories[row["Category"]].id,
            name=row["Medicine Name"],
            generic_name=row["Generic Name"],
            brand=row["Brand"],
            strength=row["Strength"],
            form=row["Form"],
            pack_size=row["Pack Size"],
            manufacturer=row["Manufacturer"],
            unit_price=Decimal(str(row["Price"])),
            requires_prescription=row["Prescription Required"] == "Yes",
            stock_remaining=int(row["Available Stock"]),
            minimum_stock=int(row["Minimum Stock"]),
            barcode=str(row["Barcode"]),
            expiry_placeholder=row["Expiry Placeholder"],
        )
        db.session.add(medicine)
        medicines.append(medicine)
    db.session.flush()

    med_lookup = {medicine.name: medicine for medicine in medicines}
    william_meds = [
        next(m for m in medicines if m.name.startswith("Metformin")),
        next(m for m in medicines if m.name.startswith("Amlodipine")),
    ]
    oliver_med = next(m for m in medicines if m.name.startswith("Ibuprofen"))
    db.session.add_all(
        [
            MedicineSchedule(profile_id=profiles[0].id, medicine_id=william_meds[0].id, dosage_text="1 Tablet", timing_text="Morning", start_date=date.today(), forever_medication=True, times_per_day=1, dose_morning=True, food_timing="After Food", quantity_per_dose="1", unit="Tablet", repeat_pattern="Daily", adherence_percent=92),
            MedicineSchedule(profile_id=profiles[0].id, medicine_id=william_meds[1].id, dosage_text="1 Tablet", timing_text="Evening", start_date=date.today(), forever_medication=True, times_per_day=1, dose_evening=True, food_timing="After Food", quantity_per_dose="1", unit="Tablet", repeat_pattern="Daily", adherence_percent=86),
            MedicineSchedule(profile_id=profiles[1].id, medicine_id=oliver_med.id, dosage_text="1 Tablet", timing_text="Morning", start_date=date.today(), forever_medication=False, times_per_day=1, dose_morning=True, food_timing="With Food", quantity_per_dose="1", unit="Tablet", repeat_pattern="Custom schedule", repeat_days="When pain score is above 5", adherence_percent=100),
        ]
    )

    chennai_hospitals = [
        ("Apollo Hospitals Greams Road", "21 Greams Lane, Thousand Lights, Chennai", 13.0632, 80.2514, "Cardiology, Oncology, Emergency", "+91 44 2829 3333", True),
        ("MIOT International", "4/112 Mount Poonamallee Road, Manapakkam, Chennai", 13.0212, 80.1746, "Orthopedics, Cardiology, Emergency", "+91 44 4200 2288", True),
        ("Fortis Malar Hospital", "52 1st Main Road, Adyar, Chennai", 13.0067, 80.2579, "Neurology, Cardiology, Emergency", "+91 44 4289 2222", True),
        ("Gleneagles Global Health City", "Perumbakkam, Chennai", 12.9051, 80.2067, "Transplant, Gastroenterology, Emergency", "+91 44 4477 7000", True),
        ("Sri Ramachandra Medical Centre", "Porur, Chennai", 13.0368, 80.1426, "Multi-specialty, Emergency", "+91 44 4592 8500", True),
        ("Vijaya Hospital", "Vadapalani, Chennai", 13.0501, 80.2121, "Cardiology, General Medicine", "+91 44 2480 2221", True),
        ("Kauvery Hospital Alwarpet", "TTK Road, Alwarpet, Chennai", 13.0358, 80.2551, "Geriatrics, Cardiology, Emergency", "+91 44 4000 6000", True),
        ("SIMS Hospital", "Jawaharlal Nehru Road, Vadapalani, Chennai", 13.0524, 80.2129, "Neurology, Emergency", "+91 44 4921 1455", True),
        ("Billroth Hospitals Shenoy Nagar", "Shenoy Nagar, Chennai", 13.0755, 80.2257, "General Medicine, Emergency", "+91 44 4292 1777", True),
        ("Prashanth Super Speciality Hospital", "Velachery, Chennai", 12.9815, 80.2209, "Women & Child, Emergency", "+91 44 2243 2323", True),
        ("Dr. Mehta's Hospitals", "Chetpet, Chennai", 13.0732, 80.2445, "Pediatrics, General Medicine", "+91 44 4227 1001", True),
        ("MGM Healthcare", "Nelson Manickam Road, Aminjikarai, Chennai", 13.0730, 80.2219, "Heart, Lung, Emergency", "+91 44 4524 2407", True),
        ("Rela Hospital", "Chromepet, Chennai", 12.9527, 80.1420, "Liver, Multi-specialty, Emergency", "+91 44 6666 7788", True),
        ("Sankara Nethralaya", "College Road, Nungambakkam, Chennai", 13.0647, 80.2486, "Ophthalmology", "+91 44 4227 1500", False),
        ("Adyar Cancer Institute", "Sardar Patel Road, Adyar, Chennai", 13.0063, 80.2425, "Oncology", "+91 44 2220 9150", False),
        ("Madras Medical Mission", "Mogappair, Chennai", 13.0836, 80.1842, "Cardiac Sciences, Emergency", "+91 44 2656 5931", True),
        ("Stanley Medical College Hospital", "Old Jail Road, Chennai", 13.1065, 80.2862, "Government Hospital, Emergency", "+91 44 2528 1351", True),
        ("Rajiv Gandhi Government General Hospital", "Park Town, Chennai", 13.0819, 80.2768, "Government Hospital, Emergency", "+91 44 2530 5000", True),
        ("Chettinad Hospital and Research Institute", "Kelambakkam, Chennai", 12.7934, 80.2195, "Multi-specialty, Emergency", "+91 44 4741 1000", True),
    ]
    hospitals = [
        Hospital(
            name=name,
            address=address,
            city="Chennai",
            distance_km=Decimal("0"),
            rating=Decimal("4.5"),
            departments=departments,
            latitude=Decimal(str(lat)),
            longitude=Decimal(str(lon)),
            phone=phone,
            emergency_available=emergency,
            working_hours="24/7 Emergency" if emergency else "Mon-Sat, 9:00 AM - 6:00 PM",
        )
        for name, address, lat, lon, departments, phone, emergency in chennai_hospitals
    ]
    db.session.add_all(hospitals)
    db.session.flush()

    caretaker = Caretaker(account_id=caretaker_account.id, specialties="Medicine assistance, mobility support, daily visits", languages="English, Spanish", rating=Decimal("4.9"), available=True, experience_years=8, verified=True)
    db.session.add(caretaker)
    db.session.flush()

    db.session.add_all(
        [
            Appointment(profile_id=profiles[0].id, booked_by_account_id=family.id, hospital_id=hospitals[0].id, appointment_date=date.today() + timedelta(days=1), appointment_time="10:30", reason="Blood pressure review", status="confirmed"),
            CareRequest(profile_id=profiles[0].id, requested_by_account_id=family.id, caretaker_id=caretaker.id, care_type="Medicine Assistance", start_date=date.today(), visit_time="09:00", duration="4 weeks", language="English", gender_preference="No preference", recurring=True, notes="Confirm morning and evening medicines.", status="accepted", visit_note="Checked BP log and confirmed breakfast medication."),
            CareRequest(profile_id=profiles[2].id, requested_by_account_id=family.id, caretaker_id=caretaker.id, care_type="Daily Visit", start_date=date.today(), visit_time="10:30", duration="1 week", language="English", gender_preference="No preference", notes="Short wellness check after work.", status="accepted", visit_note="Prepared hydration reminder."),
            CareRequest(profile_id=profiles[1].id, requested_by_account_id=family.id, caretaker_id=caretaker.id, care_type="Mobility Support", start_date=date.today(), visit_time="14:00", duration="2 weeks", language="English", gender_preference="No preference", recurring=True, notes="Gentle movement and safety check.", status="accepted", visit_note="Completed hallway walk and stretching routine."),
            HomeServiceBooking(profile_id=profiles[0].id, booked_by_account_id=family.id, service_type="Meal Preparation", scheduled_date=date.today() + timedelta(days=2), status="confirmed", notes="Low-sodium dinner prep."),
            InventoryItem(medicine_id=william_meds[0].id, branch_name="Northstar Pharmacy - Downtown", quantity_on_hand=96, reorder_level=25, status="healthy"),
            InventoryItem(medicine_id=william_meds[1].id, branch_name="Northstar Pharmacy - Downtown", quantity_on_hand=18, reorder_level=25, status="low_stock"),
            InventoryItem(medicine_id=next(m for m in medicines if m.name.startswith("Paracetamol")).id, branch_name="Harborview Pharmacy", quantity_on_hand=210, reorder_level=40, status="healthy"),
            Notification(account_id=family.id, profile_id=profiles[0].id, category="medicines", priority="high", title="Medicine due soon", message="William has Metformin due in 20 minutes."),
            Notification(account_id=family.id, profile_id=profiles[0].id, category="appointments", priority="normal", title="Appointment tomorrow", message="Blood pressure review at Northstar Medical Center."),
            Notification(account_id=family.id, profile_id=profiles[1].id, category="caretaker", priority="normal", title="Caretaker checked in", message="Sophia checked in for Oliver's mobility support."),
        ]
    )

    events = [
        (profiles[0], "Medicine confirmed", "Sophia confirmed William's breakfast Metformin.", "medicines"),
        (profiles[0], "Appointment reminder", "Northstar Medical Center visit is scheduled for tomorrow.", "hospitals"),
        (profiles[0], "Order delivered", "Amlodipine refill was delivered to Maple Avenue.", "pharmacy"),
        (profiles[1], "Caretaker checked in", "Sophia started Oliver's mobility support visit.", "caretaker"),
        (profiles[1], "Visit note added", "Oliver completed a 15-minute walking routine.", "caretaker"),
        (profiles[2], "Wellness check complete", "No pending reminders for Emma today.", "family"),
    ]
    for profile, title, description, module in events:
        db.session.add(
            TimelineEvent(
                profile_id=profile.id,
                actor_account_id=family.id,
                event_type=title.lower().replace(" ", "_"),
                title=title,
                description=description,
                source_module=module,
            )
        )

    db.session.commit()
