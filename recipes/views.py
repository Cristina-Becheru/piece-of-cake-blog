from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import (
    CreateView,
    ListView,
    DetailView,
    DeleteView,
    UpdateView,
)
from django.contrib.auth.mixins import (
    UserPassesTestMixin,
    LoginRequiredMixin,
)
from django.db.models import Q
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required

from .models import Recipe, Comment
from .forms import RecipeForm, CommentForm

# Define cake types and flavors as constants
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
        query = self.request.GET.get("q")
        cake_type_slug = self.request.GET.get("cake_type")
        flavor_slug = self.request.GET.get("flavor")

        recipes = self.model.objects.all()

        if query:
            recipes = recipes.filter(
                Q(title__icontains=query)
                | Q(description__icontains=query)
                | Q(instructions__icontains=query)
            )

        if cake_type_slug:
            recipes = recipes.filter(cake_type=cake_type_slug)

        if flavor_slug:
            recipes = recipes.filter(flavor=flavor_slug)

        return recipes

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["cake_types"] = dict(CAKE_TYPES)
        context["flavor_types"] = dict(FLAVOR_TYPES)
        return context


class RecipeDetail(DetailView):
    """View a single recipe"""

    template_name = "recipes/recipe_detail.html"
    model = Recipe
    context_object_name = "recipe"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["comment_form"] = CommentForm()
        context["comments"] = self.object.comments.all()
        return context

    def post(self, request, *args, **kwargs):
        recipe = self.get_object()
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.recipe = recipe
            comment.user = request.user
            comment.save()
            return redirect("recipe_detail", pk=recipe.pk)
        return self.render_to_response(self.get_context_data(comment_form=form))


class AddRecipe(LoginRequiredMixin, CreateView):
    """Add recipe view"""

    template_name = "recipes/add_recipe.html"
    model = Recipe
    form_class = RecipeForm
    success_url = "/recipes/"

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

@login_required
def edit_comment(request, pk):
    """Edit a comment"""
    comment = get_object_or_404(Comment, pk=pk)

    if request.user != comment.user and not request.user.is_staff:
        return redirect('recipe_detail', pk=comment.recipe.pk)

    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect('recipe_detail', pk=comment.recipe.pk)
    else:
        form = CommentForm(instance=comment)

    return render(request, 'recipes/edit_comment.html', {'form': form})

class CommentDeleteView(LoginRequiredMixin, DeleteView):
    """Delete a comment"""
    model = Comment
    template_name = 'comments/delete_comment.html'

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)

    def get_success_url(self):
        return reverse_lazy('recipe_detail', kwargs={'pk': self.object.recipe.pk})
