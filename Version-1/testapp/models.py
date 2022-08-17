from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Customer(models.Model):
    c = (
        ("M", "Male"),("F", "Female")
    )
    name = models.CharField(max_length=255, unique=True)
    email = models.EmailField()
    gender = models.CharField(max_length = 150, choices =c)
    is_registered = models.BooleanField()
   
    # id = models.BigAutoField(primary_key = True)

    def __str__(self):
        return self.name


class Contact_us(models.Model):
    name = models.CharField(max_length = 250)
    contact_number = models.IntegerField(blank = True, unique = True)
    subject = models.CharField(max_length = 250)
    message = models.TextField()
    added_on = models.DateTimeField(auto_now_add= True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Contact"
class Category(models.Model):
    cat_name = models.CharField(max_length = 255)
    cover_image = models.FileField(upload_to = "media")
    description = models.TextField()
    added_on = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return self.cat_name

class register_table(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    contact_num = models.IntegerField()
    profile_pic = models.ImageField(upload_to = "profiles", null = True, blank = True)
    age = models.CharField(max_length = 250, null = True, blank = True, default="Male")
    city = models.CharField(max_length = 250, null = True, blank = True)
    gender =models.CharField(max_length = 255, null = True, blank = True)
    update_on = models.DateTimeField(auto_now = True)


    def __str__(self):
        return self.user.username
class add_Form(models.Model):
    user_name = models.ForeignKey(User, on_delete=models.CASCADE)
    form_name = models.CharField(max_length =250)
    form_category = models.ForeignKey(Category, on_delete=models.CASCADE)
    form_image = models.ImageField(upload_to  = "upload")
    details = models.TextField()

    def __str__(self):
        # return self.form_category.cat_name
        return self.form_name


