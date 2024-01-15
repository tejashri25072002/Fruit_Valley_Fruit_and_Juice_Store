from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class fruit_product(models.Model):
    name=models.CharField(max_length=50,verbose_name="Fruit name")
    price=models.FloatField()
    benefit=models.CharField(max_length=800,verbose_name="fruit benefit")
    CAT=((1,'Fleshy Fruit'),(2,'Dry Fruit'))
    cat=models.IntegerField(verbose_name="fruit type",choices=CAT)
    is_active=models.BooleanField(default=True,verbose_name="Available")
    fimage=models.ImageField(upload_to='image/fruits')

class juice_product(models.Model):
    name=models.CharField(max_length=50,verbose_name="Juice name")
    price=models.FloatField()
    benefit=models.CharField(max_length=800,verbose_name="juice benefit")
    JUICECAT=((1,'Fresh Fruit Juice'),(2,'FC Juice(From Concentrate)'),(3,'NFC Juice(Non From Concentrate)'),(4,'Cold Press Juice'),(5,'Fruity Drinks'))
    juicecat=models.IntegerField(verbose_name="juice type",choices=JUICECAT)
    is_active=models.BooleanField(default=True,verbose_name="Available")
    jimage=models.ImageField(upload_to='image/fruits')

    #def __str__(self):
    #    return self.name

class FruitAddCart(models.Model):
    uid=models.ForeignKey(User,on_delete=models.CASCADE,db_column="uid")
    pid=models.ForeignKey(fruit_product,on_delete=models.CASCADE,db_column="pid")
    quantity=models.IntegerField(default=1)

class JuiceAddCart(models.Model):
    uid=models.ForeignKey(User,on_delete=models.CASCADE,db_column="uid")
    pid=models.ForeignKey(juice_product,on_delete=models.CASCADE,db_column="pid")
    quantity=models.IntegerField(default=1)

class FruitOrder(models.Model):
    order_id=models.CharField(max_length=50)
    uid=models.ForeignKey(User,on_delete=models.CASCADE,db_column="uid")
    pid=models.ForeignKey(fruit_product,on_delete=models.CASCADE,db_column="pid")
    quantity=models.IntegerField(default=1)

class JuiceOrder(models.Model):
    order_id=models.CharField(max_length=50)
    uid=models.ForeignKey(User,on_delete=models.CASCADE,db_column="uid")
    pid=models.ForeignKey(juice_product,on_delete=models.CASCADE,db_column="pid")
    quantity=models.IntegerField(default=1)

class customer_details(models.Model): 
    uname=models.CharField(max_length=50)
    email=models.CharField(max_length=50)
    firstname=models.CharField(max_length=50,null=True)
    lastname=models.CharField(max_length=50,null=True)
    mobile=models.BigIntegerField(null=True)
    address=models.CharField(max_length=350,null=True)
    is_active=models.BooleanField(default=True, verbose_name ="Active")