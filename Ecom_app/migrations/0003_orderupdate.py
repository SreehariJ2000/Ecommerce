# Generated by Django 4.2.1 on 2023-05-15 09:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Ecom_app', '0002_orders'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderUpdate',
            fields=[
                ('update_id', models.AutoField(primary_key=True, serialize=False)),
                ('order_id', models.IntegerField(default='')),
                ('update_desc', models.CharField(max_length=5000)),
                ('timestamp', models.DateField(auto_now_add=True)),
            ],
        ),
    ]