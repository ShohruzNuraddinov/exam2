# Generated by Django 4.2.8 on 2024-01-02 18:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('erp', '0002_alter_printer_api_key'),
    ]

    operations = [
        migrations.AlterField(
            model_name='check',
            name='pdf_file',
            field=models.FileField(blank=True, null=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='check',
            name='printer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='printers', to='erp.printer'),
        ),
    ]