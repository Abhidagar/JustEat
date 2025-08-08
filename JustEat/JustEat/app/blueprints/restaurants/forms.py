from datetime import time

from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField
from wtforms import (
    BooleanField,
    DecimalField,
    SelectField,
    SelectMultipleField,
    StringField,
    SubmitField,
    TextAreaField,
    TimeField,
)
from wtforms.validators import DataRequired, Length, Optional


class RestaurantForm(FlaskForm):
    """Form for creating/editing restaurant information."""

    # Basic Information
    name = StringField(
        "Restaurant Name",
        validators=[DataRequired(), Length(min=2, max=100)],
        description="Official name of the restaurant (2-100 characters)",
    )
    location = StringField(
        "Location",
        validators=[DataRequired(), Length(max=200)],
        description="Physical address of the restaurant",
    )

    # Operating Hours
    opening_time = TimeField(
        "Opening Time",
        validators=[DataRequired()],
        default=time(9, 0),
        description="Daily opening time",
    )
    closing_time = TimeField(
        "Closing Time",
        validators=[DataRequired()],
        default=time(22, 0),
        description="Daily closing time",
    )

    # Form Submission
    submit = SubmitField("Save Restaurant")


class CuisineForm(FlaskForm):
    """Form for managing restaurant cuisine types."""

    cuisines = SelectMultipleField(
        "Cuisines",
        coerce=int,
        validators=[DataRequired()],
        description="Select all applicable cuisine types",
    )


class ItemForm(FlaskForm):
    """Form for creating/editing menu items."""

    # Item Details
    name = StringField(
        "Item Name", 
        validators=[DataRequired()], 
        description="Name of the menu item"
    )
    description = TextAreaField(
        "Description",
        validators=[Optional()],
        description="Item description (optional)",
    )
    price = DecimalField(
        "Price",
        validators=[DataRequired()],
        places=2,
        description="Price in local currency",
    )

    # Classification
    cuisine_id = SelectField(
        "Select Cuisine",
        validators=[DataRequired()],
        description="Primary cuisine type",
    )
    category_id = SelectField(
        "Select Category", 
        validators=[DataRequired()], 
        description="Menu category"
    )
    is_non_veg = BooleanField(
        "Non Veg", 
        description="Check if non-vegetarian item"
        )

    # Form Submission
    submit = SubmitField("Submit")
