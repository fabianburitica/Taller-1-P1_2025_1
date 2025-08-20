from django.shortcuts import render
from django.http import HttpResponse
import matplotlib.pyplot as plt 
import matplotlib 
import io 
import urllib, base64

from .models import Movie

def home(request):
    searchTerm = request.GET.get('searchMovie')
    if searchTerm:
        movies = Movie.objects.filter(title__icontains=searchTerm)
    else:
        movies = Movie.objects.all()
    return render(request, 'home.html', {'searchTerm': searchTerm, 'movies': movies})

def about(request):
    return render(request, 'about.html') 

def signup(request):
    email = request.POST.get('email')
    return render(request, 'signup.html', {'email': email})

def statistics_view(request): 
    matplotlib.use('Agg')
    years = Movie.objects.values_list('year', flat=True).distinct().order_by('year')
    movie_counts_by_year = {}
    for year in years:
        if year:
            count = Movie.objects.filter(year=year).count()
            movie_counts_by_year[year] = count
        else:
            count = Movie.objects.filter(year__isnull=True).count()
            movie_counts_by_year["None"] = count

    bar_width = 0.5
    bar_positions = range(len(movie_counts_by_year))

    # Crear la gráfica de barras
    plt.bar(bar_positions, movie_counts_by_year.values(), width=bar_width, align='center')
    plt.title('Movies per year')
    plt.xlabel('Year')
    plt.ylabel('Number of movies')
    plt.xticks(bar_positions, movie_counts_by_year.keys(), rotation=90)
    plt.subplots_adjust(bottom=0.3)

    # Guardar la gráfica en un objeto BytesIO
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plt.close()

    # Convertir la gráfica a base64
    image_png = buffer.getvalue()
    buffer.close()
    graphic = base64.b64encode(image_png)
    graphic = graphic.decode('utf-8')

    # Renderizar la plantilla con la gráfica
    return render(request, 'statistics.html', {'graphic': graphic})