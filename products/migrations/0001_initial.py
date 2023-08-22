# Generated by Django 4.2.4 on 2023-08-22 04:07

from django.db import migrations, models
import django.db.models.deletion
import products.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0004_alter_user_number'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='카테고리명')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_name', models.CharField(max_length=200, verbose_name='상품명')),
                ('price', models.IntegerField(verbose_name='가격')),
                ('amount', models.IntegerField(default=0, verbose_name='수량')),
                ('desc', models.TextField()),
                ('score', models.FloatField(default=0, verbose_name='평점')),
                ('thumbnail_image', models.ImageField(blank=True, null=True, upload_to=products.models.image_path, verbose_name='썸네일')),
                ('status', models.CharField(max_length=30, verbose_name='상태')),
                ('order_status', models.CharField(max_length=30, verbose_name='주문 상태')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='등록일')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='수정일')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.category', verbose_name='카테고리')),
                ('seller', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.seller', verbose_name='판매자')),
            ],
        ),
        migrations.CreateModel(
            name='ProductImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to=products.models.image_path, verbose_name='상품 이미지')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.product', verbose_name='상품')),
            ],
        ),
    ]