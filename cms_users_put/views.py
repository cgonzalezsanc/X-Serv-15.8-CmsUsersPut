from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound
from models import Pages
from django.views.decorators.csrf import csrf_exempt


# Create your views here.

@csrf_exempt
def handler(request, recurso):
    estado = "<br>\n<br>\n"
    if request.user.is_authenticated():
        estado += "Eres " + request.user.username + "."
        estado += "<a href='/admin/logout/'>Logout</a>"
    else:
        estado += "No has hecho login. " + "<a href='/admin/'>Login</a>"
    fila = Pages.objects.filter(name=recurso)
    if request.method == "GET":
        if not fila:
            return HttpResponseNotFound("Pagina no encontrada" + estado)
        else:
            return HttpResponse(fila[0].page + estado)
    elif request.method == "PUT":
        if request.user.is_authenticated():
            if not fila:
                if recurso == "":
                    fila = Pages(name=recurso, page="Pagina principal")
                else:
                    fila = Pages(name=recurso, page="Pagina de " + recurso)
                fila.save()
                return HttpResponse(fila.page + estado)
            else:
                return HttpResponse("Esta pagina ya esta almacenada" + estado)
        else:
            return HttpResponse("Solo usuarios registrados pueden " +
                                 "cambiar contenido" + estado)
    else:
        return HttpResponseNotFound("Metodo erroneo" + estado)
