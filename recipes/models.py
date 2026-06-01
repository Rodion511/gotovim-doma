from django.db import models
from django.contrib.auth.models import User 
from django.db import models
from django.contrib.auth.models import User
class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название категории")
    slug = models.SlugField(unique=True, verbose_name="URL")
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class Recipe(models.Model):
    title = models.CharField(max_length=200, verbose_name="Название")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Категория")
    ingredients = models.TextField(verbose_name="Ингредиенты (через запятую)")
    description = models.TextField(verbose_name="Как приготовить")
    cooking_time = models.IntegerField(default=30, verbose_name="Время (мин)")
    image = models.ImageField(upload_to='recipes/', blank=True, null=True, verbose_name="Фото")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата добавления", null=True)  
    
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = "Рецепт"
        verbose_name_plural = "Рецепты"


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='favorited_by')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user', 'recipe')
class Recipe(models.Model):
    title = models.CharField(max_length=200, verbose_name="Название")
    ingredients = models.TextField(verbose_name="Ингредиенты (через запятую)")
    description = models.TextField(verbose_name="Как приготовить")
    cooking_time = models.IntegerField(default=30, verbose_name="Время (мин)")
    image = models.ImageField(upload_to='recipes/', blank=True, null=True, verbose_name="Фото") 
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = "Рецепт"
        verbose_name_plural = "Рецепты"


class Favorite(models.Model):
    """Избранные рецепты пользователя"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='favorited_by')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user', 'recipe')  
        verbose_name = "Избранное"
        verbose_name_plural = "Избранное"
    
    def __str__(self):
        return f"{self.user.username} - {self.recipe.title}"

from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название категории")
    slug = models.SlugField(unique=True, verbose_name="URL")
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class Recipe(models.Model):
    """Модель рецепта"""
    title = models.CharField(max_length=200, verbose_name="Название")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Категория")  # ДОБАВИТЬ
    ingredients = models.TextField(verbose_name="Ингредиенты (через запятую)")
    description = models.TextField(verbose_name="Как приготовить")
    cooking_time = models.IntegerField(default=30, verbose_name="Время (мин)")
    image = models.ImageField(upload_to='recipes/', blank=True, null=True, verbose_name="Фото")
    
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = "Рецепт"
        verbose_name_plural = "Рецепты"


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='favorited_by')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user', 'recipe')