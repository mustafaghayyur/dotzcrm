from django.db import models
# from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils import timezone
from django.contrib.auth.models import UserManager, PermissionsMixin

# Create your models here.

class User(AbstractBaseUser, PermissionsMixin):
    """
        We will do our best not to modify columns already set in Django.
        Only column additions.
    """
    username_validator = UnicodeUsernameValidator()
    username = models.CharField(
        _("username"),
        max_length=150,
        unique=True,
        help_text=_(
            "Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."
        ),
        validators=[username_validator],
        error_messages={
            "unique": _("A user with that username already exists."),
        },
    )
    first_name = models.CharField(_("preferred first name"), max_length=150, blank=True)
    last_name = models.CharField(_("preferred last name"), max_length=150, blank=True)
    email = models.EmailField(_("email address"), blank=True)
    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can be a Staff Member."),
    )
    user_level = models.SmallIntegerField(
        _("access level of user"),
        default=1, 
        db_default=1  # 1 = memeber -> 9 = most senior administrator
    )
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    delete_time = models.DateTimeField(null=True, blank=True)
    objects = UserManager()
    EMAIL_FIELD = "email"
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    class Meta:
        db_table = 'auth_user'
        verbose_name = _("user")
        verbose_name_plural = _("users")

class UserProfile(models.Model):
    """
        Extension of the User model, mean for the user profile section.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    legal_first_name = models.CharField(max_length=150, blank=True, null=True)
    legal_last_name = models.CharField(max_length=150, blank=True, null=True)
    office_phone = models.CharField(max_length=15, blank=True, null=True)
    office_ext = models.CharField(max_length=10, blank=True, null=True)
    cell_phone = models.CharField(max_length=15, blank=True, null=True)
    home_phone = models.CharField(max_length=15, blank=True, null=True)
    office_location = models.CharField(max_length=250, blank=True, null=True)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    delete_time = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f'{self.legal_first_name} {self.legal_last_name} [{self.user.username}]'

class UserSettings(models.Model):
    """
        We will keep this for future feature development.
        User model's user_setting has limits on its size. 
        This model can be used more freely.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    settings = models.JSONField(null=True, blank=True)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    delete_time = models.DateTimeField(null=True, blank=True)

class Department(models.Model):
    """
        Departments, can be nested.
    """
    name = models.CharField(max_length=70)
    description = models.CharField(max_length=1000)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    delete_time = models.DateTimeField(null=True, blank=True)


class UserToDepartment(models.Model):
    """
        User's associent with departments. Can be M2M.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    create_time = models.DateTimeField(auto_now_add=True)
    delete_time = models.DateTimeField(null=True, blank=True)

class DepartmentHead(models.Model):
    """
        Assigns head(s) to departments. Can be M2M.
    """
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    create_time = models.DateTimeField(auto_now_add=True)
    delete_time = models.DateTimeField(null=True, blank=True)

class UserReportsTo(models.Model):
    """
        User's boss. Can be M2M.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    reports_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reports_to')
    create_time = models.DateTimeField(auto_now_add=True)
    delete_time = models.DateTimeField(null=True, blank=True)
    