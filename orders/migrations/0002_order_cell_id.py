from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("orders", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="order",
            name="cell_id",
            field=models.PositiveIntegerField(default=1),
            preserve_default=False,
        ),
    ]
