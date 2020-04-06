from django.db import models
import uuid

# Create your models here.


class Customer(models.Model):
    uuid = models.UUIDField(primary_key=True, auto_created=True, default=uuid.uuid4, editable=False, max_length=36)
    name = models.CharField(verbose_name="客户", max_length=32)
    age = models.CharField(verbose_name="年龄", max_length=32)
    email = models.CharField(verbose_name="邮箱", max_length=32)
    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    update_time = models.DateTimeField(verbose_name='更新时间', auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "customs"
        verbose_name = "客户表"
        verbose_name_plural = verbose_name


class Payment(models.Model):
    uuid = models.UUIDField(primary_key=True, auto_created=True, default=uuid.uuid4, editable=False, max_length=36)
    title = models.CharField(max_length=32, verbose_name="消费记录")
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="customer")
    money = models.IntegerField(verbose_name='付费金额')
    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    update_time = models.DateTimeField(verbose_name='更新时间', auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = "payment"
        verbose_name = "账单记录"
        verbose_name_plural = verbose_name