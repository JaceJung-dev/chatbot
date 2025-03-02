from django.contrib import admin
from .models import User
from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    model = User
    list_display = ["email", "first_name", "last_name", "is_staff"]
    search_fields = ("email", "first_name", "last_name")
    ordering = ("email",)

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal Info", {"fields": ("first_name", "last_name")}),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2"),
            },
        ),
    )

    # 기본적으로 username 기반의 인증을 email로 변경
    add_form_template = None
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()
