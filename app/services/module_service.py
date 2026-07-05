from datetime import datetime
from decimal import Decimal

from app.extensions import db
from app.models import (
    Appointment,
    CareRequest,
    HomeServiceBooking,
    InventoryItem,
    Medicine,
    MedicineOrder,
    MedicineOrderItem,
    MedicineSchedule,
    Prescription,
)
from app.services.profile_service import add_timeline


def create_order(profile, account_id, items, address_text):
    total = Decimal("0")
    order = MedicineOrder(
        profile_id=profile.id,
        ordered_by_account_id=account_id,
        delivery_address=address_text,
        total_amount=Decimal("0"),
        status="confirmed",
    )
    db.session.add(order)
    db.session.flush()

    for item in items:
        medicine = db.session.get(Medicine, int(item["medicine_id"]))
        quantity = int(item["quantity"])
        line_total = Decimal(quantity) * medicine.unit_price
        total += line_total
        unit_label = item.get("unit", "packs")
        db.session.add(
            MedicineOrderItem(
                order_id=order.id,
                medicine_id=medicine.id,
                medicine_name_snapshot=f"{medicine.name} ({unit_label})",
                quantity=quantity,
                unit_price_snapshot=medicine.unit_price,
                line_total=line_total,
            )
        )
        medicine.stock_remaining = max(0, medicine.stock_remaining - quantity)

    order.total_amount = total
    add_timeline(profile.id, account_id, "Medicine ordered", f"{len(items)} medicine item(s) ordered.", "pharmacy")
    db.session.commit()
    return order


def create_appointment(profile, account_id, form):
    appointment = Appointment(
        profile_id=profile.id,
        booked_by_account_id=account_id,
        hospital_id=int(form["hospital_id"]),
        appointment_date=datetime.strptime(form["appointment_date"], "%Y-%m-%d").date(),
        appointment_time=form["appointment_time"],
        reason=form["reason"],
        status="requested",
    )
    db.session.add(appointment)
    add_timeline(profile.id, account_id, "Appointment booked", f"Appointment requested for {appointment.reason}.", "hospitals")
    db.session.commit()
    return appointment


def create_prescription(profile, account_id, filename, extracted_text=None):
    prescription = Prescription(
        profile_id=profile.id,
        uploaded_by_account_id=account_id,
        original_filename=filename or "uploaded-prescription.pdf",
        status="ocr_complete",
        extracted_text=extracted_text or "Metformin 500 mg after breakfast; Amlodipine 5 mg after dinner",
    )
    db.session.add(prescription)
    add_timeline(profile.id, account_id, "Prescription uploaded", "Prescription OCR completed and is ready for review.", "ocr")
    db.session.commit()
    return prescription


def approve_prescription(profile, account_id, prescription_id):
    prescription = db.session.get(Prescription, prescription_id)
    prescription.status = "converted_to_schedule"
    metformin = Medicine.query.filter(Medicine.name.ilike("%Metformin%")).first()
    if metformin:
        db.session.add(
            MedicineSchedule(
                profile_id=profile.id,
                medicine_id=metformin.id,
                dosage_text="1 tablet",
                timing_text="After breakfast",
                adherence_percent=100,
            )
        )
    add_timeline(profile.id, account_id, "OCR reviewed", "Prescription reviewed and converted to a medicine schedule.", "ocr")
    db.session.commit()


def create_care_request(profile, account_id, form):
    request = CareRequest(
        profile_id=profile.id,
        requested_by_account_id=account_id,
        care_type=form["care_type"],
        start_date=datetime.strptime(form["start_date"], "%Y-%m-%d").date(),
        visit_time=form.get("visit_time", "09:00"),
        duration=form["duration"],
        language=form.get("language"),
        gender_preference=form.get("gender_preference"),
        recurring=bool(form.get("recurring")),
        emergency_request=bool(form.get("emergency_request")),
        notes=form.get("notes"),
        status="requested",
    )
    db.session.add(request)
    add_timeline(profile.id, account_id, "Caretaker requested", f"{request.care_type} care requested.", "caretaker")
    db.session.commit()
    return request


def create_home_service(profile, account_id, form):
    booking = HomeServiceBooking(
        profile_id=profile.id,
        booked_by_account_id=account_id,
        service_type=form["service_type"],
        scheduled_date=datetime.strptime(form["scheduled_date"], "%Y-%m-%d").date(),
        notes=form.get("notes"),
        status="requested",
    )
    db.session.add(booking)
    add_timeline(profile.id, account_id, "Home service booked", f"{booking.service_type} service requested.", "home_services")
    db.session.commit()
    return booking


def adjust_inventory(item_id, quantity_delta):
    item = db.session.get(InventoryItem, item_id)
    item.quantity_on_hand = max(0, item.quantity_on_hand + int(quantity_delta))
    item.status = "low_stock" if item.quantity_on_hand <= item.reorder_level else "healthy"
    db.session.commit()
    return item
