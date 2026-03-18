from django.db import migrations, models
import django.core.validators
import django.db.models.deletion


def set_house_from_room(apps, schema_editor):
    Review = apps.get_model('reviews', 'Review')
    for review in Review.objects.select_related('room').all():
        if review.room_id:
            review.house_id = review.room.house_id
            review.save(update_fields=['house'])


class Migration(migrations.Migration):

    dependencies = [
        ('houses', '0003_remove_room_picture'),
        ('reviews', '0003_alter_review_reviewer'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='house',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='houses.house'),
        ),
        migrations.RunPython(set_house_from_room, migrations.RunPython.noop),
        migrations.AlterField(
            model_name='review',
            name='house',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='houses.house'),
        ),
        migrations.AlterField(
            model_name='review',
            name='rating',
            field=models.PositiveSmallIntegerField(default=5, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)]),
        ),
    ]
