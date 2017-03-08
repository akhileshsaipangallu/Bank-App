from django.shortcuts import render


def home_page(request):
    context = {'user': request.user}
    return render(request, 'bank/home_page.html', context)
