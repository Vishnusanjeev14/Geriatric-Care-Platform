from datetime import datetime

from app.extensions import db


class TimestampMixin:
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )


class BaseModel(db.Model, TimestampMixin):
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)


class Account(BaseModel):
    __tablename__ = "accounts"

    full_name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(180), nullable=False, unique=True, index=True)
    phone = db.Column(db.String(30))
    password_hash = db.Column(db.String(255), nullable=False)
    account_type = db.Column(db.String(40), nullable=False, default="family", index=True)
    status = db.Column(db.String(40), nullable=False, default="active", index=True)
    preferred_language = db.Column(db.String(8), nullable=False, default="en")
    last_login_at = db.Column(db.DateTime)

    permissions = db.relationship("AccountProfilePermission", back_populates="account")


class Profile(BaseModel):
    __tablename__ = "profiles"

    display_name = db.Column(db.String(120), nullable=False, index=True)
    relationship_label = db.Column(db.String(80), nullable=False, default="Family")
    date_of_birth = db.Column(db.Date, nullable=False)
    gender = db.Column(db.String(40))
    photo_initials = db.Column(db.String(4), nullable=False, default="CC")
    blood_group = db.Column(db.String(5))
    health_status = db.Column(db.String(40), nullable=False, default="stable")
    primary_hospital = db.Column(db.String(160))
    primary_care_note = db.Column(db.Text)
    status = db.Column(db.String(40), nullable=False, default="active")

    addresses = db.relationship("ProfileAddress", back_populates="profile", cascade="all, delete-orphan")
    permissions = db.relationship("AccountProfilePermission", back_populates="profile")
    timeline_events = db.relationship("TimelineEvent", back_populates="profile", order_by="TimelineEvent.created_at.desc()")

    @property
    def age(self):
        today = datetime.utcnow().date()
        return today.year - self.date_of_birth.year - (
            (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day)
        )


class AccountProfilePermission(BaseModel):
    __tablename__ = "account_profile_permissions"
    __table_args__ = (db.UniqueConstraint("account_id", "profile_id", name="uq_account_profile"),)

    account_id = db.Column(db.Integer, db.ForeignKey("accounts.id"), nullable=False, index=True)
    profile_id = db.Column(db.Integer, db.ForeignKey("profiles.id"), nullable=False, index=True)
    role = db.Column(db.String(40), nullable=False, default="owner")
    accepted_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    account = db.relationship("Account", back_populates="permissions")
    profile = db.relationship("Profile", back_populates="permissions")


class ProfileAddress(BaseModel):
    __tablename__ = "profile_addresses"

    profile_id = db.Column(db.Integer, db.ForeignKey("profiles.id"), nullable=False, index=True)
    label = db.Column(db.String(80), nullable=False, default="Home")
    line1 = db.Column(db.String(180), nullable=False)
    city = db.Column(db.String(80), nullable=False)
    state = db.Column(db.String(80), nullable=False)
    postal_code = db.Column(db.String(20), nullable=False)
    is_default = db.Column(db.Boolean, nullable=False, default=False)

    profile = db.relationship("Profile", back_populates="addresses")


class EmergencyContact(BaseModel):
    __tablename__ = "emergency_contacts"

    profile_id = db.Column(db.Integer, db.ForeignKey("profiles.id"), nullable=False, index=True)
    name = db.Column(db.String(120), nullable=False)
    relationship = db.Column(db.String(80), nullable=False)
    phone = db.Column(db.String(30), nullable=False)
    priority = db.Column(db.Integer, nullable=False, default=1)


class MedicalCondition(BaseModel):
    __tablename__ = "medical_conditions"

    profile_id = db.Column(db.Integer, db.ForeignKey("profiles.id"), nullable=False, index=True)
    name = db.Column(db.String(120), nullable=False)
    severity = db.Column(db.String(40), nullable=False, default="monitoring")


class MedicineCategory(BaseModel):
    __tablename__ = "medicine_categories"

    name = db.Column(db.String(100), nullable=False, unique=True)


class Medicine(BaseModel):
    __tablename__ = "medicines"

    category_id = db.Column(db.Integer, db.ForeignKey("medicine_categories.id"), nullable=False, index=True)
    name = db.Column(db.String(160), nullable=False, index=True)
    generic_name = db.Column(db.String(160))
    strength = db.Column(db.String(80), nullable=False)
    form = db.Column(db.String(60), nullable=False)
    brand = db.Column(db.String(120))
    pack_size = db.Column(db.String(80), nullable=False, default="10 tablets")
    manufacturer = db.Column(db.String(120), nullable=False)
    unit_price = db.Column(db.Numeric(10, 2), nullable=False)
    requires_prescription = db.Column(db.Boolean, nullable=False, default=False)
    stock_remaining = db.Column(db.Integer, nullable=False, default=100)
    minimum_stock = db.Column(db.Integer, nullable=False, default=20)
    barcode = db.Column(db.String(80))
    expiry_placeholder = db.Column(db.String(20))

    category = db.relationship("MedicineCategory")


class MedicineSchedule(BaseModel):
    __tablename__ = "medicine_schedules"

    profile_id = db.Column(db.Integer, db.ForeignKey("profiles.id"), nullable=False, index=True)
    medicine_id = db.Column(db.Integer, db.ForeignKey("medicines.id"), nullable=False)
    dosage_text = db.Column(db.String(160), nullable=False)
    timing_text = db.Column(db.String(160), nullable=False)
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    forever_medication = db.Column(db.Boolean, nullable=False, default=True)
    times_per_day = db.Column(db.Integer, nullable=False, default=1)
    dose_morning = db.Column(db.Boolean, nullable=False, default=False)
    dose_afternoon = db.Column(db.Boolean, nullable=False, default=False)
    dose_evening = db.Column(db.Boolean, nullable=False, default=False)
    dose_night = db.Column(db.Boolean, nullable=False, default=False)
    food_timing = db.Column(db.String(40), nullable=False, default="After Food")
    quantity_per_dose = db.Column(db.String(40), nullable=False, default="1")
    unit = db.Column(db.String(40), nullable=False, default="Tablet")
    repeat_pattern = db.Column(db.String(40), nullable=False, default="Daily")
    repeat_days = db.Column(db.String(80))
    notes = db.Column(db.Text)
    adherence_percent = db.Column(db.Integer, nullable=False, default=100)
    status = db.Column(db.String(40), nullable=False, default="active")

    medicine = db.relationship("Medicine")


class MedicineAdherence(BaseModel):
    __tablename__ = "medicine_adherence"

    schedule_id = db.Column(db.Integer, db.ForeignKey("medicine_schedules.id"), nullable=False, index=True)
    profile_id = db.Column(db.Integer, db.ForeignKey("profiles.id"), nullable=False, index=True)
    dose_date = db.Column(db.Date, nullable=False, index=True)
    dose_period = db.Column(db.String(40), nullable=False)
    dose_time = db.Column(db.String(20), nullable=False)
    status = db.Column(db.String(40), nullable=False, default="due")
    confirmed_by_account_id = db.Column(db.Integer, db.ForeignKey("accounts.id"))
    notes = db.Column(db.Text)

    schedule = db.relationship("MedicineSchedule")
    confirmed_by = db.relationship("Account")


class MedicineOrder(BaseModel):
    __tablename__ = "medicine_orders"

    profile_id = db.Column(db.Integer, db.ForeignKey("profiles.id"), nullable=False, index=True)
    ordered_by_account_id = db.Column(db.Integer, db.ForeignKey("accounts.id"), nullable=False)
    status = db.Column(db.String(40), nullable=False, default="confirmed", index=True)
    total_amount = db.Column(db.Numeric(10, 2), nullable=False, default=0)
    delivery_address = db.Column(db.String(255), nullable=False)

    items = db.relationship("MedicineOrderItem", back_populates="order", cascade="all, delete-orphan")


class MedicineOrderItem(BaseModel):
    __tablename__ = "medicine_order_items"

    order_id = db.Column(db.Integer, db.ForeignKey("medicine_orders.id"), nullable=False, index=True)
    medicine_id = db.Column(db.Integer, db.ForeignKey("medicines.id"), nullable=False)
    medicine_name_snapshot = db.Column(db.String(160), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    unit_price_snapshot = db.Column(db.Numeric(10, 2), nullable=False)
    line_total = db.Column(db.Numeric(10, 2), nullable=False)

    order = db.relationship("MedicineOrder", back_populates="items")
    medicine = db.relationship("Medicine")


class Prescription(BaseModel):
    __tablename__ = "prescriptions"

    profile_id = db.Column(db.Integer, db.ForeignKey("profiles.id"), nullable=False, index=True)
    uploaded_by_account_id = db.Column(db.Integer, db.ForeignKey("accounts.id"), nullable=False)
    original_filename = db.Column(db.String(180), nullable=False)
    extracted_text = db.Column(db.Text)
    status = db.Column(db.String(40), nullable=False, default="uploaded", index=True)


class Hospital(BaseModel):
    __tablename__ = "hospitals"

    name = db.Column(db.String(160), nullable=False)
    branch_type = db.Column(db.String(40), nullable=False, default="hospital")
    address = db.Column(db.String(255))
    city = db.Column(db.String(80), nullable=False)
    distance_km = db.Column(db.Numeric(5, 1), nullable=False)
    rating = db.Column(db.Numeric(3, 1), nullable=False)
    departments = db.Column(db.String(255), nullable=False)
    latitude = db.Column(db.Numeric(10, 6))
    longitude = db.Column(db.Numeric(10, 6))
    phone = db.Column(db.String(40))
    emergency_available = db.Column(db.Boolean, nullable=False, default=False)
    working_hours = db.Column(db.String(120))


class Appointment(BaseModel):
    __tablename__ = "appointments"

    profile_id = db.Column(db.Integer, db.ForeignKey("profiles.id"), nullable=False, index=True)
    booked_by_account_id = db.Column(db.Integer, db.ForeignKey("accounts.id"), nullable=False)
    hospital_id = db.Column(db.Integer, db.ForeignKey("hospitals.id"), nullable=False)
    appointment_date = db.Column(db.Date, nullable=False)
    appointment_time = db.Column(db.String(20), nullable=False)
    reason = db.Column(db.String(180), nullable=False)
    status = db.Column(db.String(40), nullable=False, default="requested", index=True)

    hospital = db.relationship("Hospital")


class Caretaker(BaseModel):
    __tablename__ = "caretakers"

    account_id = db.Column(db.Integer, db.ForeignKey("accounts.id"), nullable=False, unique=True)
    specialties = db.Column(db.String(180), nullable=False)
    languages = db.Column(db.String(120), nullable=False)
    rating = db.Column(db.Numeric(3, 1), nullable=False, default=4.8)
    available = db.Column(db.Boolean, nullable=False, default=True)
    experience_years = db.Column(db.Integer, nullable=False, default=6)
    verified = db.Column(db.Boolean, nullable=False, default=True)

    account = db.relationship("Account")


class CareRequest(BaseModel):
    __tablename__ = "care_requests"

    profile_id = db.Column(db.Integer, db.ForeignKey("profiles.id"), nullable=False, index=True)
    requested_by_account_id = db.Column(db.Integer, db.ForeignKey("accounts.id"), nullable=False)
    caretaker_id = db.Column(db.Integer, db.ForeignKey("caretakers.id"))
    care_type = db.Column(db.String(60), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    visit_time = db.Column(db.String(20), nullable=False, default="09:00")
    duration = db.Column(db.String(80), nullable=False)
    language = db.Column(db.String(80))
    gender_preference = db.Column(db.String(40))
    recurring = db.Column(db.Boolean, nullable=False, default=False)
    emergency_request = db.Column(db.Boolean, nullable=False, default=False)
    notes = db.Column(db.Text)
    status = db.Column(db.String(40), nullable=False, default="requested", index=True)
    visit_note = db.Column(db.Text)

    caretaker = db.relationship("Caretaker")
    profile = db.relationship("Profile")


class HomeServiceBooking(BaseModel):
    __tablename__ = "home_service_bookings"

    profile_id = db.Column(db.Integer, db.ForeignKey("profiles.id"), nullable=False, index=True)
    booked_by_account_id = db.Column(db.Integer, db.ForeignKey("accounts.id"), nullable=False)
    service_type = db.Column(db.String(80), nullable=False)
    scheduled_date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(40), nullable=False, default="requested", index=True)
    notes = db.Column(db.Text)


class InventoryItem(BaseModel):
    __tablename__ = "inventory_items"

    medicine_id = db.Column(db.Integer, db.ForeignKey("medicines.id"), nullable=False, index=True)
    branch_name = db.Column(db.String(160), nullable=False)
    quantity_on_hand = db.Column(db.Integer, nullable=False, default=0)
    reorder_level = db.Column(db.Integer, nullable=False, default=20)
    status = db.Column(db.String(40), nullable=False, default="healthy")

    medicine = db.relationship("Medicine")


class Notification(BaseModel):
    __tablename__ = "notifications"

    account_id = db.Column(db.Integer, db.ForeignKey("accounts.id"), nullable=False, index=True)
    profile_id = db.Column(db.Integer, db.ForeignKey("profiles.id"), index=True)
    category = db.Column(db.String(60), nullable=False, default="system")
    priority = db.Column(db.String(40), nullable=False, default="normal")
    title = db.Column(db.String(160), nullable=False)
    message = db.Column(db.Text, nullable=False)
    read_at = db.Column(db.DateTime)


class TimelineEvent(BaseModel):
    __tablename__ = "timeline_events"

    profile_id = db.Column(db.Integer, db.ForeignKey("profiles.id"), nullable=False, index=True)
    actor_account_id = db.Column(db.Integer, db.ForeignKey("accounts.id"))
    event_type = db.Column(db.String(80), nullable=False, index=True)
    title = db.Column(db.String(160), nullable=False)
    description = db.Column(db.Text, nullable=False)
    source_module = db.Column(db.String(80), nullable=False)
    priority = db.Column(db.String(40), nullable=False, default="normal")

    profile = db.relationship("Profile", back_populates="timeline_events")

