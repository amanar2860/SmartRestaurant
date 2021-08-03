import uuid

from django.db import models
from django.conf import settings
from django.shortcuts import reverse
from django.utils import timezone
from django.contrib.auth.models import User


class Category(models.Model):
    categoryname = models.CharField(unique=True, max_length=200)
    posted_on = models.DateField(default=timezone.now)
    imageurl=models.FileField(default='default.png',upload_to='cat_images')

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categorys'

    def __str__(self):
        return self.id

    def __str__(self):
        return self.categoryname


class Feedback(models.Model):
    name = models.CharField(max_length=40)
    message = models.CharField(max_length=200)
    date = models.DateField(auto_now_add=True, null=True)

    class Meta:
        verbose_name = 'Feedback'
        verbose_name_plural = 'Feedbacks'

    def _str__(self):
        return self.name

    def get_absolute_url(self):
        """Returns the url to access a particular instance of the model."""
        return reverse('model-detail-view', args=[str(self.id)])


class Item(models.Model):
    LABELS = (
        ('Best Selling Foods', 'Best Selling Foods'),
        ('New Food', 'New Food'),
        ('Spicy Foods🔥', 'Spicy Foods🔥'),
    )

    LABEL_COLOUR = (
        ('danger', 'danger'),
        ('success', 'success'),
        ('primary', 'primary'),
        ('info', 'info'),
        ('warning', 'warning'),
    )

    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    description = models.CharField(max_length=250, blank=True)
    price = models.FloatField()
    pieces = models.IntegerField(default=6)
    tableno=models.IntegerField(blank=True)
    instructions = models.CharField(max_length=250, default="Available")
    image = models.ImageField(default='default.png', upload_to='images/')
    labels = models.CharField(max_length=25, choices=LABELS, blank=True)
    label_colour = models.CharField(max_length=15, choices=LABEL_COLOUR, blank=True)
    slug = models.SlugField(default="foods" ,unique=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)


    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("main:dishes", kwargs={
            'slug': self.slug
        })

    def get_add_to_cart_url(self):
        return reverse("main:add-to-cart", kwargs={
            'slug': self.slug
        })

    def get_item_delete_url(self):
        return reverse("main:item-delete", kwargs={
            'slug': self.slug
        })

    def get_update_item_url(self):
        return reverse("main:item-update", kwargs={
            'slug': self.slug
        })


class Reviews(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    rslug = models.SlugField()
    review = models.TextField()
    posted_on = models.DateField(default=timezone.now)

    class Meta:
        verbose_name = 'Review'
        verbose_name_plural = 'Reviews'

    def __str__(self):
        return self.review


class TableOrders(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    phoneno = models.CharField(max_length=10)
    onDate = models.DateField(default=timezone.now)
    onTime = models.TimeField()
    totalperson = models.IntegerField()
    table_orderno = models.IntegerField()
    description = models.TextField()
    status= models.TextField()
    booked_on = models.DateField(default=timezone.now)
    class Meta:

        verbose_name = 'TableOrder'
        verbose_name_plural = 'TableOrders'

    def __int__(self):
        return self.id

    def _str__(self):
        return self.name

    def get_absolute_url(self):
        """Returns the url to access a particular instance of the model."""
        return reverse('model-detail-view', args=[str(self.id)])


class CartItems(models.Model):
    ORDER_STATUS = (
        ('Active', 'Active'),
        ('Delivered', 'Delivered')
    )
    DONATE_STATUS=(
        ('Donate','Donate'),
        ('NoThanks','NoThanks')
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    quantity = models.IntegerField(default=1)
    ordered_date = models.DateField(default=timezone.now)
    status = models.CharField(max_length=20, choices=ORDER_STATUS, default='Active')
    delivery_date = models.DateField(default=timezone.now)
    table_orderno = models.IntegerField(default=1)
    donate_status=models.CharField(max_length=20, choices=DONATE_STATUS, default='NoThanks')
    payment_status = models.CharField(max_length=20,  default='Cash')
    payment_Desc = models.CharField(max_length=200, default='Paid')



    class Meta:
        verbose_name = 'Cart Item'
        verbose_name_plural = 'Cart Items'

    def __str__(self):
        return self.item.title

    def get_remove_from_cart_url(self):
        return reverse("main:remove-from-cart", kwargs={
            'pk': self.pk
        })

    def update_status_url(self):
        return reverse("main:update_status", kwargs={
            'pk': self.pk
        })
