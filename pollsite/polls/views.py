#from django.shortcuts import render

# Create your views here.
from django.http import HttpResponseRedirect, HttpResponse
from django.template import loader
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

from .models import Choice, Question

def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    #output = ', '.join([q.question_text for q in latest_question_list])
    ##template = loader.get_template('polls/index.html')
    context = {
        'latest_question_list': latest_question_list,
    }
    #return HttpResponse(output)
    ##return HttpResponse(template.render(context, request))
    return render(request, 'polls/index.html', context)


def testpage(request):
    return HttpResponse("this is the test page.")

def detail(request, question_id):
    #2try:
    #2    question = Question.objects.get(pk = question_id)
    #2except Question.DoesNotExist:
    #2    raise Http404("Question does not exist")
    #1return HttpResponse("You're looking at the question %s." % question_id)
    question = get_object_or_404(Question, pk = question_id)
    return render(request, 'polls/detail.html', {'question' : question})

def results(request, question_id):
    #response = "You're looking at the results of question %s."
    #return HttpResponse(response % question_id)
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question' : question})


def vote(request, question_id):
    question = get_object_or_404(Question, pk = question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        #redisplay question voting form
        return render(request, 'polls/detail.html', {'question' : question,
                                                     'error_message': "You didn't select a choice"})
    else:
        selected_choice.votes += 1
        selected_choice.save()
    return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))