from datetime import date, datetime

from app.extensions import db
from app.models import Medicine, MedicineAdherence, MedicineSchedule
from app.services.profile_service import add_timeline


DOSE_TIMES = {
    "Morning": "08:00",
    "Afternoon": "13:00",
    "Evening": "18:00",
    "Night": "21:00",
}


def create_schedule(profile, account_id, form):
    medicine = db.session.get(Medicine, int(form["medicine_id"]))
    periods = _periods_from_form(form)
    schedule = MedicineSchedule(
        profile_id=profile.id,
        medicine_id=medicine.id,
        dosage_text=f"{form['quantity_per_dose']} {form['unit']}",
        timing_text=", ".join(periods),
        start_date=datetime.strptime(form["start_date"], "%Y-%m-%d").date(),
        end_date=datetime.strptime(form["end_date"], "%Y-%m-%d").date() if form.get("end_date") else None,
        forever_medication=bool(form.get("forever_medication")),
        times_per_day=len(periods),
        dose_morning="Morning" in periods,
        dose_afternoon="Afternoon" in periods,
        dose_evening="Evening" in periods,
        dose_night="Night" in periods,
        food_timing=form["food_timing"],
        quantity_per_dose=form["quantity_per_dose"],
        unit=form["unit"],
        repeat_pattern=form["repeat_pattern"],
        repeat_days=form.get("repeat_days"),
        notes=form.get("notes"),
    )
    db.session.add(schedule)
    db.session.flush()
    ensure_today_adherence(schedule)
    add_timeline(profile.id, account_id, "Medicine schedule created", f"{medicine.name} schedule added to profile.", "medicines")
    db.session.commit()
    return schedule


def ensure_today_adherence(schedule):
    today = date.today()
    if schedule.start_date and schedule.start_date > today:
        return []
    if schedule.end_date and schedule.end_date < today:
        return []
    records = []
    for period in _periods_from_schedule(schedule):
        existing = MedicineAdherence.query.filter_by(
            schedule_id=schedule.id,
            dose_date=today,
            dose_period=period,
        ).first()
        if existing:
            records.append(existing)
            continue
        record = MedicineAdherence(
            schedule_id=schedule.id,
            profile_id=schedule.profile_id,
            dose_date=today,
            dose_period=period,
            dose_time=DOSE_TIMES[period],
            status="due",
        )
        db.session.add(record)
        records.append(record)
    return records


def due_today(profile_id):
    schedules = MedicineSchedule.query.filter_by(profile_id=profile_id, status="active").all()
    records = []
    for schedule in schedules:
        records.extend(ensure_today_adherence(schedule))
    db.session.commit()
    return MedicineAdherence.query.filter_by(profile_id=profile_id, dose_date=date.today()).order_by(MedicineAdherence.dose_time).all()


def confirm_adherence(record_id, account_id, status, notes=None):
    record = db.session.get(MedicineAdherence, record_id)
    record.status = status
    record.confirmed_by_account_id = account_id
    record.notes = notes
    add_timeline(record.profile_id, account_id, f"Medicine {status}", f"{record.schedule.medicine.name} {record.dose_period} dose marked {status}.", "medicines")
    _recalculate_adherence(record.schedule)
    db.session.commit()
    return record


def _recalculate_adherence(schedule):
    records = MedicineAdherence.query.filter_by(schedule_id=schedule.id).all()
    if not records:
        return
    taken = len([record for record in records if record.status == "taken"])
    schedule.adherence_percent = round((taken / len(records)) * 100)


def _periods_from_form(form):
    periods = [period for period in DOSE_TIMES if form.get(f"dose_{period.lower()}")]
    return periods or ["Morning"]


def _periods_from_schedule(schedule):
    periods = []
    if schedule.dose_morning:
        periods.append("Morning")
    if schedule.dose_afternoon:
        periods.append("Afternoon")
    if schedule.dose_evening:
        periods.append("Evening")
    if schedule.dose_night:
        periods.append("Night")
    return periods or ["Morning"]
