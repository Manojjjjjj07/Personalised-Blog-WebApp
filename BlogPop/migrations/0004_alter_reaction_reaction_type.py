# Generated by Django 5.1.1 on 2025-01-07 07:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BlogPop', '0003_remove_post_claps_remove_post_likes_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reaction',
            name='reaction_type',
            field=models.CharField(choices=[('like', 'Like'), ('love', 'Love'), ('dis', 'Dislike')], max_length=10),
        ),
    ]
