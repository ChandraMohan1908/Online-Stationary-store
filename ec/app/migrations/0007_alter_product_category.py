# Generated by Django 5.1.1 on 2024-09-27 13:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_alter_product_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.CharField(choices=[('AR', 'Atta, Rice, Dal'), ('OG', 'Oil, Ghee'), ('DB', 'Dairy, Bakery'), ('PS', 'Pet Supplies'), ('SS', 'Spices, Salt, Sugar'), ('DF', 'Dry Fruits, Nuts, Seeds'), ('BS', 'Biscuits, Chips, Namkeens'), ('BE', 'Breakfast Essentials'), ('BC', 'Body, Skincare'), ('BG', 'Beauty, Grooming'), ('OC', 'Oral Care'), ('BA', 'Baby Care'), ('HW', 'Hygiene, Wellness'), ('LD', 'Laundry, Dishwash'), ('HC', 'Household, Cleaning'), ('HK', 'Home, Kitchen')], max_length=2),
        ),
    ]
