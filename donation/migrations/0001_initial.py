# Generated by Django 3.2 on 2021-08-10 11:33

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DonationRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('blood_group', models.CharField(choices=[('A+', 'Apositive'), ('A-', 'Anegative'), ('B+', 'Bpositive'), ('B-', 'Bnegative'), ('O+', 'Opositive'), ('O-', 'Onegative'), ('AB+', 'Abpositive'), ('AB-', 'Abnegative')], max_length=3)),
                ('quantity', models.IntegerField(default=0)),
                ('location', models.CharField(max_length=200)),
                ('time', models.DateTimeField(db_index=True, default=django.utils.timezone.now)),
            ],
        ),
    ]