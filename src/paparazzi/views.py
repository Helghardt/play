from collections import OrderedDict
from django.utils.translation import ugettext as _
from django.shortcuts import render
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework.reverse import reverse


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
                [(_('Register'), reverse('paparazzi-api:register',
                                         request=request,
                                         format=format)),
                 # (_('Login'), reverse('paparazzi-api:login',
                 #                      request=request,
                 #                      format=format)),
                 # (_('Logout'), reverse('paparazzi-api:logout',
                 #                       request=request,
                 #                       format=format)),
                 # (_('Change Password'), reverse('paparazzi-api:password_change',
                 #                                request=request,
                 #                                format=format)),
                 # (_('Reset Password'), reverse('paparazzi-api:password_reset',
                 #                               request=request,
                 #                               format=format)),
                 ]
            )},
        ])


def index(request):
    context_dict = {}

    return render(request, 'paparazzi/index.html', context=context_dict)
