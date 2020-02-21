from django.core.exceptions import PermissionDenied
from portal.models import User, Candidate
from portal.choices import CANDIDATE
from functools import wraps


def user_has_role(role, pk=0):
    def decorator(function):
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
                if user.junta.role == role:
                    if role == CANDIDATE:
                        if user.junta.candidate.all()[0] == Candidate.objects.get(pk=pk):
                            return function(request, *args, **kwargs)
                        else:
                            print(pk, user.junta.candidate.all()[0].pk, pk == user.junta.candidate.all()[0].pk)
                            raise PermissionDenied
                    else:
                        return function(request, *args, **kwargs)
                else:
                    print("role", user.junta.role)
                    raise PermissionDenied
            else:
                raise PermissionDenied

        return wrap

    return decorator
