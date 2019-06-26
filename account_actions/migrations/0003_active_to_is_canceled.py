from django.db import migrations


def active_to_is_canceled(apps, schema_editor):
    Token = apps.get_model('account_actions', 'AccountActionToken')
    for token in Token.objects.all():
        token.is_canceled = not token.active
        token.save()


class Migration(migrations.Migration):

    dependencies = [
        ('account_actions', '0002_accountactiontoken_is_canceled'),
    ]

    operations = [
        migrations.RunPython(active_to_is_canceled, migrations.RunPython.noop),
    ]
