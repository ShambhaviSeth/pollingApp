from django.test import TestCase
from .forms import QuestionForm
from .models import Question, Choice
from django.urls import reverse

class QuestionFormTest(TestCase):
    def test_form_valid(self):
        form_data = {
            'question_text': "What's your favorite color?",
            'pub_date': "2024-10-20"
        }
        form = QuestionForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_form_invalid_without_question_text(self):
        form_data = {
            'question_text': '',
            'pub_date': "2024-10-20"
        }
        form = QuestionForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('question_text', form.errors)

    def test_form_invalid_without_pub_date(self):
        form_data = {
            'question_text': "What's your favorite color?",
            'pub_date': ''
        }
        form = QuestionForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('pub_date', form.errors)


class VoteViewTest(TestCase):
    def setUp(self):
        self.question = Question.objects.create(
            question_text="What's your favorite color?",
            pub_date="2024-10-20"
        )
        self.choice = Choice.objects.create(
            question=self.question,
            choice_text="Blue",
            votes=0
        )

    def test_vote_increments_choice_votes(self):
        response = self.client.post(reverse('polls:vote', args=(self.question.id,)), {'choice': self.choice.id})
        self.choice.refresh_from_db()
        self.assertEqual(self.choice.votes, 1)

    def test_vote_redirects_to_results(self):
        response = self.client.post(reverse('polls:vote', args=(self.question.id,)), {'choice': self.choice.id})
        self.assertRedirects(response, reverse('polls:results', args=(self.question.id,)))
