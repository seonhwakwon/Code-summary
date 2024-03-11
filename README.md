# Code-summary

Back-End stories

1.I created model for adding recipe, book about recipe and contact.
2.I also created Modelform.

3.There are three functions below, Add function saves in the database recipe entered by users through the Modelform.

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

<img src=https://github.com/seonhwakwon/Code-summary/assets/148311845/8155f171-7922-4b33-95e2-8c388d068f63 width="400" height="300">

4.saved_list function also saves in the database that my app main page's recipes, if the user wants.
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

    <img src=https://github.com/seonhwakwon/Code-summary/assets/148311845/0940184a-dc21-4402-978d-835b7382f582 width="400" height="300"><img src =https://github.com/seonhwakwon/Code-summary/assets/148311845/602050e8-2eaa-41c4-ac89-82065a6cf117  width="400" height="300">
