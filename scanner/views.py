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
        codigos = data.get('codigos')
        if not codigos:
            # Suporte ao envio antigo (um código só)
            codigo = data.get('codigo')
            if codigo:
                codigos = [codigo]
            else:
                return JsonResponse({'status': 'erro', 'mensagem': 'Nenhum código enviado.'}, status=400)
        
        # Dados do modal
        peso_liquido = data.get('peso_liquido')
        peso_bruto = data.get('peso_bruto')
        medidas_caixa = data.get('medidas_caixa')
        
        criados = []
        for codigo in codigos:
            equipamento = Equipamento.objects.create(
                codigo=codigo,
                peso_liquido=peso_liquido,
                peso_bruto=peso_bruto,
                medidas_caixa=medidas_caixa
            )
            criados.append({'codigo': codigo, 'criado': True})
        return JsonResponse({
            'status': 'ok',
            'mensagem': f'{len(criados)} código(s) processado(s).',
            'resultados': criados
        })
    return JsonResponse({'status': 'erro', 'mensagem': 'Método não permitido'}, status=405)