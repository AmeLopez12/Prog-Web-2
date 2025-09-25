from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.urls import reverse
from .models import Question, Choice
from django.template import loader
from django.db.models import F
from django.views import generic

class GatoViewDetail (generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'

class ResultView (generic.DetailView):
    model = Question
    template_name = 'polls/results.html'
class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'
    queryset = Question.objects.order_by('-pub_date')[:5]
    

    
# Create your views here.
# def index(request):
#     lastest_question_list =  Question.objects.order_by('-pub_date')[:5]
    
#     template = loader.get_template('polls/index.html')
#     context = {
#         "latest_question_list": lastest_question_list,
#     }
#     return HttpResponse(template.render(context, request))
def index(request): 
    lastest_question_list =  Question.objects.order_by('-pub_date')[:5]
    context = {
        "latest_question_list": lastest_question_list,
    }   
    return render(request, 'polls/index.html', context)

    #output = ', '.join([q.question_text for q in lastest_question_list])
    #return HttpResponse(output)
    #return HttpResponse("Hello, world. You're at the polls index.")

def detail(request, question_id):
    #return HttpResponse("You're looking at question %s." % question_id)
    # try:
    #     question = Question.objects.get(pk=question_id)
    # except Question.DoesNotExist:
    #     raise Http404("Question does not exist")
    # return render(request, 'polls/detail.html', {'question': question})   
    return render (request, "polls/detail.html", { "question":   get_object_or_404(Question, pk=question_id)})
    
        

def results(request, question_id): 
    question = get_object_or_404(Question, pk=question_id)
    return render(request, "polls/results.html", {"question": question})

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render (
            request,
            'polls/detail.html',
            {
                'question': question,
                'error_message': "You didn't select a choice.",
            },
        )
    else:
        selected_choice.votes = F('votes') + 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
        