from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Equipamento

def index(request):
    return render(request, 'scanner/scan.html')


@csrf_exempt
def registrar_equipamento(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        codigo = data.get('codigo')
        if codigo:
            equipamento, criado = Equipamento.objects.get_or_create(codigo=codigo)
            return JsonResponse({
                'status': 'ok',
                'mensagem': 'Equipamento registrado com sucesso.' if criado else 'Equipamento já registrado.',
                'criado': criado
            })
        else:
            return JsonResponse({'status': 'erro', 'mensagem': 'Código inválido'}, status=400)
    return JsonResponse({'status': 'erro', 'mensagem': 'Método não permitido'}, status=405)