# Generated by Django 4.1.1 on 2022-09-06 08:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=32)),
                ('price', models.DecimalField(decimal_places=2, max_digits=5)),
                ('pub_date', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=32)),
                ('password', models.CharField(max_length=32)),
                ('user_type', models.IntegerField(choices=[(1, '超级用户'), (2, '普通用户'), (3, '二笔用户')])),
            ],
        ),
        migrations.CreateModel(
            name='UserToken',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', models.CharField(max_length=64)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='app.user')),
            ],
        ),
    ]
