from django.shortcuts import render
from django.http import JsonResponse
from .models import CodigoEscaneado
from django.views.decorators.csrf import csrf_exempt
import json

def scanner_view(request):
    return render(request, 'scanner/scan.html')

@csrf_exempt
def salvar_codigo(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        codigo = data.get('codigo')
        tipo = data.get('tipo')
        CodigoEscaneado.objects.create(codigo=codigo, tipo=tipo)
        return JsonResponse({'status': 'salvo com sucesso'})
    return JsonResponse({'erro': 'requisição inválida'}, status=400)
