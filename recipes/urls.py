from django.urls import path, include

from .views import ( AddRecipe, Recipes, 
RecipeDetail,  edit_comment, 
CommentDeleteView, DeleteRecipe, 
EditRecipe )


urlpatterns = [
    path("add/", AddRecipe.as_view(), name="add_recipe"),
    path("", Recipes.as_view(), name="recipes"),
    path("<slug:pk>/", RecipeDetail.as_view(), name="recipe_detail"),
    path("delete/<slug:pk>/", DeleteRecipe.as_view(), name="delete_recipe"),
    path("edit/<slug:pk>/", EditRecipe.as_view(), name="edit_recipe"),
    
    path("comment/<int:pk>/edit/", edit_comment, name="edit_comment"),
    path("comment/<int:pk>/delete/", CommentDeleteView.as_view(), name="delete_comment"),
    
    path('accounts/', include('allauth.urls')),
]
