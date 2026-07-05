from flask import flash, redirect, render_template, request, session, url_for

from app.models import Medicine, MedicineAdherence, MedicineCategory, MedicineOrder, MedicineSchedule
from app.permissions.decorators import account_type_required
from app.services.auth_service import current_account
from app.services.module_service import create_order
from app.services.profile_service import active_profile
from app.services.schedule_service import confirm_adherence, create_schedule, due_today

from . import pharmacy_bp


@pharmacy_bp.get("/")
@account_type_required("family")
def catalogue():
    query = request.args.get("q", "")
    category_id = request.args.get("category_id", type=int)
    medicines_query = Medicine.query
    if query:
        pattern = f"%{query}%"
        medicines_query = medicines_query.filter(
            Medicine.name.ilike(pattern)
            | Medicine.generic_name.ilike(pattern)
            | Medicine.brand.ilike(pattern)
        )
    if category_id:
        medicines_query = medicines_query.filter_by(category_id=category_id)
    medicines = medicines_query.limit(48).all()
    return render_template("pharmacy/catalogue.html", medicines=medicines, categories=MedicineCategory.query.all(), query=query, cart_count=len(session.get("cart", [])))


@pharmacy_bp.route("/schedule/new/<int:medicine_id>", methods=["GET", "POST"])
@account_type_required("family")
def new_schedule(medicine_id):
    profile = active_profile(current_account().id)
    medicine = Medicine.query.get_or_404(medicine_id)
    if request.method == "POST":
        create_schedule(profile, current_account().id, request.form)
        flash("Medicine schedule created and today's reminders generated.", "success")
        return redirect(url_for("pharmacy.schedules"))
    return render_template("pharmacy/schedule_form.html", medicine=medicine, profile=profile)


@pharmacy_bp.get("/schedules")
@account_type_required("family")
def schedules():
    profile = active_profile(current_account().id)
    records = due_today(profile.id) if profile else []
    schedules = MedicineSchedule.query.filter_by(profile_id=profile.id, status="active").order_by(MedicineSchedule.created_at.desc()).all() if profile else []
    history = MedicineAdherence.query.filter_by(profile_id=profile.id).order_by(MedicineAdherence.dose_date.desc(), MedicineAdherence.dose_time.desc()).limit(30).all() if profile else []
    return render_template("pharmacy/schedules.html", schedules=schedules, records=records, history=history, profile=profile)


@pharmacy_bp.post("/adherence/<int:record_id>")
@account_type_required("family")
def adherence(record_id):
    confirm_adherence(record_id, current_account().id, request.form["status"], request.form.get("notes"))
    flash("Medicine confirmation saved.", "success")
    return redirect(url_for("pharmacy.schedules"))


@pharmacy_bp.post("/cart/add")
@account_type_required("family")
def add_to_cart():
    cart = session.get("cart", [])
    cart.append(
        {
            "medicine_id": int(request.form["medicine_id"]),
            "quantity": int(request.form["quantity"]),
            "unit": request.form.get("unit", "packs"),
        }
    )
    session["cart"] = cart
    flash("Medicine added to cart.", "success")
    return redirect(url_for("pharmacy.catalogue"))


@pharmacy_bp.get("/cart")
@account_type_required("family")
def cart():
    profile = active_profile(current_account().id)
    cart_items = []
    total = 0
    for item in session.get("cart", []):
        medicine = Medicine.query.get(item["medicine_id"])
        line_total = medicine.unit_price * item["quantity"]
        total += line_total
        cart_items.append({"medicine": medicine, "quantity": item["quantity"], "unit": item["unit"], "line_total": line_total})
    return render_template("pharmacy/cart.html", cart_items=cart_items, total=total, profile=profile)


@pharmacy_bp.post("/cart/clear")
@account_type_required("family")
def clear_cart():
    session["cart"] = []
    flash("Cart cleared.", "success")
    return redirect(url_for("pharmacy.cart"))


@pharmacy_bp.post("/cart/remove/<int:item_index>")
@account_type_required("family")
def remove_from_cart(item_index):
    cart = session.get("cart", [])
    if 0 <= item_index < len(cart):
        cart.pop(item_index)
        session["cart"] = cart
        flash("Medicine removed from cart.", "success")
    else:
        flash("That cart item could not be found.", "error")
    return redirect(url_for("pharmacy.cart"))


@pharmacy_bp.post("/order")
@account_type_required("family")
def order():
    profile = active_profile(current_account().id)
    cart = session.get("cart", [])
    if not cart:
        flash("Your cart is empty.", "error")
        return redirect(url_for("pharmacy.catalogue"))
    address = profile.addresses[0] if profile and profile.addresses else None
    if not address:
        flash("Add a delivery address before ordering.", "error")
        return redirect(url_for("pharmacy.cart"))
    create_order(profile, current_account().id, cart, f"{address.line1}, {address.city}, {address.state}")
    session["cart"] = []
    flash("Order placed. This is a simulated confirmation for the prototype.", "success")
    return redirect(url_for("pharmacy.orders"))


@pharmacy_bp.get("/orders")
@account_type_required("family")
def orders():
    profile = active_profile(current_account().id)
    orders = MedicineOrder.query.filter_by(profile_id=profile.id).order_by(MedicineOrder.created_at.desc()).all() if profile else []
    return render_template("pharmacy/orders.html", orders=orders)
