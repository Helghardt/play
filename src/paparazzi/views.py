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
        ])
