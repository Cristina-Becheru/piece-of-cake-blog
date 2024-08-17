from django.test import TestCase
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Recipe, Comment


class RecipeModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')

    def test_recipe_creation(self):
        recipe = Recipe.objects.create(
            user=self.user,
            title="Delicious Cake",
            description="A very delicious cake.",
            ingredients="Flour, Sugar, Eggs",
            instructions="Mix ingredients and bake.",
            image=None,  
            image_alt="Image of the cake",
            cake_type="classic",
            flavor="vanilla",
            calories=300,
            prep_time="30 minutes",
            servings=4,
            cook_time="45 minutes",
        )
        self.assertEqual(recipe.title, "Delicious Cake")
        self.assertEqual(recipe.description, "A very delicious cake.")
        self.assertEqual(recipe.ingredients, "Flour, Sugar, Eggs")
        self.assertEqual(recipe.instructions, "Mix ingredients and bake.")
        self.assertEqual(recipe.cake_type, "classic")
        self.assertEqual(recipe.flavor, "vanilla")
        self.assertEqual(recipe.calories, 300)
        self.assertEqual(recipe.prep_time, "30 minutes")
        self.assertEqual(recipe.servings, 4)
        self.assertEqual(recipe.cook_time, "45 minutes")

    def test_recipe_str_method(self):
        recipe = Recipe.objects.create(
            user=self.user,
            title="Delicious Cake",
            description="A very delicious cake.",
            ingredients="Flour, Sugar, Eggs",
            instructions="Mix ingredients and bake.",
            image=None,  
            image_alt="Image of the cake",
            cake_type="classic",
            flavor="vanilla",
            calories=300,
            prep_time="30 minutes",
            servings=4,
            cook_time="45 minutes",
        )
        self.assertEqual(str(recipe), "Delicious Cake")

    def test_recipe_ordering(self):
        recipe1 = Recipe.objects.create(
            user=self.user,
            title="Old Cake",
            description="An old cake.",
            ingredients="Flour, Sugar",
            instructions="Mix and bake.",
            image=None, 
            image_alt="Old cake image",
            cake_type="classic",
            flavor="vanilla",
            calories=200,
            prep_time="15 minutes",
            servings=2,
            cook_time="30 minutes",
        )
        recipe2 = Recipe.objects.create(
            user=self.user,
            title="New Cake",
            description="A new cake.",
            ingredients="Flour, Sugar, Eggs, Chocolate",
            instructions="Mix and bake.",
            image=None, 
            image_alt="New cake image",
            cake_type="classic",
            flavor="chocolate",
            calories=350,
            prep_time="45 minutes",
            servings=6,
            cook_time="60 minutes",
        )
        recipes = list(Recipe.objects.all())
        self.assertEqual(recipes[0], recipe2)
        self.assertEqual(recipes[1], recipe1)

class CommentModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.recipe = Recipe.objects.create(
            user=self.user,
            title="Sample Recipe",
            description="A sample recipe.",
            ingredients="Flour, Sugar",
            instructions="Mix and bake.",
            image=None, 
            image_alt="Sample image",
            cake_type="classic",
            flavor="vanilla",
            calories=200,
            prep_time="15 minutes",
            servings=2,
            cook_time="30 minutes",
        )

    def test_comment_creation(self):
        comment = Comment.objects.create(
            user=self.user,
            recipe=self.recipe,
            content="Great recipe!",
            rating=5,
        )
        self.assertEqual(comment.content, "Great recipe!")
        self.assertEqual(comment.rating, 5)
        self.assertEqual(comment.user, self.user)
        self.assertEqual(comment.recipe, self.recipe)

    def test_comment_str_method(self):
        comment = Comment.objects.create(
            user=self.user,
            recipe=self.recipe,
            content="Great recipe!",
            rating=5,
        )
        self.assertEqual(str(comment), f"Comment by testuser on Sample Recipe")

    def test_comment_ordering(self):
        comment1 = Comment.objects.create(
            user=self.user,
            recipe=self.recipe,
            content="First comment",
            rating=3,
        )
        comment2 = Comment.objects.create(
            user=self.user,
            recipe=self.recipe,
            content="Second comment",
            rating=4,
        )
        comments = list(Comment.objects.all())
        self.assertEqual(comments[0], comment2)
        self.assertEqual(comments[1], comment1)

class RecipeModelTest(TestCase):
    def setUp(self):
        
        self.user = User.objects.create_user(username='testuser', password='testpass')

    def test_create_recipe_without_image(self):
       
        recipe = Recipe.objects.create(
            user=self.user,
            title="Test Recipe",
            description="This is a test recipe.",
            ingredients="Flour, Sugar, Eggs",
            instructions="Mix and bake.",
            image=None,  
            image_alt="Test Image Alt",
            cake_type="classic",
            flavor="vanilla",
            calories=200,
            prep_time="30 minutes",
            cook_time="45 minutes",
            servings=4
        )
        self.assertIsInstance(recipe, Recipe)
        self.assertEqual(recipe.title, "Test Recipe")

    def test_recipe_string_representation(self):
        recipe = Recipe.objects.create(
            user=self.user,
            title="Test Recipe",
            description="This is a test recipe.",
            ingredients="Flour, Sugar, Eggs",
            instructions="Mix and bake.",
            image=None,
            image_alt="Test Image Alt",
            cake_type="classic",
            flavor="vanilla",
            calories=200,
            prep_time="30 minutes",
            cook_time="45 minutes",
            servings=4
        )
        self.assertEqual(str(recipe), "Test Recipe")

    def test_recipe_ordering(self):
        recipe1 = Recipe.objects.create(
            user=self.user,
            title="Old Recipe",
            description="Old recipe description.",
            ingredients="Flour",
            instructions="Mix.",
            image=None,
            image_alt="Old Image Alt",
            cake_type="classic",
            flavor="vanilla",
            calories=100,
            prep_time="10 minutes",
            cook_time="20 minutes",
            servings=2,
            posted_date=timezone.make_aware(timezone.datetime(2023, 1, 1))
        )
        recipe2 = Recipe.objects.create(
            user=self.user,
            title="New Recipe",
            description="New recipe description.",
            ingredients="Sugar",
            instructions="Bake.",
            image=None,
            image_alt="New Image Alt",
            cake_type="fruit",
            flavor="chocolate",
            calories=300,
            prep_time="40 minutes",
            cook_time="60 minutes",
            servings=6,
            posted_date=timezone.make_aware(timezone.datetime(2024, 1, 1))
        )
        self.assertEqual(list(Recipe.objects.all()), [recipe2, recipe1])

class CommentModelTest(TestCase):
    def setUp(self):
        
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.recipe = Recipe.objects.create(
            user=self.user,
            title="Test Recipe",
            description="This is a test recipe.",
            ingredients="Flour, Sugar, Eggs",
            instructions="Mix and bake.",
            image=None,
            image_alt="Test Image Alt",
            cake_type="classic",
            flavor="vanilla",
            calories=200,
            prep_time="30 minutes",
            cook_time="45 minutes",
            servings=4
        )

    def test_create_comment(self):
        comment = Comment.objects.create(
            user=self.user,
            recipe=self.recipe,
            content="Great recipe!",
            rating=5
        )
        self.assertIsInstance(comment, Comment)
        self.assertEqual(comment.content, "Great recipe!")

    def test_comment_string_representation(self):
        comment = Comment.objects.create(
            user=self.user,
            recipe=self.recipe,
            content="Nice!",
            rating=4
        )
        self.assertEqual(str(comment), f"Comment by {self.user.username} on {self.recipe.title}")

    def test_comment_ordering(self):
        comment1 = Comment.objects.create(
            user=self.user,
            recipe=self.recipe,
            content="Good recipe.",
            rating=3,
            created_at=timezone.make_aware(timezone.datetime(2024, 1, 1))
        )
        comment2 = Comment.objects.create(
            user=self.user,
            recipe=self.recipe,
            content="Excellent!",
            rating=5,
            created_at=timezone.make_aware(timezone.datetime(2024, 2, 1))
        )
        self.assertEqual(list(Comment.objects.all()), [comment2, comment1])
        
    