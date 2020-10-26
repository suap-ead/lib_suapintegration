from django.utils.translation import gettext as _
from django.conf import settings
from django.dispatch import receiver
from django.db.models import Model, CharField, EmailField, BooleanField, DateTimeField, ForeignKey, CASCADE
from django.db.models.signals import post_save
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from social_django.models import UserSocialAuth


class AbstractSuapUser(AbstractUser):
    username = CharField(_('username'), max_length=150, unique=True)
    password = CharField(_('password'), max_length=128, null=True, blank=True)
    name = CharField(_('name'), max_length=255, null=True, blank=True)
    social_name = CharField(_('social name'), max_length=255, null=True, blank=True)
    email = EmailField(_('email address'), null=True, blank=True)
    scholar_email = EmailField(_('scholar email address'), null=True, blank=True)
    academic_email = EmailField(_('academic email address'), null=True, blank=True)
    campus = CharField(_('campus'), max_length=255, null=True, blank=True)
    is_staff = BooleanField(_('staff status'), default=False,
                            help_text=_('Designates whether the user can log into this admin site.'),)
    is_active = BooleanField(_('active'), default=True,
                             help_text=_('Designates whether this user should be treated as active.'
                                         ' Unselect this instead of deleting accounts.'),)
    created_at = DateTimeField(_('date created'), auto_now_add=True)
    changed_at = DateTimeField(_('date changed'), auto_now=True)

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'name']

    class Meta:
        ordering = ['name']
        abstract = True

    def __str__(self):
        return f'{self.name}'


class SuapUser(AbstractSuapUser):

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')
        ordering = ['name']
        abstract = False

    def __str__(self):
        return f'{self.name}'

    def save(self, *args, **kwargs):
        if self.name:
            splitted_name = self.name.split()
            self.first_name = ' '.join(splitted_name[:-1])
            self.last_name = splitted_name[-1] if len(splitted_name) > 1 else '.'
        super().save(*args, **kwargs)


class LoginHistory(Model):
    user = ForeignKey(get_user_model(), on_delete=CASCADE)
    login_at = DateTimeField(_('login at'), auto_now_add=True)
    ip = CharField(_('IP'), max_length=255)

    class Meta:
        verbose_name = _('User login history')
        verbose_name_plural = _('User logins history')
        ordering = ['-login_at']


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_socialauth_suap_user(sender, instance=None, created=False, **kwargs):
    if instance:
        UserSocialAuth.objects.update_or_create(user=instance, defaults={'provider': 'suap', 'uid': instance.username})
