from django.db import models
from django.contrib.auth.models import User, Group

# Create your models here.


class Person(models.Model):
    birthdate = models.DateField()
    birthplace = models.ForeignKey("base.Area", on_delete=models.SET_NULL, null=True)
    account = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    job_location = models.ForeignKey("base.Area", related_name="work_at", on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return str(self.account.last_name) + ' ' + str(self.account.first_name)
    

class Office(models.Model):
    center = models.ForeignKey("base.Area", on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return str(self.center.name)

class Area(models.Model):
    name = models.CharField(max_length=250)
    center = models.ForeignKey("base.Office", on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return str(self.name) + ' - ' + str(self.center)

class Request(models.Model):
    request_date = models.DateField(auto_now_add=True)
    dup_number = models.IntegerField()
    requester = models.ForeignKey("base.Person", on_delete=models.CASCADE)
    state = models.CharField(max_length=250, default='Mbola tsy vita')
    office = models.ForeignKey("base.Office", on_delete=models.SET_NULL, null=True)
    pdf = models.FileField(upload_to='requests/', blank=True, null=True)

    def __str__(self):
        return str(self.request_date) + ' - ' + str(self.requester.account.first_name)



# Offices     {toerana mampizara : firaisana} : id, #centre
# Areas       {toerana kely, tafiditra anaty firaisana} : id, nom, #office
# Requests    {fangatahana copie} : id, date, copie, #person, #office
# Documents   {sauvegarde an'ireo copie efa lasa} : id, #request, blob