from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from .managers import UserManager

# Create your models here.
class User(AbstractBaseUser):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    
    def get_short_name(self):
        # The user is identified by their email
        return self.email
    
    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True
    
    def has_module_perms(self, app_label):
           return True
    
    def __str__(self):
        return self.email
    
    
class Room(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='creator', default=None)
    key = models.CharField(max_length=100, null=False, blank=False)
    name = models.CharField(max_length=100, null=False, blank=False, default='')
    password = models.CharField(max_length=20, null=False, blank=False)
    users = models.ManyToManyField(User, related_name='user_rooms')
    def __str__(self):
        return self.name
    
class money_request(models.Model):
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="from_money")
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="to_money")
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    amount = models.IntegerField()
    description = models.CharField(max_length=250, null=True, blank=True)
    key = models.CharField(max_length=20, null=False, blank=False, default='')
    is_accepted = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)
    
    
    def __str__(self):
        return self.from_user.email
    
class receipt(models.Model):
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="from_receipt")
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="to_receipt")
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    amount = models.IntegerField()
    last_updated = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.from_user.email
    
    def save(self, *args, **kwargs):
        if (self.amount == 0):
            super(receipt, self).delete()
        elif (self.amount < 0):
            self.amount = -self.amount
            self.to_user, self.from_user = self.from_user, self.to_user
            super(receipt, self).save(*args, **kwargs)
        else:
            super(receipt, self).save(*args, **kwargs)

