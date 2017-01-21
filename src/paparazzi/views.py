import requests

from collections import OrderedDict
from django.utils.translation import ugettext as _
from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.generics import GenericAPIView
from rest_framework.pagination import CursorPagination, PageNumberPagination
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.settings import api_settings
from paparazzi.models import Photo
from paparazzi.serializers import ListCreatePhotoSerializer

from django.conf import settings


@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def api_root(request, format=None):
    """
    ### API documentation for the Paparazzi.
    ---
    """
    return Response(
        [
            {_('Authentication'): OrderedDict(
                [
                    (_('Register'), reverse('rest_register',
                                            request=request,
                                            format=format)),
                    (_('Login'), reverse('rest_login',
                                         request=request,
                                         format=format)),
                    (_('Logout'), reverse('rest_logout',
                                          request=request,
                                          format=format)),
                    (_('Change Password'), reverse('rest_password_change',
                                                   request=request,
                                                   format=format)),
                    (_('Reset Password'), reverse('rest_password_reset',
                                                  request=request,
                                                  format=format)),
                    (_('Reset Password Confirm'), reverse('rest_password_reset_confirm',
                                                          request=request,
                                                          format=format)),
                    (_('User Details'), reverse('rest_user_details',
                                                request=request,
                                                format=format)),
                ]
            )},
            {_('Paparazzi'): OrderedDict(
                [
                    (_('Photos'), reverse('paparazzi-api:photos',
                                            request=request,
                                            format=format)),
                ]
            )},
        ])


class ResultsSetPagination(PageNumberPagination):
    page_size = 15
    page_size_query_param = 'page_size'
    max_page_size = 250

    def get_paginated_response(self, data):
        response = OrderedDict([
            ('count', self.page.paginator.count),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('results', data)
        ])

        return Response(OrderedDict([('status', 'success'), ('data', response)]))


# Example cursor pagination, not used atm due to having no 'page_size_query_param' or 'count' result
class LargeResultsSetPagination(CursorPagination):
    page_size = 50
    cursor_query_param = 'cursor'
    max_page_size = 500

    def get_paginated_response(self, data):
        response = OrderedDict([
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('results', data)
        ])

        return Response(OrderedDict([('status', 'success'), ('data', response)]))


class CreateModelMixin(object):
    """
    Create a model instance.
    """

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response({'status': 'success', 'data': serializer.data}, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save()

    def get_success_headers(self, data):
        try:
            return {'Location': data[api_settings.URL_FIELD_NAME]}
        except (TypeError, KeyError):
            return {}


class ListModelMixin(object):
    """
    List a queryset.
    """

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response({'status': 'success', 'data': serializer.data})


class RetrieveModelMixin(object):
    """
    Retrieve a model instance.
    """

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({'status': 'success', 'data': serializer.data})


class UpdateModelMixin(object):
    """
    Update a model instance.
    """

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response({'status': 'success', 'data': serializer.data})

    def perform_update(self, serializer):
        serializer.save()

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)


class DestroyModelMixin(object):
    """
    Destroy a model instance.
    """

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_destroy(serializer)
        return Response({'status': 'success'})

    def perform_destroy(self, serializer):
        serializer.destroy()


class CreateAPIView(CreateModelMixin,
                    GenericAPIView):
    """
    Concrete view for creating a model instance.
    """

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class ListAPIView(ListModelMixin,
                  GenericAPIView):
    """
    Concrete view for listing a queryset.
    """

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class ListCreateAPIView(ListModelMixin,
                        CreateModelMixin,
                        GenericAPIView):
    """
    Concrete view for listing a queryset or creating a model instance.
    """

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class RetrieveUpdateAPIView(RetrieveModelMixin,
                            UpdateModelMixin,
                            GenericAPIView):
    """
    Concrete view for retrieving, updating a model instance.
    """

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class RetrieveUpdateDestroyAPIView(RetrieveModelMixin,
                                   UpdateModelMixin,
                                   DestroyModelMixin,
                                   GenericAPIView):
    """
    Concrete view for retrieving, updating, deleting model instance.
    """

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class RetrieveAPIView(RetrieveModelMixin,
                      GenericAPIView):
    """
    Concrete view for retrieving a model instance.
    """

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


class ListCreatePhoto(ListCreateAPIView):
    """
    ### List create photo

    """
    serializer_class = ListCreatePhotoSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        url = 'https://westus.api.cognitive.microsoft.com/face/v1.0/detect?returnFaceId=true&returnFaceLandmarks=true&returnFaceAttributes=age,gender,headPose,smile,facialHair,glasses'
        data = open(getattr(settings, 'PROJECT_DIR') + '/var/www/media/users/1/images/test.jpg', 'rb').read()
        res = requests.post(
            url=url,
            data=data,
            headers={
                'Content-Type': 'application/octet-stream',
                'Ocp-Apim-Subscription-Key': getattr(settings, 'MICROSOFT_FACE_API_KEY')
            }
        )
        faceId = res.json()[0]['faceId']
        print(faceId)
        # return res

        return Photo.objects.filter(user=self.request.user)