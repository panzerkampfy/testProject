from datetime import timezone, time, datetime

from django.contrib.auth.hashers import check_password, make_password
from django.contrib.auth.models import User, UserManager
from django.db import models
from django.contrib.auth.validators import UnicodeUsernameValidator


class User(models.Model):
    username_validator = UnicodeUsernameValidator()

    username = models.CharField(
        max_length=150,
        unique=True,
        help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.',
        validators=[username_validator],
        error_messages={
            'unique': "A user with that username already exists.",
        },
    )
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    email = models.EmailField(blank=False)
    city = models.CharField(max_length=100, null=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    password = models.CharField(max_length=100, blank=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []
    objects = UserManager()

    @property
    def is_anonymous(self):
        return False

    @property
    def is_authenticated(self):
        return True

    def set_password(self, raw_password):
        self.password = make_password(raw_password)
        self._password = raw_password

    def check_password(self, raw_password):
        """
        Return a boolean of whether the raw_password was correct. Handles
        hashing formats behind the scenes.
        """

        def setter(raw_password):
            self.set_password(raw_password)
            # Password hash upgrades shouldn't be considered password changes.
            self._password = None
            self.save(update_fields=["password"])

        return check_password(raw_password, self.password, setter)
