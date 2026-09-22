from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('store_app', '0011_tool_status_changed_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='materialtransaction',
            name='delivery_note_no',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Delivery Note / PO No'),
        ),
    ]
