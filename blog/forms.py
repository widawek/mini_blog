from werkzeug.routing import ValidationError
from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, PasswordField
from wtforms.validators import DataRequired
from config import Config


class EntryForm(FlaskForm):
    """
    Form for creating or editing blog entries.

    This form is used to gather data for a blog entry including the title,
    content, and publication status. It uses Flask-WTF and validators to
    ensure that the required data is provided.

    Attributes:
        title (StringField): Field for the entry's title, input is required.
        body (StringField): Field for the entry's content, input is required.
        is_published (BooleanField): Checkbox to indicate if the entry is to be published.
    """

    title = StringField('Title', validators=[DataRequired()])
    body = StringField('Content', validators=[DataRequired()])
    is_published = BooleanField('Is_published?')


class LoginForm(FlaskForm):
    """
    Form for user login.

    This form is used for the authentication of users. It includes fields for
    username and password, and contains custom validation methods to verify
    the credentials against the application's configuration.

    Attributes:
        username (StringField): Field for entering the username, input is required.
        password (PasswordField): Field for entering the password, input is required.
    """

    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])

    def validate_username(self, field):
        """
        Validate the username.

        Custom validation method to check if the provided username matches
        the ADMIN_USERNAME in the application's configuration. Raises a
        ValidationError if it doesn't match.

        Args:
            field: The field instance containing the input data for the username.

        Returns:
            str: The validated username if validation is successful.

        Raises:
            ValidationError: If the input username does not match the expected value.
        """

        if field.data != Config.ADMIN_USERNAME:
            raise ValidationError("Invalid username")
        return field.data

    def validate_password(self, field):
        """
        Validate the password.

        Custom validation method to check if the provided password matches
        the ADMIN_PASSWORD in the application's configuration. Raises a
        ValidationError if it doesn't match.

        Args:
            field: The field instance containing the input data for the password.

        Returns:
            str: The validated password if validation is successful.

        Raises:
            ValidationError: If the input password does not match the expected value.
        """

        if field.data != Config.ADMIN_PASSWORD:
            raise ValidationError("Invalid password")
        return field.data
