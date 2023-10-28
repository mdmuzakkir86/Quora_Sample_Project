from django.urls import include, path
from . import views

# Define the namespace for the app
app_name = 'quora'

# Define the URL patterns for the "quora" app
urlpatterns = [
    # Define the URL pattern for the main index page
    path('', views.index, name='index'),

    # Define the URL pattern for the page displaying categories
    path('categories', views.categories, name='categories'),

    # Define the URL pattern for displaying a specific category by its ID
    path('categories/<int:category_id>/', views.category, name='category'),

    # Define the URL pattern for creating a new category
    path('new_category', views.new_category, name='new_category'),

    # Define the URL pattern for creating a new question within a specific category
    path('new_question/<int:category_id>/', views.new_question, name='new_question'),

    # Define the URL pattern for listing answers to a specific question by its ID
    path('list_answers/<int:question_id>/', views.list_answers, name='list_answers'),

    # Define the URL pattern for editing a specific question by its ID
    path('edit_question/<int:question_id>/', views.edit_question, name='edit_question'),

    # Define the URL pattern for answering a specific question by its ID
    path('answer_question/<int:question_id>/', views.answer_question, name='answer_question'),

    # Define the URL pattern for liking a specific answer by its ID
    path('like_answer/<int:answer_id>/', views.like_answer, name='like_answer'),

]