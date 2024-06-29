from django.db import models
# from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField
from django.db.models.signals import post_save
from django.dispatch import receiver

from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    is_admin = models.BooleanField('Is admin', default=False)
    is_hospital = models.BooleanField('Is hospital',default=False)
    is_public = models.BooleanField('Is public', default=False)

  
class Profile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE,related_name='profile')
    username=models.CharField(max_length=100,blank=True,null=True)
    user_email=models.EmailField(max_length=100,blank=True,null=True)
    profile_pic=CloudinaryField('image')
    biography=models.TextField(blank=True,null=True)
    contact_number=models.CharField(max_length=200)
    location=models.CharField(max_length=200)

    def save_profile(self):
        self.save()

    def delete_profile(self):
        self.delete()

    def profile_update(self,id,profile):
        updated_profile=Profile.objects.filter(id=id).update(profile)
        return updated_profile

    def __str__(self):
        return str(self.username)
    
    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)
            instance.profile.save()

        post_save.connect(Profile, sender=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        Profile.objects.get_or_create(user=instance)
        instance.profile.save()
    
    @classmethod
    def filter_profile_by_id(cls, id):
        profile = Profile.objects.filter(user__id = id).first()
        return profile
 
    


class Ambulance(models.Model):
    image = CloudinaryField('image', null=True)
    ambulance_name = models.CharField(max_length=50, null=True)
    current_location = models.CharField(max_length=100, null=True)
    availability = models.BooleanField(default=True)  # Changed to a Boolean field for simplicity
    response_rate = models.IntegerField(default=0)  # General response rate for emergencies
    driver_name = models.CharField(max_length=50, null=True)
    hospital_name = models.CharField(max_length=100, null=True)
    
    def save_ambulance(self):
        self.save()

    def update_ambulance(self):
        self.save()  # save() should be used for updating as well

    def delete_ambulance(self):
        self.delete()
        
    @classmethod
    def find_ambulance(cls, ambulance_id):
        return cls.objects.filter(id=ambulance_id).first()  # Corrected the query to use id field

    def __str__(self):
        return self.ambulance_name



















# class Machinery(models.Model):
#     image=CloudinaryField('image', null=True)
#     machinery_properties = models.TextField(null=True)
#     machinery_name =models.CharField(max_length=50 , null=True)
#     current_location = models.CharField(max_length=100, null=True)
#     availability= models.CharField(max_length=5)
#     hire_price= models.IntegerField(default=0)
#     ploughing_pay_rate= models.IntegerField(default=0)
#     planting_pay_rate= models.IntegerField(default=0)
#     forklifting_pay_rate= models.IntegerField(default=0)
#     transport_pay_rate= models.IntegerField(default=0)
#     operator_name = models.CharField(max_length=50 , null=True)
#     owner_id = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    
    
#     def save_machinery(self):
#         self.save()

#     def update_machinery(self):
#         self.update()

#     def delete_farm(self):
#         self.delete()
        
#     @classmethod
#     def find_machinery(cls,machinery_id):
#         new_machinery = cls.objects.filter(machinery_id=machinery_id)
#         return new_machinery

#     def __str__(self):
#         return self.machinery_name
    
    





class HospitalPost(models.Model):
    ambulance_name = models.CharField(max_length=100, null=True, blank=True)
    ambulance_image = CloudinaryField('ambulance_image', blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts", null=True, blank=True)
    description = models.TextField(null=False)
    posted_at = models.DateTimeField(auto_now_add=True)
    pay_rate = models.CharField(max_length=100, null=True, blank=True)

    def save_post(self):
        self.save()

    def delete_post(self):
        self.delete()

    def update_post(self, id, updated_data):
        updated_post = HospitalPost.objects.filter(id=id).update(**updated_data)
        return updated_post

    def __str__(self):
        return self.ambulance_name if self.ambulance_name else "Unnamed Ambulance"




























# class Owner_post(models.Model):
#     machinery_name=models.CharField(max_length=100,null=True,blank=True)
#     machinery_image=CloudinaryField('machinery_image',blank=True)
#     user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="post",null=True,blank=True)
#     describe=models.TextField(null=False)
#     posted_at=models.DateTimeField(auto_now_add=True,)
#     pay_rate=models.CharField(max_length=100,null=True,blank=True)

#     def save_owner_post(self):
#         self.save()

#     def delete_owner_post(self):
#         self.delete()

#     def update_owner_post(self,id,owner_post):
#         updated_post=Owner_post.objects.filter(id=id).update(owner_post)
#         return updated_post


#     def __str__(self):
#         return self.machinery_name
    

# class Order(models.Model):
#     customer_name = models.CharField(max_length=100)
#     contact_no = models.CharField(max_length=15)
#     address = models.CharField(max_length=40)
#     date = models.DateTimeField(auto_now_add=True)
#     service=models.CharField(max_length=40, null=True)
#     machinery_id = models.ForeignKey(Machinery, on_delete=models.CASCADE, null=True)
#     user_id = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    
#     def save_order(self):
#         self.save()

#     def delete_order(self):
#         self.delete()

#     def update_order(self,id,order):
#         updated_order=Order.objects.filter(id=id).update(order)
#         return updated_order
    
#     @classmethod
#     def get_orders(cls,id):
#         orders = Order.objects.filter(machinery_id__pk = id)
#         return orders


#     def __str__(self):
#         return self.machinery_name
    






class Booking(models.Model):
    customer_name = models.CharField(max_length=100)
    contact_no = models.CharField(max_length=15)
    address = models.CharField(max_length=100)  # Increased max_length for more detailed addresses
    date = models.DateTimeField(auto_now_add=True)
    service = models.CharField(max_length=40, null=True)
    ambulance = models.ForeignKey(Ambulance, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def save_booking(self):
        self.save()

    def delete_booking(self):
        self.delete()

    def update_booking(self, id, updated_data):
        updated_booking = Booking.objects.filter(id=id).update(**updated_data)
        return updated_booking
    
    @classmethod
    def get_bookings(cls, ambulance_id):
        bookings = cls.objects.filter(ambulance_id=ambulance_id)
        return bookings

    def __str__(self):
        return f"{self.customer_name} - {self.service}"





    
class Customer(models.Model):
    customer_name=models.CharField(max_length=50)
    customer_id =models.ForeignKey(User, on_delete=models.CASCADE, null=True) 

    
class Feedback(models.Model):
    user_name = models.CharField(max_length=50, null=True)
    email = models.EmailField(max_length=70, null=True, blank=True)
    content=models.TextField(null=True)
    rating = models.IntegerField(default=0)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    ambulance_id =models.ForeignKey(Ambulance, on_delete=models.CASCADE, null=True)
    posted_at=models.DateTimeField(auto_now_add=True,)
    