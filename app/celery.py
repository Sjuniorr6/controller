# app/celery.py
from __future__ import absolute_import, unicode_literals
import os
from datetime import timedelta

from celery import Celery
from django.conf import settings

# ---------------------------------------------------------------------
# 1) Aponta o Django settings
# ---------------------------------------------------------------------
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app.settings")

# ---------------------------------------------------------------------
# 2) Cria a instância do Celery
# ---------------------------------------------------------------------
app = Celery("app")

# ---------------------------------------------------------------------
# 3) Carrega todas as chaves que começam com CELERY_ no settings.py
# ---------------------------------------------------------------------
app.config_from_object("django.conf:settings", namespace="CELERY")

# ---------------------------------------------------------------------
# 4) Ajustes extras (importantes para Windows)
# ---------------------------------------------------------------------
app.conf.update(
    worker_pool="solo",                       # evita erros de prefork
    broker_connection_retry_on_startup=True,  # some o PendingDeprecation
    timezone="America/Sao_Paulo",
    enable_utc=False,
)

# ---------------------------------------------------------------------
# 5) Agenda do beat (TUDO em 5 s)  ← só a task que realmente existe!
# ---------------------------------------------------------------------
app.conf.beat_schedule = {
    "verifica_assetcontrol_a_cada_5s": {
        "task": "core.tasks.verificar_alertas_equipamentos",
        "schedule": timedelta(seconds=10),
    },
}

# ---------------------------------------------------------------------
# 6) Autodescobre as tasks em todos os apps instalados
# ---------------------------------------------------------------------
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

# ---------------------------------------------------------------------
# 7) Task de debug opcional
# ---------------------------------------------------------------------
@app.task(bind=True)
def debug_task(self):
    print(f"⚙️  Debug task executada → {self.request!r}")
