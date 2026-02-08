from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin


class IsUserOwnerOfModelMixin(UserPassesTestMixin, LoginRequiredMixin):
    def test_func(self):

        if self.request.user.is_authenticated:
            obj_user = self.get_object().user
            return self.request.user == obj_user
        else:
            return False
