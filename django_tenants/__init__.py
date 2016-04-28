from django.conf import settings
setattr(settings, 'TENANT_SESSION_KEY', 'tenant_schema')
setattr(settings, 'TENANT_SELECTION_METHOD', 'domain')
setattr(settings, 'TENANT_DATABASE', 'default')

default_app_config = 'django_tenants.apps.DjangoTenantsConfig'
