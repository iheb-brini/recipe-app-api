from django.db import models
from django.contrib.auth.models import (AbstractBaseUser,
                                        BaseUserManager,
                                        PermissionsMixin)


class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        """ Creates and saves a new user """

        # validations
        UserManager.validateEmail(email)

        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)  # to suppoer multiple database

        return user

    def create_superuser(self, email, password):
        """Creates and saves a new super users"""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user

    @staticmethod
    def validateEmail(email):
        if not email:
            raise ValueError("Users must have a valid email address")


class User(AbstractBaseUser, PermissionsMixin):
    """ custom user model that support using email by defaut """
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'  # change the default behavior username -> email
