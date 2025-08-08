from flask import flash, redirect, render_template, url_for
from flask_login import current_user, login_required, login_user, logout_user

from app.models import UserRole
from app.services import auth_service as auth_svc
from app.services import cart_service as cart_svc
from app.utils import get_dashboard_for_role

from . import auth_bp
from .forms import LoginForm, ProfileForm, PasswordResetForm


@auth_bp.route("/")
def about():
    """Display the about/welcome page."""
    # If user is already logged in, redirect to dashboard
    if current_user.is_authenticated:
        return redirect(url_for('auth.dashboard'))
    
    return render_template("about.html")


@auth_bp.route("/Dashboard")
@login_required
def dashboard():
    """Redirect to appropriate dashboard based on user role."""
    dashboard_route = get_dashboard_for_role(current_user.role)
    return redirect(url_for(dashboard_route))


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    """Handle user login process."""
    form = LoginForm()

    if form.validate_on_submit():
        # Authentication logic
        user = auth_svc.login_user(form.email.data, form.password.data)

        if user:
            flash(f"Welcome back {user.name.split()[0]}", "success")
            login_user(user)
            return redirect(url_for("auth.dashboard"))
        else:
            flash("Invalid credentials", "danger")

    return render_template("auth/login.html", form=form)


@auth_bp.route("/logout", methods=["POST"])
@login_required
def logout():
    """Handle user logout process"""
    logout_user()
    return redirect(url_for("auth.login"))


@auth_bp.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    """Handle user profile management."""
    form = ProfileForm(obj=current_user)

    # Profile update logic
    if form.validate_on_submit():
        user = auth_svc.update_profile(current_user, form.name.data, form.phone.data)

        if user:
            flash("Profile updated successfully", "success")
            return redirect(url_for("auth.profile"))
        else:
            flash("Error updating profile", "danger")

    # Customer-specific data
    cart = cart_summary = None
    if current_user.role == UserRole.CUSTOMER:
        cart = cart_svc.get_user_cart(current_user)
        cart_summary = cart_svc.get_cart_summary(current_user)

    return render_template(
        "auth/profile.html",
        form=form,
        cart=cart,
        cart_summary=cart_summary,
        dashboard=True,
        page="profile",
    )


@auth_bp.route("/reset-password", methods=["GET", "POST"])
@login_required
def reset_password():
    """Handle password reset functionality."""
    form = PasswordResetForm()

    if form.validate_on_submit():
        # Attempt to update password
        success = auth_svc.update_password(
            current_user,
            form.current_password.data,
            form.new_password.data
        )

        if success:
            flash("Password updated successfully. Please log in again.", "success")
            logout_user()  # Automatically logout after password change
            return redirect(url_for("auth.login"))
        else:
            flash("Current password is incorrect. Please try again.", "error")
    else:
        # Flash form validation errors
        for field, errors in form.errors.items():
            for error in errors:
                flash(f"{field.replace('_', ' ').title()}: {error}", "error")

    # Customer-specific data for navbar
    cart = cart_summary = None
    if current_user.role == UserRole.CUSTOMER:
        cart = cart_svc.get_user_cart(current_user)
        cart_summary = cart_svc.get_cart_summary(current_user)

    return render_template(
        "auth/reset_password.html",
        form=form,
        cart=cart,
        cart_summary=cart_summary,
        dashboard=True,
        page="reset-password",
    )
