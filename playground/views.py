from django.shortcuts import render
from .tasks import notify_customers
# pylint: disable=no-member


# @transaction.atomic()  # all code runs inside transaction
def say_hello(request):
    notify_customers.delay('Hello Shakhzod!')
    return render(request, 'hello.html', {'name': 'Shakhzod'})
