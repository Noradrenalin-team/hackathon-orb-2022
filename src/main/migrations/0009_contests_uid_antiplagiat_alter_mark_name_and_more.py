# Generated by Django 4.1.3 on 2022-12-04 10:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_expert_login'),
    ]

    operations = [
        migrations.AddField(
            model_name='contests',
            name='uid_antiplagiat',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='mark',
            name='name',
            field=models.CharField(max_length=300),
        ),
        migrations.AlterField(
            model_name='mark',
            name='type',
            field=models.CharField(choices=[('video', 'Видео'), ('article', 'Статья'), ('downgrade', 'Штраф'), ('upgrade', 'Дополнительный балл')], max_length=100),
        ),
    ]