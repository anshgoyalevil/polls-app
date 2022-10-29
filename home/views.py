import re
from time import time
from django.http import HttpResponseRedirect
from django.shortcuts import render,get_object_or_404
from django.urls import reverse
from .models import Question,Choice,Vote
from django.db.models import F
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.datastructures import MultiValueDictKeyError

def index(request):
    if request.method=="POST":
        poll=request.POST['poll']
        question=Question.objects.filter(question_text=str(poll)).values()
        return render(request, 'home/index.html', {'latest_question_list': question})
    latest_question_list = Question.objects.order_by('-pub_date')
    context = {'latest_question_list': latest_question_list}
    return render(request, 'home/index.html', context)

def create(request):
    if request.method == "POST":
        poll_question=request.POST['poll_question']
        q=Question(question_text=poll_question,pub_date=timezone.now())
        q.save()
        count=1
        while True :
            try:
                poll_choice=request.POST['poll_choice'+ (str)(count)]
                choice=Choice(question=Question.objects.get(pk=q.id),choice_text=poll_choice,votes=0)
                choice.save()
            except  MultiValueDictKeyError:
                break
            count+=1

        # latest_question_list = Question.objects.order_by('-pub_date')
        # context = {'latest_question_list': latest_question_list}
        return HttpResponseRedirect(reverse('index'))
    if request.user.is_authenticated:
       return render(request,'home/create.html',{'hello':"hello"})
    else:
       return HttpResponseRedirect(reverse('login'))    

def detail(request, question_id):
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        raise get_object_or_404("Question does not exist")
    return render(request, 'home/detail.html', {'question': question})


def vote(request, question_id):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'home/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        if Vote.objects.filter(user=User.objects.get(pk=request.user.id)).exists() and Vote.objects.filter(poll=Question.objects.get(pk=question_id)).exists():
            return render(request, 'home/detail.html',{
                'question': question,
                'error_message': "You have already given Vote on this poll",
            })
        user_vote_at=Vote()
        user_vote_at.user=User.objects.get(pk=request.user.id)
        user_vote_at.poll=Question.objects.get(pk=question_id)
        user_vote_at.save()
        selected_choice.votes = F("votes") + 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('detail', args=(question.id,)))