from django.dispatch import receiver
from store.signals import order_created
from store.models import Order


@receiver(order_created)
def on_order_created(sender, **kwargs):
    # Order.objects.create(user=kwargs['instance'])
    print(f'Order created: {kwargs['order']}')
