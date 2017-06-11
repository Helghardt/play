from django.shortcuts import render
from config.views import CreateAPIView, GenericAPIView, RetrieveUpdateAPIView
from escrow.serializers import CreateEscrowSerializer, UpdateEscrowSerializer
from escrow.models import Escrow

# Create your views here.



class CreateEscrow(CreateAPIView):
    serializer_class = CreateEscrowSerializer

    def perform_create(self, serializer):
        serializer.save()

class UpdateEscrow(RetrieveUpdateAPIView):

    serializer_class = UpdateEscrowSerializer

    def get_object(self):
        transfer_id = self.kwargs.get('transfer_id')
        escrow = Escrow.objects.get(transfer_id=transfer_id)
        return escrow
