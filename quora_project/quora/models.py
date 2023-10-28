from django.db import models
from django.contrib.auth.models import User

# Define a model for categories
class Category(models.Model):
    text = models.CharField(max_length=30) # Field for the category name
    date_added = models.DateTimeField(auto_now=True) # Field for the date the category was added

    class Meta:
        verbose_name = 'Category' # Singular name of the model
        verbose_name_plural = 'Categories' # Plural name of the model

    def __str__(self):
        return self.text # String representation of the category, returns its name


# Define a model for questions
class Question(models.Model):
    category = models.ForeignKey(Category, on_delete=models.PROTECT) # ForeignKey to associate questions with categories
    text = models.TextField() # Field for the question text
    date_added = models.DateTimeField(auto_now=True) # Field for the date the question was added
    owner = models.ForeignKey(User, on_delete=models.PROTECT) # ForeignKey to associate questions with owners (users)

    class Meta:
        verbose_name = 'question' # Singular name of the model
        verbose_name_plural = 'questions' # Plural name of the model

    def __str__(self):
        if len(self.text) > 150:
            return self.text[:150] + "..." # Return a truncated question text if it's too long
        else:
            return self.text


# Define a model for answers
class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.PROTECT) # ForeignKey to associate answers with questions
    text = models.TextField() # Field for the answer text
    date_added = models.DateTimeField(auto_now=True) # Field for the date the answer was added
    owner = models.ForeignKey(User, on_delete=models.PROTECT) # ForeignKey to associate answers with owners (users)
    rating = models.PositiveIntegerField() # Field for the answer's rating
    liked_by = models.ManyToManyField(User, related_name='liked_answers', blank=True) # Many-to-Many relationship to track users who liked the answer

    def __str__(self):
        if len(self.text) > 250:
            return self.text[:250] + "..." # Return a truncated answer text if it's too long
        else:
            return self.text


