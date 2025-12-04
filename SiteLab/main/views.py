from django.shortcuts import render
# from portfolios.models import Review 

# def home(request):
#     top_reviews = Review.objects.filter(rating=5)[:3]  
#     return render(request, 'main/index.html', {'top_reviews': top_reviews})

def home(request):
    return render(request, 'main/index.html')

def our_services(request):
    return render(request, 'portfolios/our-services.html')
