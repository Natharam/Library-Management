from django.shortcuts import render

def my_view(request):
    # View code here...
    return render(request, 'index.html', {
        'foo': 'bar',
    }, content_type='application/xhtml+xml')