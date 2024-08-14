from django.urls import path
from pieceofcakeapp.views import IndexView

urlpatterns = [
    path('', IndexView.as_view(), name='home'),
    
]