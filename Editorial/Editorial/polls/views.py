from django.shortcuts import render
from .forms import PollForm

def poll_create(request):
    form = PollForm()
    return render(request, "polls/submit.html", {"form": form})