# Generated by Django 3.2 on 2021-10-19 17:18

from django.db import migrations
from django.core.serializers import base, python
from django.core.management import call_command


# noinspection PyUnusedLocal
def load_fixture(apps, schema_editor):
    # Save the old _get_model() function
    # noinspection PyProtectedMember
    old_get_model = python._get_model

    # Define new _get_model() function here, which utilizes the apps argument to
    # get the historical version of a model. This piece of code is directly stolen
    # from django.core.serializers.python._get_model, unchanged. However, here it
    # has a different context, specifically, the apps variable.
    def _get_model(model_identifier):
        try:
            return apps.get_model(model_identifier)
        except (LookupError, TypeError):
            raise base.DeserializationError("Invalid model identifier: '%s'" % model_identifier)

    # Replace the _get_model() function on the module, so loaddata can utilize it.
    python._get_model = _get_model

    try:
        # Call loaddata command
        call_command('loaddata', 'auth_initial_data.json', app_label='core')
    finally:
        # Restore old _get_model() function
        python._get_model = old_get_model


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.RunPython(load_fixture)
    ]
