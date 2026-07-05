from flask import flash, redirect, render_template, request, url_for

from app.models import InventoryItem, Medicine, MedicineOrder
from app.permissions.decorators import account_type_required
from app.services.module_service import adjust_inventory

from . import healthcare_bp


@healthcare_bp.get("/login")
def login():
    return redirect(url_for("auth.login"))


@healthcare_bp.get("/dashboard")
@account_type_required("healthcare")
def dashboard():
    inventory = InventoryItem.query.order_by(InventoryItem.status.desc()).all()
    orders = (
        MedicineOrder.query.filter(MedicineOrder.status.notin_(["completed", "cancelled"]))
        .order_by(MedicineOrder.created_at.desc())
        .limit(8)
        .all()
    )
    return render_template("healthcare/dashboard.html", inventory=inventory, orders=orders)


@healthcare_bp.route("/inventory", methods=["GET", "POST"])
@account_type_required("healthcare")
def inventory():
    if request.method == "POST":
        adjust_inventory(request.form["item_id"], request.form["quantity_delta"])
        flash("Inventory updated.", "success")
        return redirect(url_for("healthcare.inventory"))
    return render_template("healthcare/inventory.html", inventory=InventoryItem.query.all(), medicines=Medicine.query.all())


@healthcare_bp.post("/orders/<int:order_id>/status")
@account_type_required("healthcare")
def update_order(order_id):
    order = MedicineOrder.query.get_or_404(order_id)
    order.status = request.form["status"]
    from app.extensions import db

    db.session.commit()
    flash("Order status updated.", "success")
    return redirect(url_for("healthcare.dashboard"))
