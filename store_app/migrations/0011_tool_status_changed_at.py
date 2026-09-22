from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):
    dependencies = [
        ('store_app', '0010_staff_is_deleted'),
    ]

    operations = [
        migrations.AddField(
            model_name='tool',
            name='status_changed_at',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Status Date'),
        ),
    ]
