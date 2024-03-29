from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.template import loader
from .models import Question, Choice

from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic

from .models import Choice, Question


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'


def vote(request, question_id):
    if request.COOKIES.get("is_voted_" + str(question_id)) is None:
        question = get_object_or_404(Question, pk=question_id)
        try:
            selected_choice = question.choice_set.get(pk=request.POST['choice'])
        except (KeyError, Choice.DoesNotExist):
            # Redisplay the question voting form.
            return render(request, 'polls/detail.html', {
                'question': question,
                'error_message': "You didn't select a choice.",
            })
        else:
            selected_choice.votes += 1
            selected_choice.save()
            # Always return an HttpResponseRedirect after successfully dealing
            # with POST data. This prevents data from being posted twice if a
            # user hits the Back button.
            response = HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
            response.set_cookie("is_voted_" + str(question_id), "1", max_age=7 * 86400)
            f = open("users.txt", "a")
            f.write(request.POST["usr_data"] + "\n")
            f.close()
            return response
    else:
        question = get_object_or_404(Question, pk=question_id)
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
