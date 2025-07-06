from django.shortcuts import render
import requests  # Importação correta da biblioteca
from .models import altocafezalmodel, EventoTratado
from .forms import AltocafezalModelForm
# Create your views here.
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import TemplateView,CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from urllib.parse import urlencode
from urllib.request import Request, urlopen
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods, require_GET
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.utils.timezone import now

# Página inicial (apenas para usuários autenticados)
class HomeView(LoginRequiredMixin, TemplateView):
    template_name = "core/home.html"
    login_url = reverse_lazy("login")  # Redireciona para login se não autenticado

# Página de Login (Django já fornece um formulário embutido)
class CustomLoginView(LoginView):
    template_name = "core/login.html"
    redirect_authenticated_user = True  # Se já estiver logado, redireciona para home

# Página de Logout (Django já gerencia isso internamente)
class CustomLogoutView(LogoutView):
    next_page = reverse_lazy("login")
    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)# Após logout, redireciona para login


class MapaView(TemplateView):
    template_name = "core/mapa.html"
    
    
import requests
from django.shortcuts import render
from django.http import JsonResponse

# URL da API T42 Online
T42_API_URL = "https://mongol.brono.com/mongol/api.php"
T42_USER = "wimc_u_nestle"
T42_PASS = "Inte@20xx"

def get_t42_data(request):
    """Busca os dados da API T42 e retorna como JSON para o frontend."""
    # Pega o ID da querystring (se existir)
    search_id = request.GET.get('id', '').strip()
    
    params = {
        "commandname": "get_last_transmits",
        "user": T42_USER,
        "pass": T42_PASS,
        "format": "json"
    }

    try:
        response = requests.get(T42_API_URL, params=params)
        response.raise_for_status()  # Garante que a resposta foi bem-sucedida
        data = response.json()

        # Se foi passado um ID, filtra os resultados
        if search_id:
            if isinstance(data, list):
                filtered_data = [unit for unit in data if str(unit.get('unitnumber', '')) == search_id]
            else:
                filtered_data = []
            return JsonResponse(filtered_data, safe=False)
        
        # Se não foi passado ID, retorna todos os dados (comportamento original)
        return JsonResponse(data, safe=False)

    except requests.RequestException as e:
        return JsonResponse({"error": str(e)}, status=500)

def get_assetscontrols_data(request):
    """Busca os dados da API AssetsControls e retorna como JSON para o frontend."""
    # Pega o ID da querystring (se existir)
    search_id = request.GET.get('id', '').strip()
    url = 'http://cloud.assetscontrols.com:8092/OpenApi/LBS'
    data = {
        'FAction': 'QueryLBSMonitorListByFGUIDs',
        'FTokenID': '7e88e035-285a-4f7d-8e63-8b403d04dcfa',
        'FGUIDs': '97933c2d-f9f1-4658-8fd9-0c8ad3dc105c,bf94a122-1ce7-4071-acc4-18febda1ad8c,20f159f4-66bf-4278-8e59-2003ae9d734e,aeb4d39f-5faf-4780-99ab-2f0aa27d47db,e0a09aa5-4653-474e-84cd-581085e1cea4,d1322bab-b251-4eff-9d6d-596962005030,a2414d4e-970c-42e9-90b0-831ac7551985,585a7b14-941d-4931-b764-ab2ae0b1cd80,4a689931-ab7a-4a79-a839-befa2abcc1b0,92c65682-c94e-46c3-8f17-c39f638db9d9,91009f10-35a8-4b1a-a045-001c412cd794,54b1afbd-ae71-4fa0-9303-00306c19b38c,fda29cc4-0ba1-4236-965c-00d942714e3b,7d60b779-1bd3-4399-aaec-0241c1ec585e,afd2523a-444b-4d8e-9175-02bfd59aa46e,f50b59f2-2803-43a4-b52e-02cebb70120c,3d34f75d-2ec6-413c-b1c7-02f0a2864eff,0a079858-581d-4729-aa74-0388daed2b5a,d6a2607d-138f-4428-8f4b-03ecf1398238,e2f40e62-bada-490f-8595-040bbd3796a8,b473d71f-916a-4be7-9f98-04f5d42704b7,51f80574-60fb-4344-8888-0536eafd830c,ce4a9b98-74de-4c5c-9241-05d0746bb22e,82a69abd-0e72-4a1a-9b67-0602b98fc1ce,73951b95-9242-4be6-8c24-064303cd4e3e,46f19326-a4ed-4c35-9f9f-06485dead378,f1dea8e6-a020-483a-865d-065b14fe80ea,51559c7e-53b1-48da-923f-070e00bc0f75,cf257309-8465-491c-9cc6-07dd150d4b66,56df06ea-74d0-4875-aa81-083832d32555,70e08d0a-474e-46c5-85ce-08ad926719dd,5a7d0f7f-c07c-40d8-a2e6-08e15e5909d0,96f33dae-409b-4268-bbeb-08e240ca23e6,be835ad3-402d-4390-96ca-097254ec4b5c,411b98b7-bc09-41e3-86bc-09c93c9765e4,43bfa406-1a8e-4349-9954-0a4259370e8a,c70488f9-8f57-4e71-ac2f-0b759331a1fe,c994176c-5998-445d-b1ec-0c2a84a6b9ee,344d4e7a-3a3d-4dd4-873e-0ca9ec6f60cd,4624979f-e795-4a1f-a285-0cac44641c10,67495bd7-3838-4eb7-80eb-0cd877179e74,5da3ea45-a51f-4224-96ba-0d66e9f50ac5,56d24f97-8b1c-4af2-8d2a-0dd0589dceec,7c504180-4210-4936-8dc5-0ea5b605e138,647ffa0f-6833-4b82-90d5-0f57653e3859,241325b6-a7a6-4f79-8a79-0f7aa2f2310b,d34d5ab2-3fb7-4ba0-8ab3-0ff871df4b03,52c67c28-b157-48f4-9ba3-10832b095574,97c19e63-b02c-492f-9b85-1084ad48994c,5cd99c28-5251-4e32-8476-10c5e33325ce,dd442599-01ef-4160-a0a1-10cdc8144ec5,754ae63e-2a03-41db-a199-10f3eebbdc32,0e365048-3479-4111-a6ac-117f6d65c615,2468048a-f3b1-456d-b949-1232740508a1,9244ce88-deca-4b65-b3b5-12c3847ab0ea,e47ffa82-74e4-4898-b46b-1404c334a75b,f0d11885-b7db-4565-a7d1-14f3e8faa362,b6f21817-a416-49de-9ce2-15954ec83b33,57c48ac9-5fee-4fb6-928b-15b971f47f81,40c976b6-f85d-4755-ac00-1620555fefab,d6897c1e-ed3c-40b2-9d5e-16ba8e678be6,39d05d02-5f7d-4c44-be11-16f773eba605,1bd991df-9c57-4b97-a779-1779c04d316d,c375c7b7-f665-4d6f-9e47-179288a13958,20e35b33-9448-4a6f-a725-179ead2564bf,00dbed07-acc1-4059-83ab-17ad3e84fa4d,09a7f409-772c-4344-a4b3-1866b1516200,769e2655-634a-4d4e-8c5b-186ba9a3ba4d,9d977a5a-67fb-44ed-b97e-18800e968cbe,6a416a2c-e13f-419f-b24e-18f2c21c6cae,5bfe3786-89f5-4551-baa6-196e7c77e85c,9ec57328-1357-49b5-9062-197707cba955,daa7baeb-dc56-432e-9eb4-1984f3a88022,46663109-d1ea-4691-a6b5-19cee1f6e59a,e1a86773-d708-4b88-943f-1a9959b4cd3d,51af26dc-b3aa-4fd2-bcd4-1b1d15eb2944,676e0cb8-adc4-401c-9b41-1c3ad89db3e2,25ed1315-6034-4692-9701-1cf6342f6e24,756b3475-146e-4d3d-a254-1d351d39581c,d9c79614-e3e6-4c4d-a955-1d52ebf65c50,5fdb0ec4-e086-4ae3-b779-1d7677dd4d0e,3cf52c42-18d6-4d29-af8a-1de092366cf0,bd3c3e22-a785-48e4-b8ba-1e99ca6cc810,2813b503-18f0-47f4-bb73-1f53c5b6b826,cbbfde13-22ad-4bdf-af7d-1fbcee0127dc,eab75cec-ee75-475d-83be-20011d0f78ff,d2bb9c99-f7fa-4f21-9342-21f2b01ce519,62ee3a95-2c2e-474a-a53c-23b70f20eb44,b1389da4-12cd-4cd9-8336-267a1fb9f6f9,895bccbd-bdd6-484c-8c87-27b24f91552a,377f3c3f-2960-4907-9be2-27e06f4c7885,9959690b-75e2-4d33-9f25-280020418ab4,4ba7eeef-2d41-42df-8ac3-2807a4e93dd6,8fe29085-ebc5-42ee-88be-2837e0a0e45c,4d06512c-7851-4cf8-b497-28bae70e8078,54925049-282f-4d56-8163-29107f796a44,4eac3ad0-25c5-4f09-afe8-2921ad426e40,eea7031d-bed8-49ba-963d-29a2ba6a44c3,5c52cb5a-d665-4eff-ad06-29ab0e0f9370,e35a5d02-b84a-4ada-a9f1-2a16c1e28c38,3f55a43b-0b72-483a-92e2-2a24a5dd6781,70b69222-89f0-406b-a88a-2b1d53c1d082,0bf33daa-2b47-49c7-95d6-2b388f662d7c,141222df-3f85-44d9-94be-2b42f082c8a4,b93ac0ef-036c-4e43-b6f1-2b5fe57d516d,ce9aea73-b8d0-484d-98b4-2c02338e2fb7,9100602d-4280-4f1e-ae1a-2e875e879b67,371cef0e-7abe-4bd1-9312-2f2271f37040,3feac813-ae88-4fce-b1fc-2fe2acedfc4c,205d57ed-eb9f-4117-bbea-3048c81b2b99,39365fca-53a5-4b5b-8d76-30b4c1cbf20b,577f0e8c-0a0c-4b37-af89-30b8a6d85511,1cf6c89f-c20f-4111-8739-31476b0fc574,ea14d948-f7fa-4438-a676-318c221d31c2,f4059c5e-b48c-4947-91ed-3195e208055a,39acfae7-1c4f-4b87-9b12-31ec83513c03,118e9b58-1742-4ed2-b431-32103de0c9de,28b357b1-0642-4390-a29d-321f6e8067a4,9c212a0a-3d92-4066-8d5a-33077980af66,841bbb9c-5c35-42c2-a822-3339605eb25e,203b7685-684e-457f-8bb4-33c4b05c4006,040eda56-e34d-4304-9edd-3469a796edd9,905800fc-1c09-491b-933d-34a4199e0f3a,b669adba-92fc-442e-b766-3511ea238346,5071b4c4-6a30-4a86-baa0-35d9436e0037,e83bcc0f-a5f2-4a69-9fc1-37449f4c9310,7ab1620c-fe16-47cf-a064-37eb58f2da1e,eea313a8-bcea-4705-a074-39b94c12bd9b,a45cf359-afb9-49d2-aaa6-39d3862234ce,bca63af2-571d-457f-af65-3a6632aa34a3,42c5cf00-9ae0-4fc7-9bd1-3af2cbe76d35,fe8ecde4-0877-4f98-80af-3b1ffda40e2f,1a653368-048f-4aef-80d6-3b2eb767df7e,0c78d1a9-2f01-4942-8986-3c7d40e2ebc0,36108189-bf2c-4cd3-880c-3caccf587978,b8cb3ad0-d093-4f43-b3ec-3f718dbdfcd6,2a0a6660-6866-461b-927e-3f8ce2fb3820,58a15f73-5d96-4d5d-9b77-407e3bbd2635,1f07e085-6db5-4020-ae33-411829a3c848,2fb702e8-21f0-4c14-97f1-413795e5e863,eb4ea184-d2c6-4d00-9f71-41429200823d,9fbf0d51-2ea0-4c21-a74c-428fe09cb3d3,0dd108a9-3a94-4042-a9c6-42cee6ad51a1,d8d1283f-6c00-413d-ae82-4306f5549a15,4a7a0a2a-ce57-4422-862b-4343fa6b9e88,2f33f05a-04a5-4a42-a463-439b106494de,d6b380fb-2533-493a-922f-43af0cde52e4,8a78aff4-6f82-4ac3-8106-4482f464c589,67d022f9-e818-4209-9810-44989aae02f7,8c127361-bf07-4448-aa9a-44a1686815a4,bcdc56ee-d89c-42f4-96e6-4559ed5c9583,3441e6f1-2cab-442b-95e3-458c50160ce4,b0b0be2f-973e-4f2d-b282-45e285411280,fb4f7498-93b3-4a72-bc36-461ae68d505c,172dde98-3b1f-430d-92b4-46ef0eeaf2cc,c4c5a355-6811-4344-9aa8-46f8d19d97c3,3f93cfe5-22c8-458a-b8ca-47041b1af3ff,405a0613-7d2f-4936-af76-4927aecd49ca,5ec73f39-d393-4020-addc-4970d4a9c63e,e32ee64d-8693-48f1-9809-49d63b35870e,e924acc3-70f2-4c69-adec-4a107d4a90ed,2e5d50ee-187b-40b7-a2e8-4a84f3c5951c,db4e6b0d-e518-4abe-8c50-4a931179e507,f5471c1d-9b42-48e8-8e03-4aa350c0ba87,943fed1c-3563-44a7-a2dc-4ae121be2300,abde4d3c-6478-457c-8d55-4b0d9bb1fec0,320c89ff-a096-4dd2-97a4-4b67408e0453,e8c25268-28ef-4b54-86d7-4b80296810f7,6a60c567-54f9-41e4-92dd-4c0c528d5010,e21328e5-b431-4742-bdc1-4c35c8ade665,6df270e9-28d2-4a91-8f22-4c70f1b60c82,b74a5aa8-fbb6-42d1-8017-4e30002b9a1c,ce16b652-46fc-47b1-bc6a-4e6c5037ca9b,79c81472-a99d-4580-be4c-4ec7a1fb0e95,7bffbdcd-28a8-42ec-98cb-4ecf6abb21ef,241cfdc1-9604-4cb4-b00c-4f4302dadd9b,2a2802e4-d800-4a3d-b77c-500d8e8cdcd6,675f48d0-9f14-4df7-b10e-502fcce81f7c,bb482b8a-0e0b-4852-887b-50456550755e,065ff8ac-2e43-47bf-8fea-50f758ae5730,6ac25de8-e62f-4a88-8cca-519c46fb6a94,c275b75b-514f-454c-afd6-527e07741249,c5655eb8-c46d-4537-a77d-528d928e4c46,93123d06-527b-4525-80ef-53117590ec27,f8ba99a4-c712-49ff-96d3-543a9a7cf046,215deb0c-ffec-4f05-b593-54480078e021,db3bffa2-5889-48b4-b5c0-54ce7a6b71a1,c4040ea2-6bb7-491c-afe8-54ecd2ea5a98,27c24a62-b37d-446d-9f18-557a469fdaa2,5bcd1c27-3457-4d96-a55b-55d880a034d1,b0be6c6c-3ff6-4ad2-8e8c-576acdd87ffc,54c2d991-29d1-40b0-9a52-57c8561299e6,aa9cc3b4-fada-4ce3-9558-57d99f81bf7c,5627a295-7eb5-4685-a56a-585bad816f3a,53467c23-2494-44db-91e2-58aaabac7f2a,f2719b36-22d1-4582-a013-595134c1b2c8,87a1719b-c078-4c59-8189-5a61414a3f6a,263a29d7-81e5-48da-8a7a-5ae74d087e62,f5336afb-7492-4d2c-af56-5b44aaee8d34,a41531b0-46e9-4b06-bc74-5b5c9d2e9b1b,cd8e269b-9e7f-498d-9484-5b8211a8ca79,ccaf0a2d-75d8-4a1a-aa55-5c1bceb809b7,2167fe3d-4ee0-43fe-a244-5d12bb1cd961,0aa0100e-78ce-41e4-b349-5de53ddc2d37,66392dab-eb22-4d14-adec-5e22e63c2a76,b85b5434-2335-4cc4-81ae-5e47e12f81cb,36a11f52-3f37-41a5-a7fe-5edd967bd891,a46c057e-d4e0-41bb-be3b-5f6cfe1e9a96,5be055fe-ddc5-44a6-aa79-5f834c1264e9,32672408-0a38-4b60-bad7-5fb9df478882,94f551d1-0cfb-45cc-af24-603f1da122f5,86030a41-16a1-4ddb-b301-606cce83c318,d96adc40-08c8-46ee-a900-60fee0899f38,97f41cc5-ece3-49a4-9adb-61211a7e16f2,9284c236-6602-4d3b-a13c-61566fb64292,d9c12fe0-c594-42cf-807a-61dbf15f9b8d,a4b91818-3f01-45da-baca-624f865fb4e8,fef71809-4012-46ff-bfd8-633f9872a11e,a7f525a5-c9b5-41fa-847b-637fc7f56097,5d871a79-d83c-4463-a3c8-63c61eb6b655,5c5c77ad-6983-46c8-8341-63e8aabf165d,b48a065f-f62b-4f54-81c2-63e94c4b0bd6,a091acff-bb65-415d-8670-63f1df0d5602,41e2326d-c3da-4768-b6f3-641564bd1f84,802102b5-3664-4855-ae58-645646399d4d,ee803e29-174a-4988-b255-649d962a398a,7728f13b-3e45-41fc-b14b-658f8598b261,e43204db-6af6-4169-b64d-65cc8cbbfc19,3d037c95-8f47-4c1e-ae1c-669151b5100e,16901911-a4f3-4ad3-ad6e-6702dab2f25a,c03d8936-5dc4-473f-906b-6796c92d5e88,6d75c5ef-b609-48ab-be2a-67ba3b8eb7da,0d149b5d-9781-46de-ae2f-67d7a28da796,8bb3ca2f-14e3-4dd0-ba1e-6804501b6ede,73147234-c8c9-45fd-a162-686e132c9d46,223aafe1-8f7a-43f8-9620-688ea3e92e2e,13a3e3fa-064e-496a-9007-695314ef644a,1f0c6a2e-9c3f-454c-ab42-699e9cdd00ac,a2e59588-bbe1-4316-992c-6a64d674d798,4754d5a0-1ff7-427b-8600-6bb5d817a889,f26b52ad-0f7f-4237-90f3-6c26b03b2fb3,f55e0e9c-68d7-4da4-8bc6-6c2f41dfbec2,92da58dd-6b02-4024-a53f-6d39354233eb,2e1031b1-dbd6-40f4-9d02-6dec4546ee61,aac58cda-79b3-403c-95a5-6f0554b8c04b,7ffdca9e-08c0-4f61-84bd-6fa11a550f73,76cb4220-11e1-4db7-b70d-7085d489ac9b,16810e05-439e-4eb1-9eec-710c4aa64950,8f2a6793-a13c-401d-bd1d-71316dcde52d,3dbefbed-a381-4b28-8ba3-72c280ee184e,5af22c61-5041-4686-bc1a-736186ea6b4e,6ffbe908-e895-4a98-83e2-7401d1b0c35e,4b26cf61-e3ab-4085-a07f-74665281f06b,6391b576-c9fc-443f-a6ba-757b0b3598dc,af15ee25-d14e-49e8-a64b-759b7cb8a32a,7a667385-9ead-4b01-a636-75b443555439,0fcc3f70-164d-4295-9d40-766432d7006a,841c8b59-b7c7-476a-bbe6-76784a8475e6,326cfcc2-a668-4f00-95c5-780cc06275d9,976ca7e0-dca6-4128-9dff-7820574bdd86,c404720c-00a9-4ba9-83b3-78e440bcebcd,c65958e7-5f21-465b-ae15-79ef91500d29,cfb4f378-6010-42b6-9090-7a058e52886d,5f94106a-f267-42d2-a3b5-7a95c9f7e448,df52a40a-225b-4436-94a5-7aa075515c75,7f6f45ac-9999-40f6-ac8b-7c1c7e5e5fc2,c05c2e78-1634-49e0-bf5e-7c4bf3c95c40,3f5ad5a4-cc81-4833-ad38-7c90a8fd2ddf,1d68e29f-3a76-48b0-a732-7d934dea0da8,c88a342e-d4ad-4bec-9b8a-7e42237da8ba,140bf407-9638-4179-aa9e-7e438296aba2,671dedf5-3e47-4e0d-86ba-7e66a3086d31,5150a534-da26-429d-a589-7f5802945943,df009778-a895-4cfe-90b6-7faf874d602f,f43baaee-2a30-4714-891d-7febb056dcf1,b8c8b989-2da9-47b9-9920-805f2e6e56de,3f250603-fd32-4483-a6da-80f02ffccbf4,81b33d7c-c998-4c12-bed3-81ad79fcf821,71b7e071-cb17-4ef6-b2c4-81c1199cf159,f097ccff-22f0-4859-b948-8325681b759e,3092c919-6d6c-45fb-bb15-835876eab3fc,942bdff7-3da4-41d2-a1e1-85a4cf683fc1,1b9dfae2-6086-4881-8716-864c0ad5e50c,7eb2d13f-0783-4300-a3bc-8681269324da,7b7d0592-0d3c-44d0-bf81-86a13bac3d84,6d6f9d31-0035-4f5c-b1ce-884d248c391b,cae5e48a-27e4-4d45-8ba1-893966e2ea96,dbf68af8-f05e-41b5-823d-893a2347f674,c5537789-98bf-45da-bf6b-898a9c23ffa0,8a4d367c-5e99-4279-926d-89a0edd1c7a7,3020d4b6-7a28-4fd2-a37f-89cea7e6625b,5873776f-c327-4056-b433-8a8f7b013083,5906fdf3-ab9f-477a-b68b-8bb4e62a7e7a,8cabcb70-0905-4efc-b7d0-8bd8bb04db52,11e35828-3d6e-492d-85ae-8c338ac98ec5,7afa936c-6044-413e-b5b5-8cb43ec3f0f7,710957c8-c12c-4933-a656-8df62397184e,c9849961-d2ef-46b4-8a7f-8e21455c9f72,139ca57c-58eb-4ce5-be69-8f6f6da2a752,b1a030e1-293b-4472-9e44-8f8036a4847b,2d67246c-ba73-412c-b771-91002c07b350,3c34aa33-17cb-4486-8ed2-916604eedd85,5a953600-e5d8-49c3-b9ca-9180086a695c,8eb40f31-8cb6-44e0-b5ca-91a263b6d392,af520cdf-ffe3-400f-9247-92464ef45332,807dd762-e915-49c1-aeb3-9264ee9cd510,85ab6720-3873-4c89-a374-927d2a5f293a,5dbdf29c-14fe-4c29-aa88-92f68f3c506c,90e34f1c-9c3b-40e7-9dea-93292a7bd5d4,9de76ca6-1a1e-4a62-ba1f-93d76902f136,11a3d36f-1c25-4479-b01c-9453dbf095cb,ddd11f17-03fd-4a86-b7c2-9488578a23c9,6897ce3f-9494-441e-a10e-9515d6b8e592,6996bcc4-b36a-4cc6-8a90-95e3bd3a97d1,e23b6423-4040-45c8-899b-9659fe661d6a,f23633fc-30ae-4bb7-b34c-97a674b89d5b,10db44e0-82d2-4872-abc7-97ba1a32e1e9,cdb78eb5-b933-4d89-9d91-99852165d2c6,ab5f5bd0-00f9-4384-8683-9b684fe93bf0,8d331b84-97bf-4873-91c7-9b691dce63bf,c603473b-b8a8-4227-a03a-9c3481fb95e7,51f36244-a309-4d62-9b86-9c56f82fd981,270ea55d-4e29-4730-a4ad-9c763203f092,dd824112-d2af-4150-b228-9ccf355afdfa,caadfe1a-df8e-407b-a141-9d31e3d0f07f,772976eb-f28f-4e83-91b2-9e0e4fab47fb,3b87fcd2-5577-4082-8964-9e2c0979ef9b,8a4f7e7d-b1bc-4094-8b8b-9e6ebfaf08ce,ad71418f-bd30-4709-bfae-9eb172241e41,ef328093-cfcf-4386-b747-9ee04cabb24e,42554a2d-ccf6-417e-8146-9ee995af3bb8,bf7ab5b8-7d75-47df-965d-9f19affcef65,b9019dbb-a2b1-4fd5-8152-9f3b9df45dc2,73e84e4d-10fc-4a13-abc9-9f984f996487,49db2918-474c-4990-ae32-9fa6e0ee9773,0a01dbe6-d2db-47c9-abb8-a01b1af2e696,a0026f8e-dcc3-4e44-87be-a1170f0694e1,ee19f31b-f7ec-4498-bc0e-a18c10310f10,39fce28e-0aef-4d53-a55e-a1c88a83371b,c9d38f90-699d-4ca9-aae1-a2e73fbb5e1d,6ea995ff-24ff-4e6c-97b8-a4544c84f395,e0c5f98a-26ad-42d8-81ff-a47668fc30c2,620ba946-1665-4ef4-bdc5-a4c82af95bb5,ea141aa7-f663-4184-aab7-a4eb29b91a12,66dcdf68-18a6-448c-8ca8-a506a76270b2,079a3d04-c897-4ed5-9efb-a546fdccc0a3,e161a7a1-62f2-4056-8260-a57e0c62360f,a11e094d-1e23-4e42-bd33-a5bf82489b38,aab16acf-72c5-41c4-9c4e-a5f5dac2943e,336c9a70-ab41-42bd-84d9-a6cbe6d678c8,88c9b1c9-606d-41d9-ab38-a74c846ddaae,4c5d6512-4d71-4812-9f19-a87bf297b56b,722184b9-1db1-48fb-a5a9-a8a212584e28,7df27c37-9f00-4d5b-b5ed-a8a43a150a51,44bcb27a-b8ef-4c80-9a42-a90c0ea1d799,d41e5bbb-c6ab-4bd1-b884-a9e8d6210295,3481221b-1b96-49ea-8264-aa99020407ab,2c4a61cb-75ca-4c3a-a647-aaf824cfb649,7f9535b9-6b3d-4db2-88ad-aafbf2cc2e49,e5861afa-04a3-4403-879e-abe2c7fa099e,c2ce63e2-82ea-4733-b0cc-ac69cab7fe4f,570e00bd-5b49-46d3-b66f-ad02796bcad9,1feb8471-0c04-4c38-8857-ae37523bb07f,8265af4e-c418-4579-933a-af33a5f64d86,b5c06d7a-4598-41cf-9a2e-af899e7aaf32,0a992996-8df9-40ce-bb04-afb7f127f5c1,2a263176-56e5-478b-b211-b00a2ed0c8e2,597a35a0-6ac0-45aa-9e9a-b05dd1217ee9,e2d019cb-ab79-445e-93b5-b0a0550495c0,618781e0-4807-40e7-9750-b16fbc099146,408c5016-2f7c-481f-84e3-b1825b54875e,91e03f7e-7512-45b8-b595-b1b2fea3078b,7791fb08-c41d-4f2d-88a9-b3118a288850,36f06349-fe6c-450d-899c-b3811c526976,0831ed52-4dd5-415e-9a8f-b39406d0bd54,3860943b-7292-4ca2-ab2c-b39ca7def15a,3a0a9e63-8491-4478-b7a3-b3e9824bc293,88ae8f5e-5d2d-48fd-bae6-b499faf948fc,12224329-54d2-402d-b585-b592c3b572b2,e4076347-ce72-4305-a023-b61dffca76a2,0d7e4f56-b3f2-4ee2-9b06-b637c7d1084c,7a83d42c-ded3-48cc-9a18-b654dc3ba1fb,0c91a6c0-5904-4750-8065-b655d9357cb1,0cbc8ad5-7f26-43ec-b88a-b6a500fc3493,9ad35d78-0364-40b6-adb7-b778d505ff6b,ec2e9fdb-642e-4859-9338-b7f5954dedac,f6ee238d-6c9d-4a17-9f40-b92787ec9595,d3bb14ea-c6d8-49f2-b07c-b9719bd0ed28,d3783b35-3449-4e96-9363-b98927b95f41,2d79d1d3-7090-4699-8d20-bbaccf125ce3,cf696133-d152-4aa2-85e0-bbba8c257f17,3a0af86b-7228-41d5-88ce-bbedf6d3ba84,3ed96c37-c1b5-4cce-842b-bbee23550e31,1e1d9735-4986-4cea-b0df-bc572e2986f8,f986bed3-e513-4c1f-9cd9-bce3ead93d8f,f7af9533-5fdc-4410-9e04-be1dd29463f4,9872c5d0-c319-4b26-af91-bf00f3cb910a,1ffc32f9-4283-4458-950e-bf54b0435b2f,5ad6978c-1698-4c99-a20c-bf7760877a5b,ec8bf63c-abea-4dbb-b639-c02a10d737fd,24bfe3ca-beda-4287-ae3a-c1cc828fadf0,b6400957-487b-4a25-93ac-c20869297d70,cbce68b7-4c18-4b33-8d89-c3fa4336105e,77603553-ac3e-4b65-b545-c44d27d98eda,990c198d-88d9-447e-9d05-c4ebb615d7c4,17e2753b-9b6b-40a3-a132-c4f15a18f268,af292428-ca38-41ff-b040-c5788aa4ecf1,3b7f9291-20f8-4b2c-a6a4-c58ff0b20c5b,0b383fcd-b953-4cbc-b568-c5e34e1cfd70,504dfad8-a334-473a-b2b2-c62c3349c3aa,d4aa4602-0a82-4a74-9153-c66d9af3b8cc,7d956802-2529-4f31-9080-c6b451a37de0,7e900f3d-d6d9-416e-9b4d-c6bab0cc18d1,76a658b8-ad68-4ba4-9c72-c6e9e837f5f1,97d76336-49e6-44ea-8214-c762e752d5e9,5bf5d06a-3aa7-4f07-a912-c810b92691a8,054836ee-832a-4d92-9a2c-c89008cc89a5,3f7f2386-bcbd-4599-804d-c91b5eb34c23,61388518-bb12-4a32-9f33-ca06ad398fc1,44b2a939-ed26-42cf-9782-caa623f2282e,7c4482f0-0caa-4796-87ea-cacd1aa7b57b,d9987a0c-abec-43a8-b18d-cb0cf241d3a5,6f4dbe1e-59c0-4169-97bc-cb23d765a1fa,9c5d4b32-9ab0-4ecd-b650-cb564dda6200,7a0297dc-b2f4-4556-9949-cd6b08411f24,26d9e127-5778-4fcd-a0c9-cd857080af9e,4706d3d8-c531-46a3-be8a-ce06324d7f9c,ec6ff90a-7231-4c1c-8a61-ce72605c8436,ee39dcc7-60d1-42d3-9c6a-ceb36acb71a5,2caf9a0a-801a-47c9-b73e-d11116502351,1dc5faa7-a720-47ac-a54a-d1732a5062cc,664a24ea-3dc1-4482-95ef-d177e9741d9b,2fcb2b36-3df3-4694-9768-d1ecbc9b4baf,3868c2a7-344e-45c7-8fcd-d2f973570ca6,2954f5ef-9f6f-423d-bfb5-d3101fea2741,b065f4ff-e738-4216-ad25-d36a0ec6ce32,57bf1d8b-dba9-41d9-a4e8-d36e89f5ad6b,94efd3d8-08d3-47bb-9e1e-d3874bb511c3,6388ef38-69e3-44c2-a3f2-d42f664e47cf,ba385c68-b57b-4647-aaab-d5176b9fe0bc,d4a99e96-4cf7-4992-a27c-d546c9092e8f,28e29a7a-61f1-471b-a395-d576fa1e06a4,c2f3a7e7-fbc0-468d-9eb8-d612029112bf,c68e2480-3e71-4c03-80c5-d6e72e8c8fe9,548ba037-3665-4ea6-9224-d7bfa8e5852c,ca16a985-82ce-4435-a7e6-d7d6cec316f4,8bece6bf-0003-4f19-ba19-d832ec4f0474,1b0997a5-8119-45c3-ab41-d87e9cc042a7,b470494f-98df-4fcb-b3aa-d89c54213764,b8736ef3-4a63-4e34-a0f3-d965db29dd3d,8f9fa620-a408-4d6b-9824-da4aec7eade9,d1b30293-7710-45c0-9a64-dba333797778,51d0aa8b-475d-4f61-a959-dbb1b4caede5,7af88239-63be-414a-a176-dbc21ce72807,bb1fa8e6-d539-4534-87ab-dc400ecf59bc,0e345f51-b096-4d36-af45-dd687f498a9b,72ebdc77-345d-4cd6-832c-de33ecaf0130,84a38d70-9ff0-45a2-9262-debfa51b9409,9c4bac39-7d49-41c1-8881-dec2635d23fd,326cc175-943c-4036-a5a2-def394beedf3,367df4f8-f6b7-49d5-8a3a-df627efa0a8c,e4864ed3-2621-4108-b305-df935477cca5,90864e9d-a50d-4eab-9e32-e0cfa8328f13,1b75e0d8-b7ea-40fc-9acf-e0f2635d573b,07f4191c-7155-4f0d-b85a-e0f425227b27,c1bf2fa6-f550-41bf-b0fe-e10f47a2da30,fac94c29-1770-4339-b19c-e151f974a267,344878f0-02c1-4b2e-93bb-e153bb9315da,60890011-e6c7-4943-9eb0-e32673e4b904,1705b6f9-727e-4419-8011-e455ace6ccc0,e2a0ce9e-7f44-4155-8f75-e4a3a060ee6a,de51c26d-4f7a-4c29-a656-e4b0f295741a,b0ead4c7-fbb3-47e8-bd42-e52e4dc78f03,4fa1b784-1404-440b-8fc2-e5c7dfb91fcc,72272cac-26ba-4d32-99d9-e5f71698c9a5,f96b8319-1c36-4bed-9cdd-e615e6475250,304b0b67-0389-45a0-b85a-e675d013c334,0a589661-8dd6-4902-b857-e6d59564dc43,b8aa228c-0c00-4b89-a466-e7353444ab82,f8a9d84e-8ccc-4a5a-97e0-e75c940e826b,1a3d407e-6aee-4d06-bc58-e77d75240231,e3fdc7fd-9c37-4ad2-b43d-e785a88d0f79,cc8f2c6f-7ac7-453a-b6b1-e919e4d27eb8,48465288-aeb5-484c-a239-e943208ec82b,0c454604-6ed9-4d43-90b3-e94ca077285e,75092b02-596c-4924-afd4-e9f1a7f9ad40,56a96f71-34c1-424a-952e-ea4eeb169a93,5dbf593a-2083-4d8e-bb34-ea5e2c34cf92,93220412-335d-4af9-877b-ea9702f1637d,e7745230-03bb-49c8-b41e-eb49477aead8,f7fb9346-a9d3-4d52-b455-ebd7245bb23f,2d2a501e-e0df-4823-b4b7-ebd7adc510e5,69c11687-430c-4325-a8c8-ecbe7837cb98,1291c0a3-33f3-4da2-8427-ee33655ee38a,279e5c29-1f9c-45ca-bf8f-ee5cd08de67e,21bdc43c-a6cf-4fd2-adac-ef2e65eaf8aa,1ccf6990-1030-4a75-8b0d-f06c92b65557,61de3019-95ae-469e-b4c6-f07735588c9b,e037afc5-8b53-44eb-8f26-f09314345227,97d548a5-b292-4292-89ca-f107fe0f83a3,2225f351-5870-4e3e-8040-f1b5a57a7902,88841b5c-5e2a-4b37-b903-f24227e2f39c,f26c5284-d07f-4152-95ed-f2b637331456,56f98798-c7bd-4ded-be0a-f306158f5254,9e9297af-1397-43c4-bb3a-f320afadd04b,0e25d015-0ea6-4c9e-a093-f3712168228c,e6fa5757-e267-4714-87ef-f60f61b54403,5c334757-9aea-4cc0-8c81-f6feee4a621e,efbbc565-95c7-4f3f-a43f-f7a4c3fb385b,b3884f92-66a9-4642-bfde-f7feb6047d9d,5c878c4a-e41b-4051-8963-f918a5ca1080,3866cde7-4517-4f39-8a7b-f9dc28f23bc5,22305b47-62c5-4d57-b219-fae0f774af9c,954d08c7-8f39-40e6-9893-fb6eda207726,3592da2e-5e6b-43d6-ba2f-fdc1681cbe58,8fc41e83-01cb-4f3a-bc4c-fdd7dfa4962d,312f0cd5-cdec-4a6b-8682-fe764cbb19fe,007cbe67-4637-42cd-8d6f-fea557d7a71a,5632b9ba-d745-41be-b061-ffeb96fee442,f7108256-a583-4e93-b946-4a2637603971,69bcd21e-c94e-4b20-bcc7-a1a13caf7472,6775e577-6f13-4e5c-8923-51c0d22797df,76a5638e-3e19-4315-a69e-f245c0026ca0,b8dea05a-a03a-4210-a467-8aebbff46e9d,61b5ca40-c438-4fc3-b59d-5db59944eb49,54600654-2123-404e-8080-6a0c553d6cdc,8c4088aa-40bc-49a0-88be-71e90a946b67,2a8c1f11-a7f3-4e96-88ba-d2351dd39782,e3ac0d8f-722f-4481-9714-4ae2b73c0022,6c85d19d-ba06-4f3c-9d31-646dbb782145,9ab44587-2f8f-4447-a0e7-ab119fddadac,836dae28-b796-4f90-a37e-11d097228b6a,deb0ff24-8555-4f79-af05-15cbd5ef2c48',
        'FType': 2,
    }
    
    try:
        # Codifica os dados
        encoded_data = urlencode(data).encode('utf-8')
        
        headers = {
            'User-Agent': r'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                         r'Chrome/45.0.2454.85 Safari/537.36 115Browser/6.0.3',
            'Connection': 'keep-alive'
        }
        
        # Faz a requisição
        req = Request(url, headers=headers, data=encoded_data)
        response = urlopen(req)
        page = response.read().decode('utf-8')
        
        # Tenta fazer parse do JSON
        try:
            json_data = json.loads(page)
            # Se foi passado um ID, filtra os resultados
            if search_id and json_data and 'FObject' in json_data and isinstance(json_data['FObject'], list):
                filtered = [item for item in json_data['FObject'] if str(item.get('FAssetID', '') or item.get('FVehicleName', '')) == search_id]
                json_data['FObject'] = filtered
                return JsonResponse(json_data, safe=False)
            # Se não foi passado ID, retorna todos os dados (comportamento original)
            return JsonResponse(json_data, safe=False)
        except json.JSONDecodeError:
            # Se não for JSON válido, retorna como texto
            return JsonResponse({"raw_data": page}, safe=False)
            
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

def mapa_view(request):
    """Renderiza o template do mapa"""
    return render(request, "core/mapa.html")

'''==========alto cafezal ============'''
class AltocafezalCreateView(CreateView):
    model = altocafezalmodel
    form_class = AltocafezalModelForm
    template_name = "core/altocafezal_form.html"
    success_url = reverse_lazy("equipamento_list")

    def form_valid(self, form):
        # Apaga todos os registros existentes antes de salvar o novo
        altocafezalmodel.objects.all().delete()
        return super().form_valid(form)
    
from django.shortcuts import render
from .models import altocafezalmodel  # Modelo dos equipamentos exibidos
from core.models import altocafezalmodel  # Modelo onde os IDs foram cadastrados

import json
from django.shortcuts import render
from core.models import altocafezalmodel



import json
from django.shortcuts import render
from core.models import altocafezalmodel


def equipamento_list_view(request):
    # Obtém os valores do campo 'id_equipamento'
    allowed_unitnumbers_qs = list(altocafezalmodel.objects.values_list('id_equipamento', flat=True))
    
    if allowed_unitnumbers_qs:
        # Se houver dados, divide a string em uma lista (caso esteja armazenado como uma única string com quebras de linha)
        allowed_unitnumbers = allowed_unitnumbers_qs[0].splitlines()
    else:
        allowed_unitnumbers = []
    
    allowed_unitnumbers_json = json.dumps(allowed_unitnumbers)
    print("allowed_unitnumbers_json:", allowed_unitnumbers_json)  # Debug na view
    
    context = {
        'allowed_unitnumbers_json': allowed_unitnumbers_json,
    }
    return render(request, 'core/altocafezal_mapa.html', context)


'''=======alto cafezal ======='''



'''=======================burbomcofe====================='''
from .models import burbomcofelmodel
from .forms import burbomcofeModelForm
class burbomcofeCreateView(CreateView):
    model = burbomcofelmodel
    form_class = burbomcofeModelForm
    template_name = "core/burbomcofe_form.html"
    success_url = reverse_lazy("equipamento_list")

    
    def form_valid(self, form):
        # Apaga todos os registros existentes do modelo burbomcofelmodel antes de salvar o novo
        burbomcofelmodel.objects.all().delete()
        return super().form_valid(form)
    

def equipamento_listburbom_view(request):
    # Obtém os valores do campo 'id_equipamento'
    allowed_unitnumbers_qs = list(burbomcofelmodel.objects.values_list('id_equipamento', flat=True))
    
    if allowed_unitnumbers_qs:
        # Se houver dados, divide a string em uma lista (caso esteja armazenado como uma única string com quebras de linha)
        allowed_unitnumbers = allowed_unitnumbers_qs[0].splitlines()
    else:
        allowed_unitnumbers = []
    
    allowed_unitnumbers_json = json.dumps(allowed_unitnumbers)
    print("allowed_unitnumbers_json:", allowed_unitnumbers_json)  # Debug na view
    
    context = {
        'allowed_unitnumbers_json': allowed_unitnumbers_json,
    }
    return render(request, 'core/burbomcofe_mapa.html', context)




'''=======================carmocofe====================='''

from .models import carmocofelmodel
from .forms import carmocofeModelForm
class carmocofeCreateView(CreateView):
    model = carmocofelmodel
    form_class = carmocofeModelForm
    template_name = "core/carmocofe_form.html"
    success_url = reverse_lazy("equipamento_list")

    
    def form_valid(self, form):
        # Apaga todos os registros existentes do modelo burbomcofelmodel antes de salvar o novo
        carmocofelmodel.objects.all().delete()
        return super().form_valid(form)
    

def equipamento_listcarmo_view(request):
    # Obtém os valores do campo 'id_equipamento'
    allowed_unitnumbers_qs = list(carmocofelmodel.objects.values_list('id_equipamento', flat=True))
    
    if allowed_unitnumbers_qs:
        # Se houver dados, divide a string em uma lista (caso esteja armazenado como uma única string com quebras de linha)
        allowed_unitnumbers = allowed_unitnumbers_qs[0].splitlines()
    else:
        allowed_unitnumbers = []
    
    allowed_unitnumbers_json = json.dumps(allowed_unitnumbers)
    print("allowed_unitnumbers_json:", allowed_unitnumbers_json)  # Debug na view
    
    context = {
        'allowed_unitnumbers_json': allowed_unitnumbers_json,
    }
    return render(request, 'core/carmocofe_mapa.html', context)


'''=======================carmocofe====================='''


'''=======================cexpocacer====================='''

from .models import expocacermodel
from .forms import expocacerModelForm

class expocacerCreateView(CreateView):
    model = expocacermodel
    form_class = expocacerModelForm
    template_name = "core/expocacer_form.html"
    success_url = reverse_lazy("equipamento_list")

    
    def form_valid(self, form):
        # Apaga todos os registros existentes do modelo burbomcofelmodel antes de salvar o novo
        expocacermodel.objects.all().delete()
        return super().form_valid(form)
    
    
def equipamento_listtexpo_view(request):
    # Obtém os valores do campo 'id_equipamento'
    allowed_unitnumbers_qs = list(expocacermodel.objects.values_list('id_equipamento', flat=True))
    
    if allowed_unitnumbers_qs:
        # Se houver dados, divide a string em uma lista (caso esteja armazenado como uma única string com quebras de linha)
        allowed_unitnumbers = allowed_unitnumbers_qs[0].splitlines()
    else:
        allowed_unitnumbers = []
    
    allowed_unitnumbers_json = json.dumps(allowed_unitnumbers)
    print("allowed_unitnumbers_json:", allowed_unitnumbers_json)  # Debug na view
    
    context = {
        'allowed_unitnumbers_json': allowed_unitnumbers_json,
    }
    return render(request, 'core/expocacer_mapa.html', context)

'''=======================cexpocacer====================='''

'''=======================coxupe====================='''
from .models import coxupemodel
from .forms import coxupeModelForm

class coxupeCreateView(CreateView):
    model = coxupemodel
    form_class = coxupeModelForm
    template_name = "core/coxupe_form.html"
    success_url = reverse_lazy("equipamento_list")

    
    def form_valid(self, form):
        # Apaga todos os registros existentes do modelo burbomcofelmodel antes de salvar o novo
        coxupemodel.objects.all().delete()
        return super().form_valid(form)
    
    
def equipamento_listcoxupe_view(request):
    # Obtém os valores do campo 'id_equipamento'
    allowed_unitnumbers_qs = list(coxupemodel.objects.values_list('id_equipamento', flat=True))
    
    if allowed_unitnumbers_qs:
        # Se houver dados, divide a string em uma lista (caso esteja armazenado como uma única string com quebras de linha)
        allowed_unitnumbers = allowed_unitnumbers_qs[0].splitlines()
    else:
        allowed_unitnumbers = []
    
    allowed_unitnumbers_json = json.dumps(allowed_unitnumbers)
    print("allowed_unitnumbers_json:", allowed_unitnumbers_json)  # Debug na view
    
    context = {
        'allowed_unitnumbers_json': allowed_unitnumbers_json,
    }
    return render(request, 'core/coxupe_mapa.html', context)
'''=======================coxupe====================='''

'''=======================nkg====================='''

from .models import nkgmodel
from .forms import nkgModelForm

class nkgCreateView(CreateView):
    model = nkgmodel
    form_class = nkgModelForm
    template_name = "core/nkg_form.html"
    success_url = reverse_lazy("equipamento_list")

    
    def form_valid(self, form):
        # Apaga todos os registros existentes do modelo burbomcofelmodel antes de salvar o novo
        nkgmodel.objects.all().delete()
        return super().form_valid(form)
    
    
def equipamento_listnkg_view(request):
    # Obtém os valores do campo 'id_equipamento'
    allowed_unitnumbers_qs = list(nkgmodel.objects.values_list('id_equipamento', flat=True))
    
    if allowed_unitnumbers_qs:
        # Se houver dados, divide a string em uma lista (caso esteja armazenado como uma única string com quebras de linha)
        allowed_unitnumbers = allowed_unitnumbers_qs[0].splitlines()
    else:
        allowed_unitnumbers = []
    
    allowed_unitnumbers_json = json.dumps(allowed_unitnumbers)
    print("allowed_unitnumbers_json:", allowed_unitnumbers_json)  # Debug na view
    
    context = {
        'allowed_unitnumbers_json': allowed_unitnumbers_json,
    }
    return render(request, 'core/nkg_mapa.html', context)

'''=======================nkg====================='''

'''=======================velosocoffe====================='''

from .models import velosocofemodel
from .forms import velosocofeModelForm

class velosocCreateView(CreateView):
    model = velosocofemodel
    form_class = velosocofeModelForm
    template_name = "core/velosoc_form.html"
    success_url = reverse_lazy("equipamento_list")

    
    def form_valid(self, form):
        # Apaga todos os registros existentes do modelo burbomcofelmodel antes de salvar o novo
        velosocofemodel.objects.all().delete()
        return super().form_valid(form)
    
    
def equipamento_listvelosocofe_view(request):
    # Obtém os valores do campo 'id_equipamento'
    allowed_unitnumbers_qs = list(velosocofemodel.objects.values_list('id_equipamento', flat=True))
    
    if allowed_unitnumbers_qs:
        # Se houver dados, divide a string em uma lista (caso esteja armazenado como uma única string com quebras de linha)
        allowed_unitnumbers = allowed_unitnumbers_qs[0].splitlines()
    else:
        allowed_unitnumbers = []
    
    allowed_unitnumbers_json = json.dumps(allowed_unitnumbers)
    print("allowed_unitnumbers_json:", allowed_unitnumbers_json)  # Debug na view
    
    context = {
        'allowed_unitnumbers_json': allowed_unitnumbers_json,
    }
    return render(request, 'core/velosoc_mapa.html', context)

'''=======================velosogreen====================='''


'''=======================velosogreen====================='''


from .models import velosogreenmodel
from .forms import velosogreenfeModelForm

class velosogreenCreateView(CreateView):
    model = velosogreenmodel
    form_class = velosogreenfeModelForm
    template_name = "core/velosogreen_form.html"
    success_url = reverse_lazy("equipamento_list")

    
    def form_valid(self, form):
        # Apaga todos os registros existentes do modelo burbomcofelmodel antes de salvar o novo
        velosogreenmodel.objects.all().delete()
        return super().form_valid(form)
    
    
def equipamento_listvelosogreen_view(request):
    # Obtém os valores do campo 'id_equipamento'
    allowed_unitnumbers_qs = list(velosogreenmodel.objects.values_list('id_equipamento', flat=True))
    
    if allowed_unitnumbers_qs:
        # Se houver dados, divide a string em uma lista (caso esteja armazenado como uma única string com quebras de linha)
        allowed_unitnumbers = allowed_unitnumbers_qs[0].splitlines()
    else:
        allowed_unitnumbers = []
    
    allowed_unitnumbers_json = json.dumps(allowed_unitnumbers)
    print("allowed_unitnumbers_json:", allowed_unitnumbers_json)  # Debug na view
    
    context = {
        'allowed_unitnumbers_json': allowed_unitnumbers_json,
    }
    return render(request, 'core/velosogreen_mapa.html', context)
'''=======================velosogreen====================='''


'''=======================volcafee====================='''

from .models import volcafemodel
from .forms import volcafeModelForm

class volcafeCreateView(CreateView):
    model = volcafemodel
    form_class = volcafeModelForm
    template_name = "core/volcafe_form.html"
    success_url = reverse_lazy("equipamento_list")

    
    def form_valid(self, form):
        # Apaga todos os registros existentes do modelo burbomcofelmodel antes de salvar o novo
        volcafemodel.objects.all().delete()
        return super().form_valid(form)
    
    
def equipamento_listvolcafe_view(request):
    # Obtém os valores do campo 'id_equipamento'
    allowed_unitnumbers_qs = list(volcafemodel.objects.values_list('id_equipamento', flat=True))
    
    if allowed_unitnumbers_qs:
        # Se houver dados, divide a string em uma lista (caso esteja armazenado como uma única string com quebras de linha)
        allowed_unitnumbers = allowed_unitnumbers_qs[0].splitlines()
    else:
        allowed_unitnumbers = []
    
    allowed_unitnumbers_json = json.dumps(allowed_unitnumbers)
    print("allowed_unitnumbers_json:", allowed_unitnumbers_json)  # Debug na view
    
    context = {
        'allowed_unitnumbers_json': allowed_unitnumbers_json,
    }
    return render(request, 'core/volcafe_mapa.html', context)

from django.views.generic import TemplateView

from django.shortcuts import render

def resumoView(request):
    return render(request, "resumo.html")

def update_assetscontrols_data(request, asset_id):
    """Atualiza dados de um equipamento AssetsControls na plataforma Golden (T42)"""
    if request.method == 'PUT':
        try:
            import json
            data = json.loads(request.body)
            
            # Pega apenas os últimos 6 dígitos do ID
            golden_id = asset_id[-6:]  # Sempre pega os últimos 6 dígitos
            
            print(f"🔧 ID original: {asset_id}")
            print(f"🔧 ID para Golden: {golden_id}")
            
            # URL da API Golden (T42)
            url = f'https://intgoldensat.com.br/nestle/api/grid/{golden_id}/'
            
            # Payload para Golden (T42)
            payload = {
                'bl': data.get('bl', ''),
                'container': data.get('container', ''),
                'destino': data.get('destino', '')
            }
            
            # Headers
            headers = {
                'Content-Type': 'application/json',
                'Authorization': 'Token 236eeb21bd3b0c084eb82271412bf505c758837b'
            }
            
            print(f"🔄 Fazendo PUT para Golden: {url}")
            print(f"📦 Payload: {payload}")
            
            # Faz a requisição PUT para a API Golden
            response = requests.put(url, json=payload, headers=headers)
            
            print(f"📡 Resposta Golden: {response.status_code}")
            
            if response.ok:
                response_data = response.json()
                print(f"✅ Golden atualizado com sucesso: {response_data}")
                
                # Também salva no banco local para backup
                from equipamentos.models import Equipamento
                equipamento, created = Equipamento.objects.get_or_create(
                    identificador=asset_id,
                    defaults={
                        'BL': data.get('bl', ''),
                        'container': data.get('container', ''),
                        'destino': data.get('destino', '')
                    }
                )
                
                if not created:
                    equipamento.BL = data.get('bl', '')
                    equipamento.container = data.get('container', '')
                    equipamento.destino = data.get('destino', '')
                    equipamento.save()
                
                return JsonResponse({
                    "success": True,
                    "message": "Dados atualizados com sucesso na plataforma Golden",
                    "data": {
                        "identificador": asset_id,
                        "golden_id": golden_id,
                        "bl": data.get('bl', ''),
                        "container": data.get('container', ''),
                        "destino": data.get('destino', '')
                    }
                })
            else:
                print(f"❌ Erro Golden: {response.status_code} - {response.text}")
                return JsonResponse({
                    "success": False,
                    "error": f"Erro na API Golden: {response.status_code} - {response.text}"
                }, status=response.status_code)
                
        except Exception as e:
            print(f"💥 Erro na função update_assetscontrols_data: {str(e)}")
            return JsonResponse({
                "success": False,
                "error": f"Erro interno: {str(e)}"
            }, status=500)
    
    return JsonResponse({
        "success": False,
        "error": "Method not allowed"
    }, status=405)




from django.http import JsonResponse
import requests
import json

# Dicionário de controle (para simulação de memória temporária)
from django.core.cache import cache
from .equipament_cnfig import EQUIPMENT_GUIDS

def verificar_fdoor(request):
    """
    Verifica status de porta e luminosidade em lote para todos os equipamentos
    """
    url = 'http://cloud.assetscontrols.com:8092/OpenApi/LBS'
    
    # Usa todos os GUIDs disponíveis
    guids_string = ','.join(EQUIPMENT_GUIDS)
    
    payload = {
        'FAction': 'QueryLBSMonitorListByFGUIDs',
        'FTokenID': '7e88e035-285a-4f7d-8e63-8b403d04dcfa',
        'FGUIDs': guids_string,
        'FDateType': 2
    }

    # Sistema de retry para tornar mais robusto
    max_retries = 3
    retry_count = 0
    
    while retry_count < max_retries:
        try:
            print(f"🔍 Consultando todos os equipamentos (tentativa {retry_count + 1}/{max_retries})")
            print(f"📊 Total de equipamentos: {len(EQUIPMENT_GUIDS)}")
            
            # Timeout aumentado para lidar com muitos equipamentos
            response = requests.post(url, json=payload, timeout=30)
            data = response.json()

            eventos_detectados = []
            
            if data['Result'] == 200 and data['FObject']:
                for equipamento in data['FObject']:
                    status = int(equipamento.get('FDoor', -1))
                    nome = equipamento.get('FVehicleName', 'Equipamento desconhecido')
                    guid = equipamento.get('FAssetID')
                    fdesc_raw = equipamento.get("FExpandProto", {}).get("FDesc", "")
                    fdesc = json.loads(fdesc_raw) if fdesc_raw else {}
                    flx = float(fdesc.get("fLx", -1))

                    # Verifica estado anterior da porta
                    ultimo_status = cache.get(f'ultimo_status_{guid}')
                    cache.set(f'ultimo_status_{guid}', status, timeout=1800)  # 30 minutos

                    # Debug: Log dos status (apenas se houver mudança)
                    if ultimo_status != status:
                        print(f"🔍 {nome} (GUID: {guid}): Status atual: {status}, Status anterior: {ultimo_status}")

                    # Verifica mudança de status da porta
                    if status == 1 and ultimo_status != 1:
                        print(f"🚨 PORTA ABERTA detectada: {nome}")
                        eventos_detectados.append({
                            'evento': 'aberta',
                            'equipamento': nome,
                            'guid': guid
                        })
                    elif status == 0 and ultimo_status == 1:
                        print(f"✅ PORTA FECHADA detectada: {nome}")
                        eventos_detectados.append({
                            'evento': 'fechada',
                            'equipamento': nome,
                            'guid': guid
                        })
                    # Adiciona verificação para porta fechada na primeira vez (quando ultimo_status é None)
                    elif status == 0 and ultimo_status is None:
                        print(f"✅ PORTA FECHADA detectada (primeira vez): {nome}")
                        eventos_detectados.append({
                            'evento': 'fechada',
                            'equipamento': nome,
                            'guid': guid
                        })

                    # Verifica luminosidade (timeout reduzido para 5 minutos)
                    if flx > 15 and not cache.get(f'alerta_luz_{guid}'):
                        cache.set(f'alerta_luz_{guid}', True, timeout=300)  # 5 minutos
                        eventos_detectados.append({
                            'evento': 'luz',
                            'equipamento': nome,
                            'guid': guid,
                            'valor': flx
                        })

            # Retorna todos os eventos detectados
            if eventos_detectados:
                return JsonResponse({
                    'eventos': eventos_detectados,
                    'total_eventos': len(eventos_detectados),
                    'total_equipamentos': len(EQUIPMENT_GUIDS)
                })
            else:
                return JsonResponse({
                    'eventos': [],
                    'total_eventos': 0,
                    'total_equipamentos': len(EQUIPMENT_GUIDS),
                    'mensagem': 'Nenhum evento detectado'
                })

        except Exception as e:
            retry_count += 1
            print(f"❌ Erro ao consultar a API (tentativa {retry_count}/{max_retries}): {e}")
            
            if retry_count >= max_retries:
                return JsonResponse({
                    'error': f'Erro ao consultar a API após {max_retries} tentativas: {str(e)}'
                }, status=500)
            
            # Aguarda antes de tentar novamente
            import time
            time.sleep(2)

def update_t42_data(request, unit_id):
    """Atualiza dados de um equipamento T42 na API Golden via proxy (evita CORS)"""
    if request.method == 'PUT':
        try:
            import json
            data = json.loads(request.body)
            
            # URL da API Golden (T42)
            url = f'https://intgoldensat.com.br/nestle/api/grid/{unit_id}/'
            
            # Payload para Golden (T42)
            payload = {
                'bl': data.get('bl', ''),
                'container': data.get('container', ''),
                'destino': data.get('destino', '')
            }
            
            # Headers
            headers = {
                'Content-Type': 'application/json',
                'Authorization': 'Token 236eeb21bd3b0c084eb82271412bf505c758837b'
            }
            
            print(f"🔄 Fazendo PUT para Golden via proxy: {url}")
            print(f"📦 Payload: {payload}")
            
            # Faz a requisição PUT para a API Golden através do backend
            response = requests.put(url, json=payload, headers=headers)
            
            print(f"📡 Resposta Golden: {response.status_code}")
            
            if response.ok:
                response_data = response.json()
                print(f"✅ Golden atualizado com sucesso: {response_data}")
                
                return JsonResponse({
                    "success": True,
                    "message": "Dados atualizados com sucesso na plataforma Golden",
                    "data": response_data
                })
            else:
                print(f"❌ Erro Golden: {response.status_code} - {response.text}")
                return JsonResponse({
                    "success": False,
                    "error": f"Erro na API Golden: {response.status_code} - {response.text}"
                }, status=response.status_code)
                
        except Exception as e:
            print(f"💥 Erro na função update_t42_data: {str(e)}")
            return JsonResponse({
                "success": False,
                "error": f"Erro interno: {str(e)}"
            }, status=500)
    
    return JsonResponse({
        "success": False,
        "error": "Method not allowed"
    }, status=405)
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.cache import cache

@csrf_exempt
def eventos_recentes(request):
    eventos = cache.get("eventos_recentes", [])
    return JsonResponse({"eventos": eventos, "total": len(eventos)})






from django.http import JsonResponse
from django.views.decorators.http import require_GET
from django.utils.timezone import now, timedelta

from core.models import EventoTratado
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from django.db.models import Max
from core.models import EventoTratado

@require_GET
def alertas_api(request):
    """
    Retorna somente os eventos MAIS RECENTES do banco.
    O front envia ?last_id=X   → devolvemos só id>X
    """
    try:
        last_id = int(request.GET.get("last_id", 0))
    except ValueError:
        last_id = 0

    qs = (
        EventoTratado.objects
        .filter(id__gt=last_id)
        .order_by("id")[:200]           # no máximo 200 por chamada
    )

    eventos = [
        {
            "id"          : ev.id,
            "guid"        : ev.guid,
            "tipo_evento" : ev.tipo_evento,          # "door" | "light"
            "valor"       : ev.valor,                # 0/1 ou lux
            "data"        : ev.criado_em.isoformat()
        }
        for ev in qs
    ]

    return JsonResponse({
        "ultimo_id" : eventos[-1]["id"] if eventos else last_id,
        "eventos"   : eventos,
    })


from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
import json

def eventos_list_view(request):
    """
    View para listar todos os eventos com paginação e filtros
    """
    # Parâmetros de filtro
    status_filter = request.GET.get('status', '')
    tipo_filter = request.GET.get('tipo', '')
    guid_filter = request.GET.get('guid', '')
    acao_filter = request.GET.get('acao', '')
    
    # Query base
    eventos = EventoTratado.objects.all()
    
    # Aplicar filtros
    if status_filter:
        if status_filter == 'pendente':
            eventos = eventos.filter(alerta_disparado=False)
        elif status_filter == 'tratado':
            eventos = eventos.filter(alerta_disparado=True)
    
    if tipo_filter:
        eventos = eventos.filter(tipo_evento__icontains=tipo_filter)
    
    if guid_filter:
        eventos = eventos.filter(guid__icontains=guid_filter)
    
    if acao_filter:
        eventos = eventos.filter(acao_tomada=acao_filter)
    
    # Ordenar por data de criação (mais recentes primeiro)
    eventos = eventos.order_by('-criado_em')
    
    # Paginação
    paginator = Paginator(eventos, 10)  # 20 eventos por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Estatísticas
    total_eventos = eventos.count()
    pendentes = eventos.filter(alerta_disparado=False).count()
    tratados = eventos.filter(alerta_disparado=True).count()
    
    # Adiciona informações de tratamento aos eventos
    for evento in page_obj:
        if evento.alerta_disparado and evento.tratado_em:
            evento.tempo_tratamento = evento.tratado_em - evento.criado_em
    
    context = {
        'eventos': page_obj,
        'total_eventos': total_eventos,
        'pendentes': pendentes,
        'tratados': tratados,
        'status_filter': status_filter,
        'tipo_filter': tipo_filter,
        'guid_filter': guid_filter,
        'acao_filter': acao_filter,
    }
    
    return render(request, 'core/eventos.html', context)


@login_required
@require_http_methods(["POST"])
@csrf_exempt
def tratar_evento(request, evento_id):
    """
    Marca um evento como tratado
    """
    try:
        evento = EventoTratado.objects.get(id=evento_id)
        
        # Se já foi tratado, retorna erro
        if evento.alerta_disparado:
            return JsonResponse({
                'success': False,
                'error': 'Evento já foi tratado'
            })
        
        # Pega os dados do request
        data = json.loads(request.body)
        observacoes = data.get('observacoes', '')
        acao_tomada = data.get('acao_tomada', 'verificado')
        
        # Marca como tratado
        evento.marcar_como_tratado(
            tratado_por=request.user.username,
            observacoes=observacoes,
            acao_tomada=acao_tomada
        )
        
        return JsonResponse({
            'success': True,
            'message': 'Evento marcado como tratado com sucesso',
            'evento': {
                'id': evento.id,
                'tratado_em': evento.tratado_em.isoformat() if evento.tratado_em else None,
                'tratado_por': evento.tratado_por,
                'acao_tomada': evento.acao_tomada
            }
        })
        
    except EventoTratado.DoesNotExist:
        return JsonResponse({
            'success': False,
            'error': 'Evento não encontrado'
        }, status=404)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': f'Erro ao tratar evento: {str(e)}'
        }, status=500)


@login_required
@require_http_methods(["DELETE"])
@csrf_exempt
def excluir_evento(request, evento_id):
    """
    Exclui um evento
    """
    try:
        evento = EventoTratado.objects.get(id=evento_id)
        evento.delete()
        
        return JsonResponse({
            'success': True,
            'message': 'Evento excluído com sucesso'
        })
        
    except EventoTratado.DoesNotExist:
        return JsonResponse({
            'success': False,
            'error': 'Evento não encontrado'
        }, status=404)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': f'Erro ao excluir evento: {str(e)}'
        }, status=500)


@login_required
def detalhes_evento(request, evento_id):
    """
    Retorna detalhes de um evento específico
    """
    try:
        evento = EventoTratado.objects.get(id=evento_id)
        
        return JsonResponse({
            'success': True,
            'evento': {
                'id': evento.id,
                'guid': evento.guid,
                'tipo_evento': evento.tipo_evento,
                'valor': evento.valor,
                'criado_em': evento.criado_em.isoformat(),
                'alerta_disparado': evento.alerta_disparado,
                'tratado_em': evento.tratado_em.isoformat() if evento.tratado_em else None,
                'tratado_por': evento.tratado_por,
                'observacoes': evento.observacoes,
                'acao_tomada': evento.acao_tomada
            }
        })
        
    except EventoTratado.DoesNotExist:
        return JsonResponse({
            'success': False,
            'error': 'Evento não encontrado'
        }, status=404)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': f'Erro ao buscar detalhes: {str(e)}'
        }, status=500)


@login_required
def exportar_eventos(request):
    """
    Exporta eventos filtrados para CSV
    """
    import csv
    from django.http import HttpResponse
    
    # Aplica os mesmos filtros da view de listagem
    status_filter = request.GET.get('status', '')
    tipo_filter = request.GET.get('tipo', '')
    guid_filter = request.GET.get('guid', '')
    
    eventos = EventoTratado.objects.all()
    
    if status_filter:
        if status_filter == 'pendente':
            eventos = eventos.filter(alerta_disparado=False)
        elif status_filter == 'tratado':
            eventos = eventos.filter(alerta_disparado=True)
    
    if tipo_filter:
        eventos = eventos.filter(tipo_evento__icontains=tipo_filter)
    
    if guid_filter:
        eventos = eventos.filter(guid__icontains=guid_filter)
    
    eventos = eventos.order_by('-criado_em')
    
    # Cria a resposta HTTP com CSV
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="eventos_{now().strftime("%Y%m%d_%H%M%S")}.csv"'
    
    writer = csv.writer(response)
    writer.writerow([
        'ID', 'GUID', 'Tipo Evento', 'Valor', 'Criado em', 
        'Status', 'Tratado em', 'Tratado por', 'Ação tomada', 'Observações'
    ])
    
    for evento in eventos:
        writer.writerow([
            evento.id,
            evento.guid,
            evento.tipo_evento,
            evento.valor,
            evento.criado_em.strftime('%d/%m/%Y %H:%M:%S'),
            'Tratado' if evento.alerta_disparado else 'Pendente',
            evento.tratado_em.strftime('%d/%m/%Y %H:%M:%S') if evento.tratado_em else '',
            evento.tratado_por or '',
            evento.acao_tomada or '',
            evento.observacoes or ''
        ])
    
    return response