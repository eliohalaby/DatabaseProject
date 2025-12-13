from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from .models import Customer

auth = Blueprint("auth", __name__)

ADMIN_EMAIL = "admin@admin.com"
ADMIN_PASSWORD = "admin123"

@auth.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        first_name = request.form.get("first_name", "").strip()
        last_name = request.form.get("last_name", "").strip()
        email = request.form.get("email", "").strip().lower()
        phone_number = request.form.get("phone_number", "").strip()
        password = request.form.get("password", "")
        confirm = request.form.get("confirm_password", "")

        if not all([first_name, last_name, email, phone_number, password, confirm]):
            flash("Please fill all fields.", "warning")
            return redirect(url_for("auth.signup"))

        if password != confirm:
            flash("Passwords do not match.", "danger")
            return redirect(url_for("auth.signup"))

        if email == ADMIN_EMAIL:
            flash("This email is reserved.", "danger")
            return redirect(url_for("auth.signup"))

        if Customer.query.filter_by(email=email).first():
            flash("Email already exists.", "warning")
            return redirect(url_for("auth.login"))

        if Customer.query.filter_by(phone_number=phone_number).first():
            flash("Phone number already exists.", "warning")
            return redirect(url_for("auth.signup"))

        new_customer = Customer(
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone_number=phone_number,
            password_hash=generate_password_hash(password)
        )
        db.session.add(new_customer)
        db.session.commit()

        flash("Account created successfully! Please log in.", "success")
        return redirect(url_for("auth.login"))

    return render_template("signup.html")


@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        # Admin login
        if email == ADMIN_EMAIL and password == ADMIN_PASSWORD:
            session.clear()
            session["role"] = "admin"
            session["email"] = email
            flash("Logged in as Admin.", "success")
            return redirect(url_for("admin.list_items"))  # ✅ route exists

        # Customer login
        customer = Customer.query.filter_by(email=email).first()
        if not customer or not check_password_hash(customer.password_hash, password):
            flash("Invalid email or password.", "danger")
            return redirect(url_for("auth.login"))

        session.clear()
        session["role"] = "customer"
        session["user_id"] = customer.user_id
        session["first_name"] = customer.first_name
        session["last_name"] = customer.last_name
        session["email"] = customer.email

        flash(f"Welcome {customer.first_name}!", "success")
        return redirect(url_for("user_hp.homepage", user_id=customer.user_id))  # ✅ correct endpoint

    return render_template("login.html")


@auth.route("/logout")
def logout():
    session.clear()
    flash("Logged out successfully.", "info")
    return redirect(url_for("auth.login"))
