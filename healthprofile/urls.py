from django.urls import path
from .views import HealthProfileViews, IllnessViews


urlpatterns = [
    path('profile/edit/<int:pk>/', HealthProfileViews.as_view(), name='edit_health_profile'),
    path('profile/', HealthProfileViews.as_view(), name='get_health_profile'),
    path('profile/create', HealthProfileViews.as_view(), name='create_health_profile'),
    path('profile/illness/add', IllnessViews.as_view(), name='add_illness'),
    path('profile/illness/edit/<int:pk>/', IllnessViews.as_view(), name='edit_illness'),
    path('profile/illness/delete/<int:pk>/', IllnessViews.as_view(), name='delete_illness'),
]