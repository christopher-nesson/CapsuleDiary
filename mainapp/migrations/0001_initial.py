# Generated by Django 3.1.5 on 2021-01-07 02:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DayBook',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('motif', models.CharField(max_length=30, verbose_name='日记本主题')),
                ('describe', models.CharField(blank=True, max_length=200, null=True, verbose_name='日记本描述')),
                ('img', models.ImageField(blank=True, null=True, upload_to='cover/', verbose_name='封面')),
                ('create_time', models.DateField(auto_now_add=True, verbose_name='创建时间')),
                ('expiration_time', models.DateField(verbose_name='过期时间')),
                ('jurisdiction', models.CharField(choices=[('0', '所有人可见'), ('1', '仅自己可见')], default='0', max_length=1, verbose_name='可见管理')),
            ],
        ),
        migrations.CreateModel(
            name='Diary',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(verbose_name='日记内容')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('importance', models.BooleanField(default=False, verbose_name='重要日记')),
                ('daybook', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.daybook', verbose_name='所属日记本')),
            ],
        ),
        migrations.CreateModel(
            name='Topic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=30, verbose_name='话题标题')),
                ('img', models.ImageField(default='topic/default.png', upload_to='topic/', verbose_name='话题配图')),
                ('info', models.CharField(blank=True, max_length=100, null=True, verbose_name='话题描述')),
                ('create_time', models.DateField(auto_now_add=True, verbose_name='发布时间')),
            ],
        ),
        migrations.CreateModel(
            name='ImageDiary',
            fields=[
                ('diary_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='mainapp.diary')),
                ('image', models.ImageField(upload_to='imagediary/', verbose_name='配图')),
            ],
            bases=('mainapp.diary',),
        ),
        migrations.AddField(
            model_name='diary',
            name='topic',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='mainapp.topic', verbose_name='话题'),
        ),
    ]
