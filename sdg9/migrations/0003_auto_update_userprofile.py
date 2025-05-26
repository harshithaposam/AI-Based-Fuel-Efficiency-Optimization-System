from django.db import migrations, models

def update_user_profiles(apps, schema_editor):
    UserProfile = apps.get_model('sdg9', 'UserProfile')
    UserProfile.objects.update(vehicle_model=None)

class Migration(migrations.Migration):

    dependencies = [
        ('sdg9', '0002_usercredit'),
    ]

    operations = [
        migrations.RunPython(update_user_profiles),
    ]
