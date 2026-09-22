from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):
    dependencies = [
        ('store_app', '0012_materialtransaction_delivery_note_no'),
    ]

    operations = [
        migrations.AddField(
            model_name='materialtransaction',
            name='gate_pass_no',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.CreateModel(
            name='GatePass',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('movement_pass_no', models.CharField(max_length=50, unique=True)),
                ('pass_type', models.CharField(choices=[('Tool', 'Tools Gate Pass'), ('Material', 'Material Gate Pass')], max_length=20)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('created_by', models.CharField(blank=True, max_length=150, null=True)),
                ('employee_name', models.CharField(blank=True, max_length=150, null=True)),
                ('employee_id_designation', models.CharField(blank=True, max_length=200, null=True)),
                ('department', models.CharField(blank=True, max_length=150, null=True)),
                ('reason', models.CharField(blank=True, max_length=255, null=True)),
                ('destination', models.CharField(blank=True, max_length=255, null=True)),
                ('returnable', models.BooleanField(blank=True, null=True)),
                ('expected_return_date', models.DateField(blank=True, null=True)),
            ],
            options={'ordering': ['-created_at']},
        ),
        migrations.CreateModel(
            name='GatePassItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=255)),
                ('quantity', models.CharField(default='1', max_length=50)),
                ('serial_asset_no', models.CharField(blank=True, max_length=100, null=True)),
                ('gate_pass', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='store_app.gatepass')),
                ('material_transaction', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='gate_pass_items', to='store_app.materialtransaction')),
                ('tool_transaction', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='gate_pass_items', to='store_app.tooltransaction')),
            ],
            options={'ordering': ['id']},
        ),
    ]
