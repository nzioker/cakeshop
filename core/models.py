from django.db import models
from django.conf import settings
from django.urls import reverse



class Item(models.Model):
    title = models.CharField(max_length=100)
    price = models.FloatField(max_length=50)
    description = models.TextField()
    slug = models.SlugField()
    

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse("cake", kwargs={"slug":self.slug})

    def get_add_to_cart_url(self):
        return reverse("add-to-cart", kwargs={"slug":self.slug})
    
    def get_remove_from_cart_url(self):
        return reverse("remove-from-cart", kwargs={"slug":self.slug})


class OrderItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.item.title}"
    
    def get_total_price(self):
        return self.quantity * self.item.price
    
    def get_final_price(self):
        return self.get_total_price()
    


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)

    def __str__(self):
        return str(self.items)
    
    def get_cart_total(self):
        total = 0
        for item in self.items.all():
            total += item.get_final_price()

        return total
    
    
