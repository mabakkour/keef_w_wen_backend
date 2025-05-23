# Generated by Django 5.2 on 2025-04-27 16:08

import datetime
import django.contrib.postgres.fields
import django.db.models.deletion
import django.utils.timezone
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('latitude', models.FloatField()),
                ('longitude', models.FloatField()),
                ('timestamp', models.DateTimeField(auto_now=True)),
                ('accuracy', models.FloatField(blank=True, null=True)),
                ('source', models.CharField(blank=True, max_length=100, null=True)),
            ],
            options={
                'verbose_name': 'Location',
                'verbose_name_plural': 'Locations',
            },
        ),
        migrations.CreateModel(
            name='AppUser',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(max_length=150, primary_key=True, serialize=False, unique=True)),
                ('fullname', models.CharField(max_length=200)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('bio', models.TextField(blank=True)),
                ('mobile_number', models.CharField(blank=True, max_length=8)),
                ('profile_picture', models.ImageField(blank=True, null=True, upload_to='profile_pictures/')),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now)),
                ('last_login', models.DateTimeField(blank=True, null=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
                ('location', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='users', to='core.location')),
            ],
            options={
                'verbose_name': 'User',
                'verbose_name_plural': 'Users',
            },
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=200)),
                ('thumbnail', models.ImageField(blank=True, null=True, upload_to='thumbnails/')),
                ('description', models.TextField()),
                ('rating', models.FloatField()),
                ('is_private', models.BooleanField(default=False, verbose_name='Private event')),
                ('needs_id', models.BooleanField(default=False, verbose_name='Identification')),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now)),
                ('date_start', models.DateTimeField()),
                ('date_closed', models.DateTimeField()),
                ('date_ended', models.DateTimeField(default=datetime.datetime(2100, 1, 1, 0, 0))),
                ('seats', models.IntegerField()),
                ('price', models.FloatField()),
                ('open_status', models.BooleanField(default=True, verbose_name='Event open')),
                ('tags', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=50), blank=True, default=list, size=None)),
                ('host_owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='event', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='EventImage',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('image', models.ImageField(upload_to='events_images/')),
                ('date_uploaded', models.DateTimeField(default=django.utils.timezone.now)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='event_images', to='core.event')),
            ],
            options={
                'verbose_name': 'Event Image',
                'verbose_name_plural': 'Event Images',
            },
        ),
        migrations.AddField(
            model_name='event',
            name='images',
            field=models.ManyToManyField(blank=True, related_name='event_images', to='core.eventimage'),
        ),
        migrations.AddField(
            model_name='event',
            name='location',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='events', to='core.location'),
        ),
        migrations.CreateModel(
            name='Participant',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('is_host', models.BooleanField(default=False)),
                ('is_owner', models.BooleanField(default=False)),
                ('date_participated', models.DateTimeField(default=django.utils.timezone.now)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='participants', to='core.event')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='EventInteraction',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('liked', models.BooleanField(default=False)),
                ('saved', models.BooleanField(default=False)),
                ('date_interacted', models.DateTimeField(default=django.utils.timezone.now)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='event_interactions', to='core.event')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Event Interaction',
                'verbose_name_plural': 'Event Interactions',
                'unique_together': {('user', 'event')},
            },
        ),
        migrations.CreateModel(
            name='UserFollow',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('date_followed', models.DateTimeField(default=django.utils.timezone.now)),
                ('follower', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='followers', to=settings.AUTH_USER_MODEL)),
                ('following', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='following', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'User Interaction',
                'verbose_name_plural': 'User Interactions',
                'unique_together': {('follower', 'following')},
            },
        ),
    ]
