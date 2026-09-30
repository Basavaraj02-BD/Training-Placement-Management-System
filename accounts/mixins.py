from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied


class RoleRequiredMixin(LoginRequiredMixin):
    """Allow logged-in users whose role is in allowed_roles (superusers always pass)."""
    allowed_roles = ('ADMIN', 'TRAINER')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if not (request.user.is_superuser or request.user.role in self.allowed_roles):
                raise PermissionDenied("You don't have permission to perform this action.")
        return super().dispatch(request, *args, **kwargs)


class AdminRequiredMixin(RoleRequiredMixin):
    """Admin-only: batch management, placements/company management."""
    allowed_roles = ('ADMIN',)
