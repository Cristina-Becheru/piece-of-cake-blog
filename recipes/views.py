from django.shortcuts import render
from django.views.generic import (
    CreateView, ListView)
from django.contrib.auth.mixins import (
    UserPassesTestMixin, LoginRequiredMixin, 
)

from django.db.models import Q
from .models import Recipe
from .forms import RecipeForm



CAKE_TYPES = [
    ("classic", "Classic"),
    ("fruit", "Fruit Cake"),
    ("cupcake", "Cupcake"),
    ("cheesecake", "Cheesecake"),
]

FLAVOR_TYPES = [
    ("vanilla", "Vanilla"),
    ("chocolate", "Chocolate"),
    ("strawberry", "Strawberry"),
    ("lemon", "Lemon"),
    ("coffee", "Coffee"),
]

class Recipes(ListView):
    """View all recipes"""

    template_name = "recipes/recipes.html"
    model = Recipe
    context_object_name = "recipes"
    paginate_by = 8

    def get_queryset(self, **kwargs):
        query = self.request.GET.get('q')
        cake_type_slug = self.request.GET.get('cake_type')
        flavor_slug = self.request.GET.get('flavor')

        recipes = self.model.objects.all()

        if query:
            recipes = recipes.filter(
                Q(title__icontains=query) |
                Q(description__icontains=query) |
                Q(instructions__icontains=query)
            )

        if cake_type_slug:
            recipes = recipes.filter(cake_type=cake_type_slug)

        if flavor_slug:
            recipes = recipes.filter(flavor=flavor_slug)

        return recipes

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cake_types'] = dict(CAKE_TYPES)
        context['flavor_types'] = dict(FLAVOR_TYPES)
        return context

class AddRecipe(LoginRequiredMixin, CreateView):
    """Add recipe view"""

    template_name = "recipes/add_recipe.html"
    model = Recipe
    form_class = RecipeForm
    success_url = "/recipes/"

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)