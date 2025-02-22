# Generated by Django 4.2.19 on 2025-02-22 16:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Booking",
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
                ("customer_name", models.CharField(max_length=100)),
                (
                    "customer_gender",
                    models.CharField(
                        choices=[
                            ("MALE", "Male"),
                            ("FEMALE", "Female"),
                            ("OTHER", "Other"),
                        ],
                        default="MALE",
                        max_length=10,
                    ),
                ),
                (
                    "customer_id",
                    models.CharField(default="TEMP_ID", max_length=50, unique=True),
                ),
                (
                    "executive_choice",
                    models.CharField(
                        choices=[
                            ("BED_ONLY", "Bed Only"),
                            ("BED_BREAKFAST", "Bed and Breakfast"),
                            ("HALFBOARD", "Halfboard"),
                            ("FULLBOARD", "Fullboard"),
                        ],
                        default="BED_BREAKFAST",
                        max_length=20,
                    ),
                ),
                (
                    "customer_phone",
                    models.CharField(blank=True, max_length=15, null=True),
                ),
                ("check_in_date", models.DateField()),
                ("check_out_date", models.DateField()),
                ("guests", models.IntegerField()),
                (
                    "total_price",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=10, null=True
                    ),
                ),
                ("booking_date", models.DateTimeField(auto_now_add=True)),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("PENDING", "Pending"),
                            ("CONFIRMED", "Confirmed"),
                            ("CANCELLED", "Cancelled"),
                        ],
                        default="PENDING",
                        max_length=10,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Feature",
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
                ("name", models.CharField(max_length=50)),
                ("description", models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name="RoomPayment",
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
                ("amount", models.DecimalField(decimal_places=2, max_digits=10)),
                ("payment_date", models.DateTimeField(auto_now_add=True)),
                (
                    "payment_method",
                    models.CharField(
                        choices=[
                            ("CASH", "Cash"),
                            ("CARD", "Card"),
                            ("MPESA", "Mpesa"),
                        ],
                        max_length=10,
                    ),
                ),
                ("is_paid", models.BooleanField(default=False)),
                (
                    "booking",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="rooms.booking"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Room",
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
                ("room_number", models.CharField(max_length=10, unique=True)),
                (
                    "room_type",
                    models.CharField(
                        choices=[
                            ("SINGLE", "Single"),
                            ("DOUBLE", "Double"),
                            ("SUITE", "Suite"),
                        ],
                        max_length=10,
                    ),
                ),
                ("capacity", models.IntegerField()),
                (
                    "price_bed_breakfast",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=8, null=True
                    ),
                ),
                (
                    "price_halfboard",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=8, null=True
                    ),
                ),
                (
                    "price_fullboard",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=8, null=True
                    ),
                ),
                (
                    "price_per_night",
                    models.DecimalField(decimal_places=2, max_digits=8),
                ),
                ("description", models.TextField(blank=True, null=True)),
                (
                    "image",
                    models.ImageField(
                        blank=True,
                        default="default_room.jpg",
                        null=True,
                        upload_to="room_images/",
                    ),
                ),
                ("features", models.ManyToManyField(blank=True, to="rooms.feature")),
            ],
        ),
        migrations.AddField(
            model_name="booking",
            name="room",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="rooms.room"
            ),
        ),
    ]
