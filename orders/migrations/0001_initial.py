# Generated by Django 4.2 on 2025-04-13 15:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('payments', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('order_id', models.CharField(default=uuid.uuid4, editable=False, max_length=20, primary_key=True, serialize=False)),
                ('order_status', models.CharField(choices=[('P', 'Pending'), ('Pr', 'Processing'), ('S', 'Shipped'), ('D', 'Delivered'), ('C', 'Cancelled')], default='P', max_length=2)),
                ('order_date', models.DateTimeField(auto_now=True)),
                ('order_update_date', models.DateTimeField(auto_now_add=True)),
                ('address', models.CharField(max_length=400)),
                ('postal_code', models.CharField(max_length=256)),
                ('payment_status', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='payments.paymentmodel')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
