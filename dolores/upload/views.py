from django.shortcuts import render
from .forms import PartituraForm

def carica_partitura(request):
    if request.method == 'POST':
        form = PartituraForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
    else:
        form = PartituraForm()
    return render(request, 'upload/carica_partitura.html', {'form': form})
