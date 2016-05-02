from django.conf import settings
from django.apps import apps as django_apps


class TenantSyncRouter(object):
    """
    A router to control which applications will be synced,
    depending if we are syncing the shared apps or the tenant apps.
    """

    def app_in_list(self, app_label, apps_list):
        """
        Is 'app_label' present in 'apps_list'?

        apps_list is either settings.SHARED_APPS or settings.TENANT_APPS, a
        list of app names.

        We check the presense of the app's name or the full path to the apps's
        AppConfig class.
        https://docs.djangoproject.com/en/1.8/ref/applications/#configuring-applications
        """
        appconfig = django_apps.get_app_config(app_label)
        appconfig_full_name = '{}.{}'.format(
            appconfig.__module__, appconfig.__class__.__name__)
        return (appconfig.name in apps_list) or (appconfig_full_name in apps_list)

    def db_for_read(self, model, **hints):
        if self.app_in_list(model._meta.app_label, settings.TENANT_APPS):
            return settings.TENANT_DATABASE
        return None

    def db_for_write(self, model, **hints):
        if self.app_in_list(model._meta.app_label, settings.TENANT_APPS):
            return settings.TENANT_DATABASE
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        # the imports below need to be done here else django <1.5 goes crazy
        # https://code.djangoproject.com/ticket/20704
        from django.db import DEFAULT_DB_ALIAS

        if self.app_in_list(app_label, settings.TENANT_APPS):
            return db == settings.TENANT_DATABASE

        elif self.app_in_list(app_label, settings.SHARED_APPS):
            return db == DEFAULT_DB_ALIAS

        print('Not migrating {0} to {1}'.format(app_label, db))
        return False
