# Generated by Django 4.2.5 on 2023-10-18 07:20

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("myapp", "0006_alter_product_product_image_link"),
    ]

    operations = [
        migrations.AlterField(
            model_name="product",
            name="product_image_link",
            field=models.CharField(default="assets/img/", max_length=255),
        ),
    ]
