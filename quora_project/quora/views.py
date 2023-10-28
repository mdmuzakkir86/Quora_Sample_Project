from django.shortcuts import render, reverse
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import reverse
from django.contrib.auth.decorators import login_required
from .models import Category, Question, Answer
from .forms import CategoryForm, QuestionForm, AnswerForm

# Define a view function to display the main page.
def index(request):
    # Retrieve and order questions by date.
    questions = Question.objects.order_by('-date_added')
    context = {'questions': questions}
    return render(request, 'quora/index.html', context)


# Define a view function to display a list of categories.
def categories(request):
    # Retrieve and order categories by their text names.
    categories = Category.objects.order_by('text')
    context = {'categories': categories}
    return render(request, 'quora/categories.html', context)

# Define a view function to display a specific category and its questions.
def category(request, category_id):
    # Retrieve a specific category by its ID and order its questions by date.
    category = Category.objects.get(id=category_id)
    questions = category.question_set.order_by('-date_added')
    context = {'category': category, 'questions': questions}
    return render(request, 'quora/category.html', context)

# Define a view function for creating a new category (requires login).
@login_required
def new_category(request):
    if request.method != 'POST':
        # No data submitted; create a blank form.
        form = CategoryForm()
    else:
        # POST data submitted; process data and save a new category.
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('quora:categories'))
    context = {'form': form}
    return render(request, 'quora/new_category.html', context)


# Define a view function to list answers for a specific question.
def list_answers(request, question_id):
    # Retrieve a specific question and order its answers by rating.
    question = Question.objects.get(id=question_id)
    answers = question.answer_set.order_by('-rating')
    context = {'question': question, 'answers': answers}
    return render(request, 'quora/answer.html', context)


# Define a view function for creating a new question within a category (requires login).
@login_required
def new_question(request, category_id):
    category = Category.objects.get(id=category_id)

    if request.method != 'POST':
        # No data submitted; create a blank form.
        form = QuestionForm()
    else:
        # POST data submitted; process data and save a new question.
        form = QuestionForm(data=request.POST)
        if form.is_valid():
            new_question = form.save(commit=False)
            new_question.category = category
            new_question.owner = request.user
            new_question.save()
            return HttpResponseRedirect(reverse('quora:category', args=[category_id]))

    context = {'category': category, 'form': form}
    return render(request, 'quora/new_question.html', context)


# Define a view function for editing a question (requires login).
@login_required
def edit_question(request, question_id):
    # Retrieve a specific question and its category.
    question = Question.objects.get(id=question_id)
    category = question.category
    if question.owner != request.user:
        raise Http404

    if request.method != 'POST':
        # Initial request; pre-fill form with current entry.
        form = QuestionForm(instance=question)

    else:
        # POST data submitted; process data.
        form = QuestionForm(instance=question, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('quora:category', args=[category.id]))

    context = {'question': question, 'category': category, 'form': form}
    return render(request, 'quora/edit_question.html', context)


# Define a view function for answering a question (requires login).
@login_required
def answer_question(request, question_id):
    question = Question.objects.get(id=question_id)
    category = question.category

    if request.method != 'POST':
        # Initial request; pre-fill form with question and answers.
        form = AnswerForm()

    else:
        # POST data submitted; process data.
        form = AnswerForm(data=request.POST)
        if form.is_valid():
            new_answer = form.save(commit=False)
            new_answer.owner = request.user
            new_answer.rating = 1
            new_answer.question = question
            new_answer.save()
            # change redirect page
            return HttpResponseRedirect(reverse('quora:list_answers', args=[question_id]))

    context = {'question': question, 'form': form, 'category': category}
    return render(request, 'quora/answer_question.html', context)


# Define a view function for liking/unliking an answer (requires login).
@login_required
def like_answer(request, answer_id):
    answer = Answer.objects.get(id=answer_id)
    user = request.user

    if user in answer.liked_by.all():
        # User has already liked this answer, so we unlike it
        answer.liked_by.remove(user)
        
    else:
        # User hasn't liked this answer, so we add the like
        answer.liked_by.add(user)

    return HttpResponseRedirect(reverse('quora:list_answers', args=[answer.question.id]))

