from django.db import models

# Create your models here.
categoty_choice=(
    ('Andhra-Pradesh','Andhra-Pradesh'),
    ('Arunachal-Pradesh','Arunachal-Pradesh'),
    ('Assam','Assam'),
    ('Bihar','Bihar'),
    ('Chhattisgarh','Chhattisgarh'),
    ('Goa','Goa'),
    ('Gujarat','Gujarat'),
    ('Haryana','Haryana'),
    ('Himachal-Pradesh','Himachal-Pradesh'),
    ('Jharkhand','Jharkhand'),
    ('Karnataka','Karnataka'),
    ('Kerala','Kerala'),
    ('Madhya-Pradesh','Madhya-Pradesh'),
    ('Maharashtra','Maharashtra'),
    ('Manipur','Manipur'),
    ('Meghalaya','Meghalaya'),
    ('Mizoram','Mizoram'),
    ('Nagaland','Nagaland'),
    ('Odisha','Odisha'),
    ('Punjab','Punjab'),
    ('Rajasthan','Rajasthan'),
    ('Sikkim','Sikkim'),
    ('Tamil-Nadu','Tamil-Nadu'),
    ('Telangana','Telangana'),
    ('Tripura','Tripura'),
    ('Uttar-Pradesh','Uttar-Pradesh'),
    ('Uttarakhand','Uttarakhand'),
    ('West-Bengal','West-Bengal'),
)
class registraion(models.Model):
    First_name = models.CharField(max_length=50)
    Last_name = models.CharField(max_length=50)
    Email = models.EmailField()
    Mobile = models.CharField(max_length=50)
    Address1 = models.CharField(max_length=200)
    Address2 = models.CharField(max_length=150)
    City = models.CharField(max_length=30)
    State = models.CharField(max_length=150,blank=True, null = True,choices=categoty_choice)
    Pincode = models.CharField(max_length=10)
    picture =  models.ImageField(upload_to='media' ,null=True, blank=True) 


class exam(models.Model):
    question = models.CharField(max_length=200)
    option1 = models.CharField(max_length=100)
    option2 = models.CharField(max_length=100)
    option3 = models.CharField(max_length=100)
    option4 = models.CharField(max_length=100)
    answer = models.CharField(max_length=100)    