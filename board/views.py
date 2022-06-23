from django.shortcuts import render

# Create your views here.

from member.models import Member

def list(request):
   returnPage = 'board/list.html'

   if (request.method == 'GET'):
        return render(request, returnPage)
   elif (request.method == 'POST'):
        pass
   return render(request, 'board/list.html')

def view(request):
    return render(request, 'board/view.html')

def write(request):
    return render(request, 'board/write.html')
