from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import AdminPasswordChangeForm
from django.utils.translation import gettext_lazy as _
from django.shortcuts import get_object_or_404, redirect
from django.urls import path, reverse
from django.contrib import messages
from django.template.response import TemplateResponse
from django.utils.html import format_html
from .models import User


class UserAdmin(BaseUserAdmin):
    """Define the admin page for the custom User model."""
    ordering = ['id']
    list_display = ['email', 'name', 'is_staff', 'is_active', 'change_password_button']
    fieldsets = (
        (None, {'fields': ('email', 'password', 'name')}),
        (
            _('Permissions'),
            {
                'fields': (
                    'is_active',
                    'is_staff',
                    'is_superuser',
                )
            }
        ),
        (_('Important dates'), {'fields': ('last_login',)}),
    )
    readonly_fields = ['last_login']
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email',
                'name',
                'password1',
                'password2',
                'is_active',
                'is_staff',
                'is_superuser',
            )
        }),
    )

    def get_urls(self):
        """Add custom URLs for changing passwords."""
        urls = super().get_urls()
        custom_urls = [
            path('<id>/change-password/', self.admin_site.admin_view(self.change_password), name='user_change_password'),
        ]
        return custom_urls + urls

    def change_password(self, request, id):
        """Custom view for changing a user's password."""
        user = get_object_or_404(User, pk=id)

        if request.method == 'POST':
            form = AdminPasswordChangeForm(user, request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, f"Password for {user.email} has been updated.")
                return redirect(reverse('admin:user_user_changelist'))  # Redirect to the user list after success
        else:
            form = AdminPasswordChangeForm(user)

        context = {
            'title': f'Change Password for {user.email}',
            'form': form,
            'user': user,
            'opts': self.model._meta,
            'original': user,
        }
        return TemplateResponse(
            request,
            'admin/auth/user/change_password.html',
            context,
        )

    def change_password_button(self, obj):
        """Add a 'Change Password' button in the user list."""
        # Hide the button if the logged-in user matches the listed user
        if self.request.user == obj:
            return "—"  # Show a dash instead of a button for the logged-in user
        return format_html(
            '<a class="button" href="{}/change-password/">Change Password</a>',
            obj.id,
        )
    change_password_button.short_description = 'Change Password'

    def get_list_display(self, request):
        """Override to pass the request object for use in change_password_button."""
        self.request = request
        return super().get_list_display(request)


admin.site.register(User, UserAdmin)
