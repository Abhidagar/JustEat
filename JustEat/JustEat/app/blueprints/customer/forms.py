from flask_wtf import FlaskForm
from wtforms import (
    FieldList,
    FormField,
    HiddenField,
    SelectField,
    SubmitField,
    TextAreaField,
)
from wtforms.validators import DataRequired, NumberRange


class ItemReviewForm(FlaskForm):
    """
    Form for reviewing individual menu items.

    Attributes:
        item_id (HiddenField): Identifier for the menu item being reviewed
        rating (SelectField): User's rating (1-5 stars) for the item
    """

    # Item identification
    item_id = HiddenField("Item ID")

    # Rating selection
    rating = SelectField(
        "Rating",
        validators=[
            DataRequired(),
            NumberRange(min=1, max=5, message="Rating must be between 1-5"),
        ],
        choices=[(i, i) for i in range(5, 0, -1)],
        default=5,
        coerce=int,  # Ensure value is stored as integer
    )


class RestaurantReviewForm(FlaskForm):
    """
    Form for reviewing the overall restaurant experience.

    Attributes:
        rating (SelectField): Overall restaurant rating (1-5 stars)
        review (TextAreaField): Detailed written review
    """

    # Rating selection
    rating = SelectField(
        "Restaurant Rating",
        validators=[
            DataRequired(),
            NumberRange(min=1, max=5, message="Rating must be between 1-5"),
        ],
        choices=[(i, i) for i in range(5, 0, -1)],
        coerce=int,  # Ensure value is stored as integer
        default=5,
    )

    # Written feedback
    review = TextAreaField(
        "Restaurant Review",
        render_kw={"placeholder": "Share your overall dining experience...", "rows": 4},
    )


class FullReviewForm(FlaskForm):
    """
    Composite form for submitting complete restaurant review with item ratings.

    Attributes:
        item_reviews (FieldList): Collection of individual item reviews
        restaurant_review (FormField): Overall restaurant review section
        submit (SubmitField): Form submission button
    """

    # Item reviews section
    item_reviews = FieldList(FormField(ItemReviewForm), min_entries=0)

    # Restaurant review section
    restaurant_review = FormField(RestaurantReviewForm)

    # Form submission
    submit = SubmitField("Submit Review")
