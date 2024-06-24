# Generated by Django 5.0.6 on 2024-06-07 09:14

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Order",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("customer_id", models.IntegerField()),
                ("order_date", models.DateField()),
                ("total_amount", models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name="OrderProduct",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("order_id", models.IntegerField()),
                ("product_id", models.IntegerField()),
                ("quantity", models.IntegerField()),
            ],
            options={
                "unique_together": {("order_id", "product_id")},
            },
        ),
    ]
