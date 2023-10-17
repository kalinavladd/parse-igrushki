from typing import List, Optional
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.apps import apps
import factory
from factory.django import get_model


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = get_user_model()
        django_get_or_create = ('email')

    email = factory.Faker('email')
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        """Override the default ``_create`` with our custom call."""
        manager = cls._get_manager(model_class)
        return manager.create_user(*args, **kwargs)


class AdminUserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = get_user_model()
        django_get_or_create = ('email')

    email = factory.Faker('email')
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    permissions: Optional[List[str]] = None

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        """Override the default ``_create`` with our custom call."""
        manager = cls._get_manager(model_class)
        permissions = kwargs.pop('permissions')
        user = manager.create_user(*args, **kwargs, is_staff=True)
        if permissions:
            permission_models = []
            for permission in permissions:
                app_name, codename = permission.split('.')
                permission_models.append(
                    Permission.objects.get(
                        content_type__app_label=app_name,
                        codename=codename
                    ))
            user.user_permissions.set(permission_models)
        return user