from django.shortcuts import render, redirect
from .forms import SpartitoForm
import subprocess
from django.http import HttpResponse, JsonResponse
import shutil
from django.http import FileResponse
from django.shortcuts import get_object_or_404
from .models import Spartito
import os
from django.core.files.storage import FileSystemStorage
from django.shortcuts import redirect
from django.http import FileResponse


def upload_spartito(request):
    if request.method == 'POST':
        form = SpartitoForm(request.POST, request.FILES)
        if form.is_valid():
            spartito = form.save()
            image_path = spartito.spartito_image.path
            darknet_path = '/home/musimathicslab/Scrivania/CacciaNegriRapa/darknet/darknet'
            darknet_command = f'{darknet_path} detector test /home/musimathicslab/Scrivania/CacciaNegriRapa/darknet/data/obj.data /home/musimathicslab/Scrivania/CacciaNegriRapa/darknet/yolov3-spp.cfg /home/musimathicslab/Scrivania/CacciaNegriRapa/darknet/yolov3-spp_final.weights {image_path} -thresh 0.1 -out risultato.json'
            result = subprocess.run(darknet_command, shell=True, capture_output=True, text=True)

            if result.returncode == 0:
                with open('risultato.json', 'r') as json_file:
                    riconoscimento = json_file.read()

                # Inserisci il risultato nel modello Spartito
                spartito.riconoscimento = riconoscimento
                spartito.save()

                shutil.move('risultato.json', '/home/musimathicslab/Scrivania/CacciaNegriRapa/pentakey/src/results/risultato.json')
                shutil.move('predictions.jpg', '/home/musimathicslab/Scrivania/CacciaNegriRapa/pentakey/src/results/predictions.jpg')

                subprocess.run("/home/musimathicslab/Scrivania/CacciaNegriRapa/pentakey/src/run.py", capture_output=True)
                
                request.session['image_name'] = image_path.split('/')[-1]
                
                return redirect("download_file")

            else:
                return JsonResponse({'error': 'Errore durante il riconoscimento oggetti'})
    else:
        form = SpartitoForm()
    return render(request, 'upload_spartito.html', {'form': form})

def download_spartito(request, pk):
    spartito = get_object_or_404(Spartito, pk=pk)
    musicxml_file = spartito.musicxml_file
    response = FileResponse(musicxml_file)
    return response

def accesso_pagina_upload(request):
    form = SpartitoForm()
    return render(request, 'sessionupload_spartito.html', {'form': form})

def download_file(request):
    image_name = request.session.get('image_name').split('.')[0]
    file_path = f"/home/musimathicslab/Scrivania/CacciaNegriRapa/pentakey/src/results/{image_name}.musicxml"
    file_name = f"{image_name}.musicxml"
    file = open(file_path, 'rb')
    response = FileResponse(file)
    response['Content-Type'] = 'application/vnd.recordare.musicxml'
    response['Content-Disposition'] = f'attachment; filename="{file_name}"'
    return response
