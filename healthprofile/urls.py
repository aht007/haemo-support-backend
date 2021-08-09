from django.urls import path
from .views import HealthProfileView, IllnessView


urlpatterns = [
    path('profile/edit/<int:pk>/', HealthProfileView.as_view(), name='edit_health_profile'),
    path('profile/', HealthProfileView.as_view(), name='get_health_profile'),
    path('profile/create', HealthProfileView.as_view(), name='create_health_profile'),
    path('profile/illness/add', IllnessView.as_view(), name='add_illness'),
    path('profile/illness/edit/<int:pk>/', IllnessView.as_view(), name='edit_illness'),
    path('profile/illness/delete/<int:pk>/', IllnessView.as_view(), name='delete_illness'),
]