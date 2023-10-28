from django import forms
from .models import Category, Question, Answer

# Define a form for creating or updating categories
class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['text']
        labels = {'text': 'Enter New Category Name'}


# Define a form for creating or updating questions
class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['text']
        labels = {'text': 'Enter Question'}
        widgets = {'text': forms.Textarea(attrs={'cols': 80})}

# Define a form for creating or updating answers
class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['text', ]
        labels = {'text': 'Your Answer'}
        widgets = {'text': forms.Textarea(attrs={'cols': 80})}


