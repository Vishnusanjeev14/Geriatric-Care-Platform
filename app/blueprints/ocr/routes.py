from flask import flash, redirect, render_template, request, session, url_for

from app.models import Medicine, Prescription
from app.permissions.decorators import account_type_required
from app.services.auth_service import current_account
from app.services.module_service import create_prescription
from app.services.ocr_service import PRINTED_ONLY_NOTICE, extract_prescription_text, recognize_medicines
from app.services.profile_service import active_profile

from . import ocr_bp


@ocr_bp.route("/", methods=["GET", "POST"])
@account_type_required("family")
def upload():
    profile = active_profile(current_account().id)
    if request.method == "POST":
        file = request.files.get("prescription")
        extracted_text, engine = extract_prescription_text(file)
        prescription = create_prescription(profile, current_account().id, file.filename if file else "mock-prescription.pdf", extracted_text)
        flash("OCR processing complete. Review the recognized medicines.", "success")
        return redirect(url_for("ocr.review", prescription_id=prescription.id))
    prescriptions = Prescription.query.filter_by(profile_id=profile.id).order_by(Prescription.created_at.desc()).all() if profile else []
    return render_template("ocr/upload.html", prescriptions=prescriptions)


@ocr_bp.route("/<int:prescription_id>/review", methods=["GET", "POST"])
@account_type_required("family")
def review(prescription_id):
    profile = active_profile(current_account().id)
    prescription = Prescription.query.filter_by(id=prescription_id, profile_id=profile.id).first_or_404()
    if request.method == "POST":
        cart = session.get("cart", [])
        matches, _ = recognize_medicines(prescription.extracted_text or "")
        for match in matches:
            cart.append({"medicine_id": match["medicine"].id, "quantity": match["quantity"], "unit": "Sheets / Strips"})
        session["cart"] = cart
        prescription.status = "reviewed"
        flash("Matched medicines added to cart for review.", "success")
        return redirect(url_for("pharmacy.cart"))
    matches, unmatched = recognize_medicines(prescription.extracted_text or "")
    return render_template("ocr/review.html", prescription=prescription, matches=matches, unmatched=unmatched, notice=PRINTED_ONLY_NOTICE)
