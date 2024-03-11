# Code-summary

Back-End stories
-Python
1.I created model for adding recipe, book about recipe and contact.<br>
2.I also created Modelform.
3.There are three functions below, Add function saves in the database recipe entered by users through the Modelform.
'''python
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
'''
<img src=https://github.com/seonhwakwon/Code-summary/assets/148311845/8155f171-7922-4b33-95e2-8c388d068f63 width="400" height="300">

4.saved_list function also saves in the database that my app main page's recipes, if the user wants.
'''python
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

    Add_recipe(image=image_url, title=title, cooking_time=cooking_time, serving=serving, ingredient=ingredient, direction=direction).save()
'''
<img src=https://github.com/seonhwakwon/Code-summary/assets/148311845/0940184a-dc21-4402-978d-835b7382f582 width="400" height="300"><img src=https://github.com/seonhwakwon/Code-summary/assets/148311845/602050e8-2eaa-41c4-ac89-82065a6cf117  width="400" height="300">

5.List function shows the recipes's list saved in the database.
In the list function, users can delete, edit the recipe user choose and link to the detail page if users click the 'title' user choose.
'''python
def list(request):
    recipe = Add_recipe.Add_recipes.all().order_by('pk')
    content ={'recipe': recipe}
    return render(request, 'recipes/recipes_list.html', content)
'''
<img src=https://github.com/seonhwakwon/Code-summary/assets/148311845/6af0295f-ad2c-43f0-9872-f417f3034207 width="400" height="300">

6.bs fuction shows the result(popular recipe and link) parsing the url using beautifulsoup. 
''''''python
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
'''    
<img src=https://github.com/seonhwakwon/Code-summary/assets/148311845/b642189b-6e7e-4850-bfd4-00359642401f width="400" height="300"> 

7.Connect the API and get the JSON repose, add in a template for displaying recipe books.
'''python
def create_api(request, id=0):

    response = requests.get("https://www.googleapis.com/books/v1/volumes?q=recipe")
   
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
'''
8.save_api function save API result in the database.
def save_api(request, id, number, title, author, published_date):
    print(number, title, author, published_date)
    Recipebook(number=number, title=title,author=author,  published_date=published_date).save()

    return redirect('recipes_saved_result_api')
<img src=https://github.com/seonhwakwon/Code-summary/assets/148311845/12753b11-7abb-4b03-8962-e36f5f76dcb7) width="400" height="300">

9.-JavaSCript- get_favorite_recipe function moves to the favorite recipe box, if users click the heart button in home.html. Additional when users click the text in the favorite box, it also links to recipe's detail page.(No duplication addition with same recipe even though clicks two time with same recipe.)
''' JavaScript
function get_favorite_Recipe(clicked_value){
     var text="";
     recipes.push(clicked_value);
     for(var i=0; i<recipes.length; i++){
        var text1 =  recipes[i];

        for(var j=i+1; j<recipes.length; j++){
            if(text1 === recipes[j]){
                recipes.splice(i, 1);
                break;
            }
        }

     }
     for (var i in recipes){
             text += '<a style="color:#fff;" href="http://127.0.0.1:8000/Recipes/' + recipes[i] + '/">'+ recipes[i]+'</a><br>';
     }

     document.getElementById('favorite_recipe').innerHTML= '<h4 style="color:purple; text-align:left;">&#x2764;favorite recipe</h4>'+'<br>' +'<h5>' + text +'</h5>'+'<br>';
'''
<img src=https://github.com/seonhwakwon/Code-summary/assets/148311845/0480e4cc-029e-4b62-87df-cc4f3476b6da width="400" height="300">
    
Front-End stories
1.This template file is saved a result of API(Recipe book).
All display templates that display the result are similar with below template.

{{% extends 'recipes_base.html' %}
{% load static %}

{% block title %}My Portfolio:Home{% endblock %}
{% block content %}
<div class="container">
    <table style="width:100%;">
        <tr>
            <th>     </th>
            <th>Title</th>
            <th>Author </th>
            <th>Published Date</th>
        </tr>
        {%for saved_menu in saved_menus %}
        <tr>
            <td>{{saved_menu.number}}</td>
            <td>{{saved_menu.title}}</td>
            <td>{{saved_menu.author}} </td>
            <td>{{saved_menu.published_date}}</td>
            <td><a href="{% url 'recipes_delete_api' saved_menu.id %}"><button>delete</button></a></td>
        </tr>
        {%endfor%}
    </table>
</div>
{% endblock %}

2.This template is contact template using form.
All of the templates using form are similar with below template. 
{% extends 'recipes_base.html' %}
{% load static %}

{% block title %}My Portfolio:Home{% endblock %}
{% block content %}
<div class="container">
    <h1>Contact Us</h1>
    <div id ="Contact">
            <div class="form-popup" id="myForm">
            <form method="POST" class="form-container">
                {% csrf_token %}
                name : {{form.name}}
                phone : {{form.phone}}
                e-mail : {{form.email}}
                message :<br> {{form.message}}
                <button type="submit" style="float:right;">SUBMIT</button>
             </form>
            </div>
    </div>
</div>
{% endblock %}

3.Using CSS.
-Hover_effect in image
<img src = https://github.com/seonhwakwon/Code-summary/assets/148311845/e745b3f6-7af9-4b6d-aa56-ec214c1111cc width="200" hegith="100">
-Hover_effect in Navbar
<img src=https://github.com/seonhwakwon/Code-summary/assets/148311845/3604e60f-b7d2-4798-ba5b-3e22413c5903 width="200" hegith="100">
-footer
<img src=https://github.com/seonhwakwon/Code-summary/assets/148311845/2d28dbc7-9e4e-4345-a00d-c7ea546dc5a0 width="200" hegith="100">
-button
<img src=https://github.com/seonhwakwon/Code-summary/assets/148311845/5d280abd-0076-4008-9b8b-ad86508d85a7 width="200" hegith="100">
