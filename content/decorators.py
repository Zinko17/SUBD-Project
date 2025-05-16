from functools import wraps
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import redirect

from django.http import HttpResponseRedirect

def position_required(*allowed_positions, login_url='login'):
    def decorator(view_func):
        @wraps(view_func)
        @login_required(login_url=login_url)
        def _wrapped(request, *args, **kwargs):
            try:
                emp = request.user.employee_profile
            except Exception:
                messages.error(request, "У вас нет профиля сотрудника.")
                return redirect(login_url)

            pos = emp.positionid.positionname

            if pos in allowed_positions:
                return view_func(request, *args, **kwargs)

            messages.error(request, "У вас нет прав доступа к этой функции.")
            # Попробовать вернуться на предыдущую страницу, иначе на home
            referer = request.META.get('HTTP_REFERER', None)
            if referer:
                return HttpResponseRedirect(referer)
            return redirect('home')
        return _wrapped
    return decorator

