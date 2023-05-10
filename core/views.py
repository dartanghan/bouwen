from django.shortcuts import render
from rest_framework import viewsets, permissions
from .serializer import UsuarioSerializer,EmpresaSerializer,CreditoSerializer, WorkboxSerializer
from .models import usuario,empresa, credito,credito_usado,workbox
# Create your views here.


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = usuario.objects.all()
    serializer_class = UsuarioSerializer
    permission_classes = [permissions.IsAuthenticated]

class EmpresaViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = empresa.objects.all()
    serializer_class = EmpresaSerializer
    permission_classes = [permissions.IsAuthenticated]

class CreditoViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = credito.objects.all()
    serializer_class = CreditoSerializer
    permission_classes = [permissions.IsAuthenticated]

class WorkboxViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = workbox.objects.all()
    serializer_class = WorkboxSerializer
    permission_classes = [permissions.IsAuthenticated]

