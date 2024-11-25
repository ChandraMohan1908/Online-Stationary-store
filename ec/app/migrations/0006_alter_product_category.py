# Generated by Django 5.1.1 on 2024-09-27 11:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_alter_product_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.CharField(choices=[('FR', 'Dried Fruit Snacks'), ('NS', 'Nut and Seed Snacks'), ('WG', 'Whole Grain Snacks'), ('VS', 'Veggie Snacks'), ('PS', 'Protein Snacks'), ('SB', 'Snack Bars'), ('GF', 'Gluten-Free Snacks'), ('SS', 'Sweet Snacks')], max_length=2),
        ),
    ]
