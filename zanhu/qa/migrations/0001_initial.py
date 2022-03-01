# Generated by Django 3.1.5 on 2021-01-19 05:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import markdownx.models
import taggit.managers
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('taggit', '0003_taggeditem_add_unique_index'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, unique=True, verbose_name='标题')),
                ('slug', models.SlugField(blank=True, max_length=80, null=True, verbose_name='(URL)别名')),
                ('status', models.CharField(choices=[('O', 'Open'), ('C', 'Close'), ('D', 'Draft')], default='O', max_length=1, verbose_name='问题状态')),
                ('content', markdownx.models.MarkdownxField(verbose_name='内容')),
                ('has_answer', models.BooleanField(default=False, verbose_name='接受回答')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('tags', taggit.managers.TaggableManager(help_text='多个标签使用,（英文）隔开', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='标签')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='q_author', to=settings.AUTH_USER_MODEL, verbose_name='提问者')),
            ],
            options={
                'verbose_name': '问题',
                'verbose_name_plural': '问题',
                'ordering': ('-created_at',),
            },
        ),
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('uuid_id', models.UUIDField(default=uuid.UUID('0d7bbc70-7802-4335-aaac-f0875eab45ce'), editable=False, primary_key=True, serialize=False)),
                ('content', markdownx.models.MarkdownxField(verbose_name='内容')),
                ('is_answer', models.BooleanField(default=False, verbose_name='回答是否被接受')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='qa.question', verbose_name='问题')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='a_author', to=settings.AUTH_USER_MODEL, verbose_name='回答者')),
            ],
            options={
                'verbose_name': '回答',
                'verbose_name_plural': '回答',
                'ordering': ('-is_answer', '-created_at'),
            },
        ),
        migrations.CreateModel(
            name='Vote',
            fields=[
                ('uuid_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('value', models.BooleanField(default=True, verbose_name='赞同或反对')),
                ('object_id', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='votes_on', to='contenttypes.contenttype')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='qa_vote', to=settings.AUTH_USER_MODEL, verbose_name='用户')),
            ],
            options={
                'verbose_name': '投票',
                'verbose_name_plural': '投票',
                'unique_together': {('user', 'content_type', 'object_id')},
                'index_together': {('content_type', 'object_id')},
            },
        ),
    ]