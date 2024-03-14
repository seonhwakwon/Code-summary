from django.db import models

# Create your models here.

class Add_recipe(models.Model):
    image = models.CharField(max_length=60, blank='False')
    title = models.CharField(max_length=60)
    # image = models.ImageField(upload_to='Recipes',null=True)
    cooking_time = models.CharField(max_length=20, blank='False')
    serving = models.CharField(max_length=20, blank='False')
    ingredient = models.TextField(max_length=1000, blank='False')
    direction = models.TextField(max_length=2000)

    Add_recipes = models.Manager()

    def __str__(self):
        return f'id={self.id} title={self.title}, age={self.cooking_time}, image={self.image}'

class Recipebook(models.Model):
    number= models.IntegerField(db_column='number', null=True)
    title = models.CharField(db_column='Title',max_length=60)
    author =models.CharField(db_column='Author', max_length=30)
    published_date = models.CharField(db_column=' published_date', max_length=30)

    Recipebooks = models.Manager()

    def __str__(self):
        return self.title,self.author, self.published_date

class contact(models.Model):
    name = models.CharField(max_length=60)
    phone = models.CharField(max_length=50)
    email = models.CharField(max_length=254)
    message = models.TextField(null=True, blank=True)

    def __str__(self):
        return f'contact[name ={self.name} phone={self.phone} email={self.email} message={self.message}]'