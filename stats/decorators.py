from django.core.exceptions import PermissionDenied
from portal.models import User
from portal.choices import ELECTION_COMMISSION
from functools import wraps


def user_is_admin(function):
    @wraps(function)
    def wrap(request, *args, **kwargs):
        d = dict()
        try:
            if request.session['user']['is_authenticated']:
                d['is_authenticated'] = True
            else:
                d['is_authenticated'] = False
        except (KeyError, AttributeError) as e:
            d['is_authenticated'] = False
        if d['is_authenticated']:
            user = User.objects.get(email=request.session['user']['email'])
            if user.junta.role == ELECTION_COMMISSION:
                return function(request, *args, **kwargs)
            else:
                raise PermissionDenied
        else:
            raise PermissionDenied

    return wrap
