from import_export import resources
from .models import Reclamo

class ReclamoResource(resources.ModelResource):
    class Meta:
        model = Reclamo
        import_id_fields = ('numero_documento',)
        fields = ('id', 'nombre', 'apellidos', 'tipo_documento', 'numero_documento', 'correo_electronico', 'telefono', 'direccion', 'distrito', 'provincia', 'fecha', 'hora', 'sede', 'descripcion', 'archivo', 'consentimiento', 'estado', 'oficina')
