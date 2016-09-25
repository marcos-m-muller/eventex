from django.conf import settings
from django.contrib import messages
from django.core import mail
from django.http import Http404
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.template.loader import render_to_string
from eventex.subscriptions.forms import SubscriptionForm
import hashlib

from eventex.subscriptions.models import Subscription


def subscribe(request):
    if request.method == 'POST':
        return create(request)
    else:
        return new(request)

def create(request):
    form = SubscriptionForm(request.POST)

    if not form.is_valid():
        return render(request, 'subscription_form.html', {'form': form})

    subscription = Subscription.objects.create(**form.cleaned_data)
    subscription.hashed_pk = hashlib.md5(str(subscription.pk).encode('utf-8')).hexdigest()
    subscription.save()

    _send_mail('Confirmação de inscrição',
              settings.DEFAULT_FROM_EMAIL,
              subscription.email,
              'subscription_email.txt',
               {'subscription':subscription})

    return HttpResponseRedirect('/inscricao/{}/'.format(subscription.hashed_pk))


def new(request):
    context = {'form': SubscriptionForm()}
    return render(request, 'subscription_form.html',context)


def detail(request, id):
    try:
        subscription = Subscription.objects.get(hashed_pk=id)
    except Subscription.DoesNotExist:
        raise Http404

    # subscription = Subscription(name='Marcos Moreira Müller', phone='21982306271', email='marcos.m.muller@gmail.com', cpf='10707955777')
    return render(request, 'subscription_detail.html', {'subscription': subscription})


def _send_mail(subject, from_, to, template_name, context):
    body = render_to_string(template_name, context)
    mail.send_mail(subject, body, from_, [from_, to])