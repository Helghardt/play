from django.shortcuts import render
from config.views import CreateAPIView, GenericAPIView, RetrieveUpdateAPIView
from escrow.serializers import CreateEscrowSerializer, UpdateEscrowSerializer
from escrow.models import Escrow

# Create your views here.
from rest_framework import exceptions


class CreateEscrow(CreateAPIView):
    serializer_class = CreateEscrowSerializer

    def perform_create(self, serializer):
        serializer.save()

class UpdateEscrow(RetrieveUpdateAPIView):
    serializer_class = UpdateEscrowSerializer

    def get_object(self):
        transfer_id = self.kwargs.get('transfer_id')
        try:
            return Escrow.objects.get(transfer_id=transfer_id)
        except Escrow.DoesNotExist:
            raise exceptions.NotFound()
