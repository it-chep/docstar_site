from django.http import Http404, HttpResponseForbidden


class DoctorPermissionsMixin:
    def has_permissions(self):
        if self.request.user.is_authenticated:
            return self.get_object().email == self.request.user.email
        raise Http404

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permissions():
            raise Http404

        return super().dispatch(request, *args, **kwargs)


class MembersPermissionsMixin(DoctorPermissionsMixin):
    def has_permissions(self):
        return self.request.user.id in self.get_object().members.all()

