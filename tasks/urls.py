from django.urls import path, include
from rest_framework import routers
from .views import *
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView


router = routers.DefaultRouter()
router.register(r'tasks', TaskViewSet)

urlpatterns = [
    path('api/v1/', include(router.urls)),
    path('api/v1/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/v1/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/v1/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]