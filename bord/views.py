from django.shortcuts import render

def post_list(request):
    return render(request, 'bord/post_list.html', {})
