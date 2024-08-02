from django.contrib import admin
from .models import Recipe


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "cake_type",
        "flavor",
        "calories",
        "posted_date",
        "image",
    )
    list_filter = ("cake_type", "flavor")
    search_fields = ("title", "description", "ingredients")
    ordering = ("-posted_date",)
