from django.urls import path
from .views import CreateHealthProfile, EditHealthProfile, GetHealthProfile


urlpatterns = [
    path('profile/edit/<int:pk>/', EditHealthProfile.as_view(), name='edit_health_profile'),
    path('profile/', GetHealthProfile.as_view(), name='get_health_profile'),
    path('profile/create', CreateHealthProfile.as_view(), name='create_health_profile'),

]