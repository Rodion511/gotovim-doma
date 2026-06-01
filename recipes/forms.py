from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Category  # ДОБАВИТЬ

class IngredientSearchForm(forms.Form):
    ingredients = forms.CharField(
        label='Ваши ингредиенты',
        max_length=200,
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'например: морковь, картофель, курица'})
    )


class RecipeFilterForm(forms.Form):
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        required=False,
        empty_label="Все категории",
        widget=forms.Select(attrs={'class': 'filter-select'})
    )
    
    cooking_time = forms.ChoiceField(
        choices=[
            ('', 'Любое время'),
            ('15', 'До 15 минут'),
            ('30', '15-30 минут'),
            ('60', '30-60 минут'),
            ('60+', 'Больше 60 минут'),
        ],
        required=False,
        widget=forms.Select(attrs={'class': 'filter-select'})
    )
    sort_by = forms.ChoiceField(
        choices=[
            ('title', 'По названию (А-Я)'),
            ('-title', 'По названию (Я-А)'),
            ('cooking_time', 'По времени (сначала быстрые)'),
            ('-cooking_time', 'По времени (сначала долгие)'),
        ],
        required=False,
        widget=forms.Select(attrs={'class': 'filter-select'})
    )


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class RatingForm(forms.Form):
    rating = forms.ChoiceField(
        choices=[(1, '★'), (2, '★★'), (3, '★★★'), (4, '★★★★'), (5, '★★★★★')],
        widget=forms.RadioSelect(attrs={'class': 'rating-radio'})
    )