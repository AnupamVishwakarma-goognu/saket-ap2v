from django.shortcuts import render
from classroom.models import BatchStudentFeedback
from django.core.paginator import Paginator

# Create your views here.

def feedback(request):
    ctx={}
    feedback_obj = BatchStudentFeedback.objects.all().order_by("-id")

    paginator = Paginator(feedback_obj, 10)
    page_number = request.GET.get('page')
    try:
        feedback_obj = paginator.page(page_number)
    except:
        feedback_obj = paginator.page(1)
    
    ctx['feedback_obj']=feedback_obj
    return render(request,'feedback.html',ctx)