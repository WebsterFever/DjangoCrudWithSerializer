from django.db import models

# Create your models here.

class Address(models.Model):
    street = models.CharField(max_length=127)
    number = models.IntegerField()
    user = models.OneToOneField("users.User", 
    on_delete = models.CASCADE,
    )
    
def __repr__(self) -> str:
    return f"<[{self.id}] {self.street} - {self.number}>"
