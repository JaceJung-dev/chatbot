# Generated by Django 4.2 on 2025-03-02 14:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('chatroom', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BotResponse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user_message', models.TextField()),
                ('bot_message', models.TextField()),
                ('chatroom', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bot_response', to='chatroom.chatroom')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
