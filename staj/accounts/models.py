from django.contrib.auth.models import AbstractUser
from django.db import models
from accounts.managers import UserManager

ROLE_CHOICES = (
    ('admin', 'Admin'),
    ('viewer', 'Viewer'),
    ('author', 'Author'),
)


class Account(AbstractUser):
    email = models.EmailField(verbose_name='Электронная почта', unique=True, blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True, default='avatars/No_avatar.png')
    role = models.CharField(choices=ROLE_CHOICES, max_length=10, null=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'

    def __str__(self):
        return f'{self.email}'
