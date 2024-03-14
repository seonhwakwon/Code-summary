from django.shortcuts import render,redirect
from .forms import Add_recipeForm, ContactForm
from .models import Add_recipe,Recipebook, contact
from django.urls import reverse
import requests
from bs4 import BeautifulSoup
import json


# Create your views here.
def home(request):
    return render(request, 'recipes/recipes_home.html')

def add(request):
    if request.method == "POST":
        form = Add_recipeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('recipes_list')
    else:
        form=Add_recipeForm()

    content = {'form': form}
    return render(request, 'recipes/recipes_add.html', content)

def list(request):
    recipe = Add_recipe.Add_recipes.all().order_by('pk')
    content ={'recipe': recipe}
    return render(request, 'recipes/recipes_list.html', content)

def delete(request,id):
    recipe =Add_recipe.Add_recipes.get(pk=id)
    recipe.delete()
    return redirect('recipes_list')


def detail(request,id):
    recipe = Add_recipe.Add_recipes.get(pk=id)
    content ={'recipe': recipe}
    return render(request, 'recipes/recipes_detail.html', content)

def edit(request,id):
    recipe = Add_recipe.Add_recipes.get(pk=id)
    if request.method == "POST":
        form = Add_recipeForm(request.POST, instance=recipe)
        if form.is_valid():
            form.save()
            return redirect('recipes_detail', recipe.id)
    else:
        form = Add_recipeForm(instance=recipe)
    content = {'form': form,'recipe':recipe}
    return render(request,'recipes/recipes_edit.html', content)

def bs(request):
    url = requests.get("https://www.allrecipes.com/gallery/most-popular-recipes-of-the-year/")
    soup = BeautifulSoup(url.content, 'html.parser')
    menus = soup.select('.mntl-sc-block-heading__text')
    links = soup.select('.mntl-sc-block-universal-featured-link__link.mntl-text-link.button--contained-standard.type--squirrel')

    recipes = []
    for link in links:
        link_text = link.attrs['href']
        recipes.append(link_text)

    menu_name =[]
    for menu in menus:
        menu_text =  menu.get_text()
        menu_name.append(menu_text)

    #convert list to dictionary
    dict_recipes = dict(zip(menu_name, recipes))

    content = {'dict_recipes' : dict_recipes}
    return render(request, 'recipes/recipes_bs.html', content)
def create_api(request, id=0):
    #get url
    response = requests.get("https://www.googleapis.com/books/v1/volumes?q=recipe")
    #convert to dictionary
    info = json.loads(response.text)
    books =[]
    titles = []
    authors = []
    published_dates = []
    number_items = info['items']
    recipe_ids = []
    i = 1

    #parse a JASON (get the titles, authors and published_data.
    # If title, author and published_data not exist, set a default value "None".
    for count in range(len(number_items)):
        title = (number_items[count]['volumeInfo']).get("title", 'None')
        author = (number_items[count]['volumeInfo']).get("authors",['None'])[0]
        published_date = (number_items[count]['volumeInfo']).get("publishedDate", 'None')
        recipe_id = i
        titles.append(title)
        authors.append(author)
        published_dates.append(published_date)
        recipe_ids.append(i)
        i= i+1

    for j in range(len(number_items)):
        book = [recipe_ids[j], titles[j],authors[j],published_dates[j]]
        books.append(book)
    content ={'books': books}
    if id==0:
        return render(request, 'recipes/recipes_create_api.html',content)
    else:
        return save_api(request, id, recipe_ids[id-1], titles[id-1],authors[id-1],published_dates[id-1])
def save_api(request, id, number, title, author, published_date):
    print(number, title, author, published_date)
    Recipebook(number=number, title=title,author=author,  published_date=published_date).save()

    return redirect('recipes_saved_result_api')

def saved_result_api(request):
    saved_menus = Recipebook.Recipebooks.all()
    content = {'saved_menus': saved_menus}

    return render(request, 'recipes/recipes_saved_result_api.html',content )
def delete_api(request, id):
    book = Recipebook.Recipebooks.get(pk=id)
    book.delete()
    i=0
    return redirect('recipes_saved_result_api')


def contact(request):
    form = ContactForm(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return HttpResponse("Submitted successfully")
    content = {'form': form}
    return render(request, 'recipes/recipes_contact.html',content)

def parsing_recipe(request, id):
    recipes_url = []
    url = requests.get("http://127.0.0.1:8000/Recipes/")
    soup = BeautifulSoup(url.content, 'html.parser')
    links = soup.select(".like")
    for link in links:
        link_text = link.attrs['value']
        recipes_url.append(link_text)

    return saved_list(request,recipes_url[id] ,id)

def saved_list(request, recipes_url, id):
    title_list =[]
    cooking_time_serving_list =[]
    ingredient_list=[]
    direction_list=[]
    url = 'http://127.0.0.1:8000/Recipes/'+ recipes_url +'/'

    url = requests.get(url)
    soup = BeautifulSoup(url.content, 'html.parser')

    title_list = recipes_url.split('_')
    title = (' ').join(title_list)
    print(title)
    image_class = soup.select(".img_fluid")
    image = image_class[0].attrs['src']
    image_url = "http://127.0.0.1:8000" + image


    time_serving_class = soup.select(".row")[1].get_text()
    cooking_time_serving_list = time_serving_class.split()
    cooking_time = cooking_time_serving_list[2]
    serving = cooking_time_serving_list[4]



    ingredient_class = soup.select(".row")[2].get_text()
    ingredient_list = ingredient_class.split('*')
    ingredient = ingredient_list[2]
    direction_class = soup.select(".row")[3].get_text()
    direction_list= direction_class.split('*')
    direction =direction_list[2]
    ingredient = ingredient_list[2]
    print(serving)
    Add_recipe(image=image_url, title=title, cooking_time=cooking_time, serving=serving, ingredient=ingredient, direction=direction).save()

    return redirect('recipes_list')

def coconut(request):

    return render(request, 'menu/recipes_coconut.html')
def shrimp_tacos(request):
    return render(request, 'menu/recipes_shrimp_tacos.html')

def chicken_miso_soup(request):
    return render(request, 'menu/recipes_chicken_miso_soup.html')

def asparagus_soup(request):
    return render(request,'menu/recipes_asparagus_soup.html')

def zucchini_salad(request):
    return render(request,'menu/recipes_zucchini_salad.html')

def cabbage_stir_fry(request):
    return render(request,'menu/recipes_cabbage_stir_fry.html')

def cranberry_tart(request):
    return render(request,'menu/recipes_cranberry_tart.html')

def sugar_cookie(request):
    return render(request,'menu/recipes_sugar_cookie.html')

def orange_cake(request):
    return render(request,'menu/recipes_orange_cake.html')

def strawberry_matcha_latte(request):
    return render(request,'menu/recipes_strawberry_matcha_latte.html')

def lemonade(request):
    return render(request,'menu/recipes_lemonade.html')

def cucumber_and_tonic(request):
    return render(request,'menu/recipes_cucumber_and_tonic.html')
