from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required, permission_required
from django.urls import reverse_lazy
from django.core.paginator import Paginator
from django.db.models import Q
import json
from .models import Equipamento
from core.models import EventoTratado

@login_required(login_url='login')
@permission_required('scanner.can_access_scanner', login_url='login')
def index(request):
    return render(request, 'scanner/scan.html')


@csrf_exempt
@login_required(login_url='login')
@permission_required('scanner.can_access_scanner', login_url='login')
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
                medidas_caixa=medidas_caixa,
                usuario_cadastro=request.user
            )
            criados.append({'codigo': codigo, 'criado': True})
        return JsonResponse({
            'status': 'ok',
            'mensagem': f'{len(criados)} código(s) processado(s).',
            'resultados': criados
        })
    return JsonResponse({'status': 'erro', 'mensagem': 'Método não permitido'}, status=405)

from django.contrib.auth.decorators import login_required, permission_required

@login_required(login_url='core:login')
@permission_required('scanner.can_access_scanner', login_url='core:login')
@permission_required('core.can_access_eventos',   login_url='core:login')
def historico_equipamentos(request):
    """
    View para exibir o histórico de equipamentos do usuário logado
    """
    # Filtros
    codigo_filter = request.GET.get('codigo', '')
    tipo_filter = request.GET.get('tipo', '')
    data_inicio = request.GET.get('data_inicio', '')
    data_fim = request.GET.get('data_fim', '')
    
    # Query base - apenas equipamentos do usuário logado
    equipamentos = Equipamento.objects.filter(usuario_cadastro=request.user)
    
    # Aplicar filtros
    if codigo_filter:
        equipamentos = equipamentos.filter(codigo__icontains=codigo_filter)
    
    if tipo_filter:
        equipamentos = equipamentos.filter(tipo_equipamento=tipo_filter)
    
    if data_inicio:
        from datetime import datetime
        try:
            data_inicio_obj = datetime.strptime(data_inicio, '%Y-%m-%d')
            equipamentos = equipamentos.filter(data_recebido__date__gte=data_inicio_obj.date())
        except ValueError:
            pass
    
    if data_fim:
        from datetime import datetime
        try:
            data_fim_obj = datetime.strptime(data_fim, '%Y-%m-%d')
            equipamentos = equipamentos.filter(data_recebido__date__lte=data_fim_obj.date())
        except ValueError:
            pass
    
    # Ordenar por data mais recente
    equipamentos = equipamentos.order_by('-data_recebido')
    
    # Paginação
    paginator = Paginator(equipamentos, 20)  # 20 equipamentos por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Estatísticas do usuário
    total_equipamentos = Equipamento.objects.filter(usuario_cadastro=request.user).count()
    total_guardians = Equipamento.objects.filter(usuario_cadastro=request.user, tipo_equipamento='guardian').count()
    total_sensores = Equipamento.objects.filter(usuario_cadastro=request.user, tipo_equipamento='sensor_porta').count()
    total_tetis = Equipamento.objects.filter(usuario_cadastro=request.user, tipo_equipamento='tetis').count()
    
    context = {
        'equipamentos': page_obj,
        'total_equipamentos': total_equipamentos,
        'total_guardians': total_guardians,
        'total_sensores': total_sensores,
        'total_tetis': total_tetis,
        'codigo_filter': codigo_filter,
        'tipo_filter': tipo_filter,
        'data_inicio': data_inicio,
        'data_fim': data_fim,
        'tipos_choices': Equipamento.TIPO_CHOICES,
    }
    
    return render(request, 'scanner/scan_historico.html', context)
