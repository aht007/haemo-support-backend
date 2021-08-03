from django.urls import path
from .views import AddIllnes, CreateHealthProfile, EditHealthProfile, EditIllness, GetHealthProfile, RemoveIllness


urlpatterns = [
    path('profile/edit/<int:pk>/', EditHealthProfile.as_view(), name='edit_health_profile'),
    path('profile/', GetHealthProfile.as_view(), name='get_health_profile'),
    path('profile/create', CreateHealthProfile.as_view(), name='create_health_profile'),
    path('profile/illness/add', AddIllnes.as_view(), name='add_illness'),
    path('profile/illness/edit/<int:pk>/', EditIllness.as_view(), name='edit_illness'),
    path('profile/illness/delete/<int:pk>/', RemoveIllness.as_view(), name='delete_illness'),
]