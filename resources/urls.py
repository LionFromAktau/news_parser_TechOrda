from rest_framework.routers import DefaultRouter
from rest_framework.urls import path
from . import views

router = DefaultRouter()
router.register('resources', views.ResourceViewSet)
router.register('items', views.ItemViewSet)
urlpatterns = router.urls