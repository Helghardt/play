from builtins import getattr
import os
import requests
import json
from decimal import Decimal
import datetime
from django.db import models
from logging import getLogger
import datetime
from django.utils.timezone import (
    utc, now
)
from django.utils.translation import ugettext_lazy as _

logger = getLogger('django')

# Money field
class MoneyField(models.DecimalField):
    """
    Decimal Field with hardcoded precision of 28 and a scale of 18.
    """

    def __init__(self, verbose_name=None, name=None, max_digits=28, decimal_places=18, **kwargs):
        super(MoneyField, self).__init__(verbose_name, name, max_digits, decimal_places, **kwargs)


STATUS = (
    ('Pending', 'Pending'),
    ('Complete', 'Complete'),
    ('Failed', 'Failed'),
    ('Deleted', 'Deleted'),
    ('Cancelled', 'Cancelled'),
    ('Expired', 'Expired'),
    ('Reversed', 'Reversed'),
    ('Escrowed', 'Escrowed'),
    ('Released', 'Released'),
    ('Disputed', 'Disputed'),
    ('Expired', 'Expired')
)


# Escrow
class Escrow(models.Model):
    company = models.CharField(max_length=250, blank=True, null=True)
    source = models.CharField(max_length=250, blank=True, null=True)
    destination = models.CharField(max_length=250, blank=True, null=True)  #
    amount = MoneyField(default=Decimal(0))
    currency = models.CharField(max_length=12, null=True, blank=True)
    description = models.TextField(max_length=500, null=True, blank=True, default='')
    expiry = models.DateTimeField(blank=True, null=True)
    # metadata = JSONField(null=True, blank=True, default=dict)
    deposit_id = models.CharField(max_length=64, null=True, blank=True)
    deposit_status = models.CharField(max_length=24, choices=STATUS, default='Pending', null=True, blank=True)
    withdraw_id = models.CharField(max_length=64, null=True, blank=True)
    withdraw_status = models.CharField(max_length=24, choices=STATUS, default='Pending', null=True, blank=True)
    transfer_id = models.CharField(max_length=64, null=True, blank=True)
    transfer_status = models.CharField(max_length=24, choices=STATUS, default='Pending', null=True, blank=True)
    created = models.DateTimeField(db_index=True, )
    updated = models.DateTimeField(default=now)

    def __str__(self):
        return self.source

    def save(self, *args, **kwargs):
        if not self.id:  # On create
            self.created = datetime.datetime.now(tz=utc)

        self.updated = datetime.datetime.now(tz=utc)

        token = os.environ.get('REHIVE_USER_TOKEN', '')
        headers = {'Authorization': 'Token ' + token}
        url = 'https://rehive.com/api/3/user/'
        r = requests.get(url, headers=headers)

        data = json.loads(r.text)

        self.company = data['data']['company']
        self.source = data['data']['identifier']

        return super(Escrow, self).save(*args, **kwargs)

    def create_tx(self, tx_type, amount, tag):
        """
        Create transaction on Rehive
        """

        if tag == 'source':
            user = self.source
            if tx_type == 'deposit':
                confirm_on_create = False
            else:
                confirm_on_create = True
        else:
            user = self.destination
            confirm_on_create = False

        token = os.environ.get('REHIVE_ADMIN_TOKEN', '')
        headers = {'Authorization': 'Token ' + token}
        url = 'https://rehive.com/api/3/admin/transactions/' + tx_type + '/'
        data = {"user": user,
                "amount": amount,
                "confirm_on_create": confirm_on_create}

        try:
            r = requests.post(url, json=data, headers=headers)
            res = json.loads(r.text)

            if r.status_code == 201:
                data = res['data']
                if tx_type == 'deposit':
                    if tag == 'source':
                        self.deposit_id = data['tx_code']
                        self.deposit_status = 'Pending'
                    else:
                        self.transfer_id = data['tx_code']
                        self.transfer_status = 'Pending'
                else:
                    if tag == 'source':
                        self.withdraw_id = data['tx_code']
                        self.withdraw_status = 'Complete'
                self.save()
                return self
            else:
                if hasattr(res, 'message'):
                    raise Exception(res['message'])
                raise Exception(_('Connection error.'))

        except (requests.exceptions.RequestException, requests.exceptions.MissingSchema) as e:
            raise Exception(_('Connection error.'))

    def update_tx(self, tx_type, status, tx_code):
        """
        Update transaction on Rehive
        """

        token = os.environ.get('REHIVE_ADMIN_TOKEN', '')
        headers = {'Authorization': 'Token ' + token}
        url = 'https://rehive.com/api/3/admin/transactions/' + tx_code + '/'
        data = {"status": status}

        try:
            r = requests.put(url, json=data, headers=headers)
            res = json.loads(r.text)

            if r.status_code == 200:
                if tx_type == 'deposit':
                    self.deposit_status = status
                elif tx_type == 'withdraw':
                    self.withdraw_status = status
                else:
                    self.transfer_status = status
                self.save()
                return self
            else:
                if hasattr(res, 'message'):
                    raise Exception(res['message'])
                raise Exception(_('Connection error.'))

        except (requests.exceptions.RequestException, requests.exceptions.MissingSchema) as e:
            raise Exception(_('Connection error.'))
