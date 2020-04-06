from django.conf import urls
from rest_framework.routers import SimpleRouter
from .views import CustomerViewSet, PaymentViewSet

router = SimpleRouter()

router.register(r'customers', CustomerViewSet, base_name='customers')
router.register(r'payments', PaymentViewSet, base_name='payments')

