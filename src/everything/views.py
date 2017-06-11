from config.views import ListAPIView, CreateAPIView, ResultsSetPagination, ListCreateAPIView
from everything.serlializers import CreateLogSerializer, ListLogSerializer, ListCreateImageSerializer
from everything.models import Log, Image


class CreateLog(CreateAPIView):
    serializer_class = CreateLogSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ListLog(ListAPIView):

    pagination_class = ResultsSetPagination
    serializer_class = ListLogSerializer

    def get_queryset(self):
        query_set = Log.objects.filter(user=self.request.user)

        return query_set


class ListCreateImage(ListCreateAPIView):
    serializer_class = ListCreateImageSerializer

    def perform_create(self, serializer):
        serializer.save()

    def get_queryset(self):
        return Image.objects.all()