from rest_framework.routers import DefaultRouter
from .views import CustomerViewSet, ContactViewSet, DealViewSet, TaskViewSet

router = DefaultRouter()
router.register('customers', CustomerViewSet)
router.register('contacts', ContactViewSet)
router.register('deals', DealViewSet)
router.register('tasks', TaskViewSet)

urlpatterns = router.urls
