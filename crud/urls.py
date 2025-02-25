from django.urls import path
from .views import CepCreateView, CepListView, CepUpdateView, CepDeleteView

urlpatterns = [
    path('criar/', CepCreateView.as_view(), name='criar_cep'),
    path('lista/', CepListView.as_view(), name='lista_cep'),
    path('editar/<int:pk>/', CepUpdateView.as_view(), name='editar_cep'),
    path('deletar/<int:pk>/', CepDeleteView.as_view(), name='deletar_cep'),
]