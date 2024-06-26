# Generated by Django 4.1.13 on 2024-02-29 21:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Usuarios', '0002_alter_alumno_carrera_alter_coda_coordinacion_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='alumno',
            name='carrera',
            field=models.CharField(choices=[('', 'Seleccione una'), ('MAT', 'Matemáticas Aplicadas'), ('COM', 'Ingeniería en Computación')], max_length=30),
        ),
        migrations.AlterField(
            model_name='coda',
            name='coordinacion',
            field=models.CharField(choices=[('', 'Seleccione una'), ('MAT', 'Matemáticas Aplicadas'), ('COM', 'Ingeniería en Computación')], max_length=30),
        ),
        migrations.AlterField(
            model_name='cordinador',
            name='coordinacion',
            field=models.CharField(choices=[('', 'Seleccione una'), ('MAT', 'Matemáticas Aplicadas'), ('COM', 'Ingeniería en Computación')], max_length=30),
        ),
        migrations.AlterField(
            model_name='tutor',
            name='coordinacion',
            field=models.CharField(choices=[('', 'Seleccione una'), ('MAT', 'Matemáticas Aplicadas'), ('COM', 'Ingeniería en Computación')], max_length=30),
        ),
    ]
