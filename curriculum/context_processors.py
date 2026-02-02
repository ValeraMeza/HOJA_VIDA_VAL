from .models import ConfiguracionPagina
def visibilidad_context(request): 
    return {'config': ConfiguracionPagina.objects.first()}