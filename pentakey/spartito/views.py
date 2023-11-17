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


def get_darknet_path():
    current_path = os.getcwd()
    parent_directory = os.path.abspath(os.path.join(current_path, ".."))
    darknet_path = os.path.abspath(os.path.join(parent_directory, "darknet"))
    return darknet_path

def get_results_path():
    current_path = os.getcwd()
    results_path = os.path.abspath(os.path.join(current_path, "src/results"))
    return results_path

def get_src_path():
    current_path = os.getcwd()
    src_path = os.path.abspath(os.path.join(current_path, "src"))
    return src_path



def upload_spartito(request):
    if request.method == 'POST':
        form = SpartitoForm(request.POST, request.FILES)
        if form.is_valid():
            spartito = form.save()
            image_path = spartito.spartito_image.path
            darknet_path = get_darknet_path()

            # I improved the code, but it would still benefit from os.abspatthing even these ones
            darknet_exec_path = f'{darknet_path}/darknet'
            darknet_command = f'{darknet_exec_path} detector test {darknet_path}/data/obj.data {darknet_path}/yolov3-spp.cfg {darknet_path}/yolov3-spp_final.weights {image_path} -thresh 0.1 -out risultato.json'
            result = subprocess.run(darknet_command, shell=True, capture_output=True, text=True)
            print(darknet_command)
            print(os.getcwd())

            if result.returncode == 0:
                with open('risultato.json', 'r') as json_file:
                    riconoscimento = json_file.read()

                # Inserisci il risultato nel modello Spartito
                spartito.riconoscimento = riconoscimento
                spartito.save()

                results_folder = get_results_path()
                shutil.move('risultato.json', f'{results_folder}/risultato.json')
                shutil.move('predictions.jpg', f'{results_folder}/predictions.jpg')

                src_folder = get_src_path()
                subprocess.run(f'{src_folder}/run.py', capture_output=True)

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
    results_path = get_results_path()
    file_path = f"{results_path}/{image_name}.musicxml"
    file_name = f"{image_name}.musicxml"
    file = open(file_path, 'rb')
    response = FileResponse(file)
    response['Content-Type'] = 'application/vnd.recordare.musicxml'
    response['Content-Disposition'] = f'attachment; filename="{file_name}"'
    return response
