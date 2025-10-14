# Tipos de geofences
TIPO_FAZENDA = "fazenda"
TIPO_PORTO = "porto"
TIPO_DEPOSITO = "deposito"

GEOFENCES = [
    {
        "nome": "Grupo Golden Sat",
        "tipo": TIPO_DEPOSITO,
        "endereco": "Rua Haiti, 129 - Parque das Nações, Santo André - SP, 09280-390",
        "lat": -23.667449,
        "lng": -46.527946,
        "raio_m": 5000
    },
    {
        "nome": "Alto Cafezal",
        "tipo": TIPO_FAZENDA,
        "endereco": "Rua Coronel João Cândico de Aguiar, 2101, Andar 1 - Industrial - Patrocínio/MG",
        "lat": -18.956857,
        "lng": -46.991943,
        "raio_m": 5000
    },
    {
        "nome": "Bourbon Specialty Coffees",
        "tipo": TIPO_FAZENDA,
        "endereco": "Rua Piauí, 129 - Centro, Poços de Caldas, MG",
        "lat": -21.785378,
        "lng": -46.564398,
        "raio_m": 5000
    },
    {
        "nome": "Carmo Coffee",
        "tipo": TIPO_FAZENDA,
        "endereco": "Rod. Fernão Dias, S/N - KM 748 - Distrito Industrial, Três Corações - MG",
        "lat": -21.692265,
        "lng": -45.255634,
        "raio_m": 5000
    },
    {
        "nome": "Cooxupé",
        "tipo": TIPO_FAZENDA,
        "endereco": "Rua Manoel Gonçalves Ferraz, 356 – Bela Vista, Guaxupé – MG",
        "lat": -21.303116,
        "lng": -46.708397,
        "raio_m": 5000
    },
    {
        "nome": "Expocaccer",
        "tipo": TIPO_FAZENDA,
        "endereco": "Avenida Faria Pereira, 3945 – Distrito Industrial – Patrocínio - MG",
        "lat": -18.940388,
        "lng": -46.987964,
        "raio_m": 5000
    },
    {
        "nome": "NKG",
        "tipo": TIPO_FAZENDA,
        "endereco": "Av. José Ribeiro Tristão, 105 - Aeroporto, Varginha - MG",
        "lat": -21.589355,
        "lng": -45.430307,
        "raio_m": 5000
    },
    {
        "nome": "Veloso Coffee",
        "tipo": TIPO_FAZENDA,
        "endereco": "Avenida Bela Vista, nº 81, Bairro Bela Vista - Carmo do Paranaíba - MG",
        "lat": -18.995857,
        "lng": -46.114857,
        "raio_m": 5000
    },
    {
        "nome": "Veloso Green Coffee",
        "tipo": TIPO_FAZENDA,
        "endereco": "AVENIDA JOAO BATISTA DA SILVA, 801, AMAZONAS, CARMO DO PARANAÍBA/MG",
        "lat": -18.995000,
        "lng": -46.112000,
        "raio_m": 5000
    },
    {
        "nome": "Volcafé",
        "tipo": TIPO_FAZENDA,
        "endereco": "Rua Maria Nazareth Prado, 225 - Industrial Reinaldo Foresti, Varginha - MG",
        "lat": -21.567800,
        "lng": -45.430900,
        "raio_m": 5000
    },
    # Portos
    {
        "nome": "Porto de Santos",
        "tipo": TIPO_PORTO,
        "endereco": "Av. Cândido Gaffrée, s/n - Paquetá, Santos - SP",
        "lat": -23.937229,
        "lng": -46.307820,
        "raio_m": 8000  # Porto é maior, raio de 8km
    }
] 