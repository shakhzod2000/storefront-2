from django.core.mail import send_mail, mail_admins, BadHeaderError, EmailMessage
from django.shortcuts import render
from templated_mail.mail import BaseEmailMessage
# pylint: disable=no-member


# @transaction.atomic()  # all code runs inside transaction
def say_hello(request):
    try:
        message = BaseEmailMessage(
            template_name='emails/hello.html',
            context={'name': 'Shakhzod'}
        )
        message.send(['john@storefront.com'])
        
        # message = EmailMessage('subject', 'message', 
        #                        'from@me.com', ['tosomeone@gmail.com'])
        # message.attach_file('playground/static/images/maldives.jpg')
        # message.send()
        
        # send_mail('subject', 'message', 'info@shakhzod.com', ['sshermatov50@gmail.com'])
        # mail_admins('subject', 'message', html_message='html message')
    except BadHeaderError:
        pass
    return render(request, 'hello.html', {'name': 'Shakhzod'})
