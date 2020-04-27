from django.test import TestCase
from django.contrib.auth import get_user_model
from core import models


def sample_user(email="test@mail.com", password="somepassword"):
    """Create a sample user"""
    return get_user_model().objects.create_user(email, password)


class ModelsTests(TestCase):

    def test_create_user_with_email_successful(self):
        """Test creating a new user with email is successful"""

        email = "test@mail.com"
        password = "test112233"
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test the email for a new user is normalized"""
        email = "testnorm@MAIL.com"
        user = get_user_model().objects.create_user(email, "test123")

        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        """Test creating user with no email raises error"""

        with self.assertRaises(ValueError):
            # if the test doesn't raise ValueError the test will fail
            get_user_model().objects.create_user(None, "test123")

    def test_create_new_superuser(self):
        """Test creating a new superuser"""

        user = get_user_model().objects.create_superuser(
            "test@mail.com",
            "test123"
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_tag_str(self):
        """Test the tag string representation"""
        tag = models.Tag.objects.create(
            user=sample_user(),
            name='Vegan'
        )

        self.assertEqual(str(tag), tag.name)

    def test_ingredient_str(self):
        """Test the ingredient string representation"""
        ingredient = models.Ingredient.objects.create(
            user=sample_user(),
            name='Beef'
        )

        self.assertEqual(str(ingredient), ingredient.name)

    def test_recipe_str(self):
        """Test the recipe string representation"""
        recipe = models.Recipe.objects.create(
            user=sample_user(),
            title="Pasta with meat balls",
            time_minutes=25,
            price=8.00
        )

        self.assertEqual(str(recipe), recipe.title)
