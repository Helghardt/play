from rest_framework import serializers
from escrow.models import Escrow
from logging import getLogger

logger = getLogger('django')


class CreateEscrowSerializer(serializers.Serializer):
    destination = serializers.CharField(required=True)
    source = serializers.CharField(read_only=True)
    amount = serializers.CharField(required=True)
    currency = serializers.CharField(required=True)
    deposit_id = serializers.CharField(read_only=True)
    deposit_status = serializers.CharField(read_only=True)
    withdraw_id = serializers.CharField(read_only=True)
    withdraw_status = serializers.CharField(read_only=True)
    transfer_id = serializers.CharField(read_only=True)
    transfer_status = serializers.CharField(read_only=True)
    description = serializers.CharField(required=True)
    # expiry = serializers.CharField(required=True)
    # metadata = serializers.JSONField(required=False, allow_null=True)

    def create(self, validated_data: dict):
        create_data = validated_data.copy()
        instance = Escrow.objects.create(**create_data)

        # Create deposit on Rehive, for source, set to pending
        instance.create_tx(tx_type='deposit',
                           amount=create_data['amount'],
                           tag='source')

        # Execute payment processing

        # Update deposit on Rehive, for source
        instance.update_tx(tx_type='deposit',
                           status='Complete',
                           tx_code=instance.deposit_id)

        # # # Create withdraw on Rehive, for source
        instance.create_tx(tx_type='withdraw',
                           amount=instance.amount,
                           tag='source')

        # Create deposit on Rehive, for destination, set to pending
        instance.create_tx(tx_type='deposit',
                           amount=instance.amount,
                           tag='destination')

        return instance


class UpdateEscrowSerializer(serializers.Serializer):
    transfer_status = serializers.CharField(required=True)

    def update(self, instance, validated_data):

        instance.update_tx(tx_type='deposit',
                           status=validated_data['transfer_status'],
                           tx_code=instance.transfer_id)

        instance.transfer_status = validated_data['transfer_status']
        instance.save()

        return instance