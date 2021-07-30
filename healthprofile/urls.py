from django.urls import path
from .views import CreateHealthProfile, GetHealthProfile


urlpatterns = [
    path('profile/', GetHealthProfile.as_view(), name='get_health_profile'),
    path('profile/create', CreateHealthProfile.as_view(), name='create_health_profile')
]