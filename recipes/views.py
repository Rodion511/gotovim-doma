from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Recipe, Favorite, Category 
from django.contrib.auth.models import User
from .forms import IngredientSearchForm, RegisterForm, RecipeFilterForm 
import random
def home(request):
    all_recipes = Recipe.objects.all()
    new_recipes = Recipe.objects.all().order_by('-id')[:6]
    fast_recipes = Recipe.objects.filter(cooking_time__lte=30)[:6]
    popular_recipes = Recipe.objects.all()[:6]
    categories = Category.objects.all()
    recipes_count = Recipe.objects.count()
    users_count = User.objects.count()
    
    context = {
        'new_recipes': new_recipes,
        'fast_recipes': fast_recipes,
        'popular_recipes': popular_recipes,
        'categories': categories,
        'recipes_count': recipes_count,
        'users_count': users_count,
    }
    return render(request, 'home.html', context)

def recipe_detail(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    is_favorite = False
    if request.user.is_authenticated:
        is_favorite = Favorite.objects.filter(user=request.user, recipe=recipe).exists()
    
    return render(request, 'recipe_detail.html', {
        'recipe': recipe,
        'is_favorite': is_favorite
    })

def recipe_list(request):
    recipes = Recipe.objects.all()
    filter_form = RecipeFilterForm(request.GET or None)
    if filter_form.is_valid():
        category = filter_form.cleaned_data.get('category')
        if category:
            recipes = recipes.filter(category=category)
        
        cooking_time = filter_form.cleaned_data.get('cooking_time')
        if cooking_time:
            if cooking_time == '15':
                recipes = recipes.filter(cooking_time__lte=15)
            elif cooking_time == '30':
                recipes = recipes.filter(cooking_time__gt=15, cooking_time__lte=30)
            elif cooking_time == '60':
                recipes = recipes.filter(cooking_time__gt=30, cooking_time__lte=60)
            elif cooking_time == '60+':
                recipes = recipes.filter(cooking_time__gt=60)
        
        sort_by = filter_form.cleaned_data.get('sort_by')
        if sort_by:
            recipes = recipes.order_by(sort_by)
        else:
            recipes = recipes.order_by('title')
    
    search_query = request.GET.get('search', '')
    if search_query:
        recipes = recipes.filter(title__icontains=search_query)
    
    categories = Category.objects.all()
    
    context = {
        'recipes': recipes,
        'filter_form': filter_form,
        'categories': categories,
        'search_query': search_query,
    }
    return render(request, 'recipe_list.html', context)

def random_recipe(request):
    """Страница для генерации случайного рецепта"""
    recipe = None
    if 'generate' in request.GET:
        count = Recipe.objects.count()
        if count > 0:
            random_index = random.randint(0, count - 1)
            recipe = Recipe.objects.all()[random_index]
    
    return render(request, 'random_recipe.html', {'recipe': recipe})
def search_by_ingredients(request):
    results = []
    form = IngredientSearchForm(request.GET or None)
    
    if form.is_valid() and form.cleaned_data['ingredients']:
        ingredients_input = form.cleaned_data['ingredients']
        user_ingredients_list = [ing.strip().lower() for ing in ingredients_input.split(',')]
        
        all_recipes = Recipe.objects.all()
        recipes_with_matches = []
        
        for recipe in all_recipes:
            recipe_ingredients_lower = recipe.ingredients.lower()
            matched_count = 0
            
            for user_ing in user_ingredients_list:
                if user_ing in recipe_ingredients_lower:
                    matched_count += 1
            
            if matched_count > 0:
                recipes_with_matches.append({
                    'recipe': recipe,
                    'matched_count': matched_count,
                })
        
        recipes_with_matches.sort(key=lambda x: x['matched_count'], reverse=True)
        results = [item['recipe'] for item in recipes_with_matches]
    
    # Убираем сортировку по просмотрам, просто берём первые 6 рецептов
    popular_recipes = Recipe.objects.all().order_by('-id')[:6]  # просто последние добавленные
    
    context = {
        'form': form,
        'results': results,
        'user_ingredients': form.cleaned_data.get('ingredients', '') if form.is_valid() else '',
        'popular_recipes': popular_recipes,
    }
    return render(request, 'search.html', context)
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Вы успешно зарегистрированы!')
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})

@login_required
def profile(request):
    favorites = Favorite.objects.filter(user=request.user).select_related('recipe')
    return render(request, 'profile.html', {'favorites': favorites})

@login_required
def add_to_favorites(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)   
    favorite, created = Favorite.objects.get_or_create(user=request.user, recipe=recipe)
    
    if created:
        messages.success(request, f'Рецепт "{recipe.title}" добавлен в избранное!')
    else:
        messages.info(request, f'Рецепт уже в избранном')
    
    return redirect('recipe_detail', pk=pk)

@login_required
def remove_from_favorites(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    Favorite.objects.filter(user=request.user, recipe=recipe).delete()
    messages.success(request, f'Рецепт "{recipe.title}" удален из избранного!')
    
    next_url = request.GET.get('next', 'profile')
    if next_url == 'profile':
        return redirect('profile')
    return redirect('recipe_detail', pk=pk)