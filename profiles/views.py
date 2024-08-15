from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from .models import Profile
from recipes.models import Recipe

class Profiles(LoginRequiredMixin, TemplateView):
    """User Profile View"""

    template_name = "profiles/profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_id = self.kwargs.get("pk")
        profile = get_object_or_404(Profile, user__id=user_id)  # Use user__id
        context["profile"] = profile

        # Limit the queryset to the 5 most recent recipes
        context["user_recipes"] = profile.user.cake_recipes.order_by("-posted_date")[:5]

        return context

        
