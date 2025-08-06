from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length


class LoginForm(FlaskForm):
    """
    Form for handling user login credentials.

    Attributes:
        email (StringField): Email input field with email validation.
        password (PasswordField): Password input field (required).
        submit (SubmitField): Form submission button.
    """

    # Authentication fields
    email = StringField(
        "Email",
        validators=[DataRequired(), Email()],
        render_kw={"placeholder": "user@example.com"},
    )
    password = PasswordField(
        "Password",
        validators=[DataRequired()],
        render_kw={"placeholder": "Enter your password"},
    )

    # Submission
    submit = SubmitField("Login")


class ProfileForm(FlaskForm):
    """
    Form for handling user profile information updates.

    Attributes:
        name (StringField): User's full name (required).
        email (StringField): User's email (disabled for editing).
        phone (StringField): User's phone number (required).
        submit (SubmitField): Form submission button.
    """

    # Personal Information
    name = StringField(
        "Name",
        validators=[DataRequired()],
        render_kw={"placeholder": "Enter your name"},
    )
    phone = StringField(
        "Phone",
        validators=[DataRequired()],
        render_kw={"placeholder": "Enter your phone number"},
    )

    # Read-only Information
    email = StringField(
        "Email",
        validators=[DataRequired(), Email()],
        render_kw={"disabled": True},
    )

    # Submission
    submit = SubmitField("Update Profile")


class PasswordResetForm(FlaskForm):
    """
    Form for handling password reset functionality.

    Attributes:
        current_password (PasswordField): Current password for verification.
        new_password (PasswordField): New password field.
        confirm_password (PasswordField): Password confirmation field.
        submit (SubmitField): Form submission button.
    """

    current_password = PasswordField(
        "Current Password",
        validators=[DataRequired()],
        render_kw={"placeholder": "Enter your current password"},
    )
    new_password = PasswordField(
        "New Password",
        validators=[
            DataRequired(),
            Length(min=6, message="Password must be at least 6 characters long")
        ],
        render_kw={"placeholder": "Enter your new password"},
    )
    confirm_password = PasswordField(
        "Confirm New Password",
        validators=[
            DataRequired(),
            EqualTo("new_password", message="Passwords must match")
        ],
        render_kw={"placeholder": "Confirm your new password"},
    )

    submit = SubmitField("Reset Password")
