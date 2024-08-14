from django.urls import path

from .views import AddRecipe, Recipes, RecipeDetail,  edit_comment, CommentDeleteView


urlpatterns = [
    path("add/", AddRecipe.as_view(), name="add_recipe"),
    path("", Recipes.as_view(), name="recipes"),
    path("<slug:pk>/", RecipeDetail.as_view(), name="recipe_detail"),
    
    path("comment/<int:pk>/edit/", edit_comment, name="edit_comment"),
    path("comment/<int:pk>/delete/", CommentDeleteView.as_view(), name="delete_comment"),
]
