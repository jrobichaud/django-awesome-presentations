from django.db import migrations


def migrate(apps, schema_editor):
    kitten_model = apps.get_model('testing_migrations', 'Kitten')
    kitten_name_model = apps.get_model('testing_migrations', 'KittenName')

    for kitten in kitten_model.objects.all():
        kitten_name_model.objects.create(
            kitten=kitten,
            name=kitten.name,
        )


def migrate_reverse(apps, schema_editor):
    kitten_model = apps.get_model('testing_migrations', 'Kitten')

    for kitten in kitten_model.objects.all():
        kitten_name = kitten.kittenname_set.first()
        kitten.name = kitten_name.name if kitten_name else "anonymous"
        kitten.save()


class Migration(migrations.Migration):

    dependencies = [
        ('testing_migrations', '0004_kittenname'),
    ]

    operations = [
        migrations.RunPython(migrate, reverse_code=migrate_reverse)
    ]
