from django.shortcuts import render
from django.http import HttpResponse
from django.template.loader import render_to_string, get_template
from django.core.mail import send_mail, EmailMessage
from .forms import *
from .models import *

#index function is not used

def index(request):

    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {'latest_question_list': latest_question_list}
    return render(request, 'polls/index.html', context)


def detail(request, qid):
    context = Question.objects.filter(pk=qid)
    if context.count()==0:
        return render(request, 'polls/no-page.html', {})

    if request.method == 'POST':
        answer = request.POST["answer"]
        if answer == '':
            return render(request, 'polls/detail.html', {'context': context, 'c':1})

        print(answer)
        #after this, the user will get notifications.
        #notification function not yet built
        context = Question.objects.get(pk=qid).delete()

        return render(request, 'polls/detail.html', {'context': context, 'c':0})


    else:

        return render(request, 'polls/detail.html', {'context': context, 'c':1})


def query_view(request):
    form = Queryform(request.POST or None)
    if form.is_valid():
        form.save()
        form = Queryform()
    return render(request, 'polls/queryform.html', {'form': form})


def adminpage(request):
    latest_question_list = Question.objects.order_by('-pub_date').values()
    c = latest_question_list.count()
    return render(request, 'polls/adminpage.html', {'latest_question_list': latest_question_list, 'c':c})

# def sendmail(request):
#     if request.method == 'POST':
#
#         text=request.POST['answer']
#         x=request.POST['email']
#         subject="Here is your answer"
#         message=text
#         to_email=x
#         from_mail= 'ruthala.shiva512@gmail.com'
#         EmailMessage(subject, message, to_email, from_mail).send()




def result(request):
    answer = request.POST["answer"]
    Answer.objects.create(answer=answer)

    return HttpResponse("Your answer is :{}".format(answer))

