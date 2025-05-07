from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('budgets/', views.liste_budgets, name='liste_budgets'),
    path('budgets/ajouter/', views.ajouter_budget, name='ajouter_budget'),
    path('budgets/modifier/<int:pk>/', views.modifier_budget, name='modifier_budget'),
    path('budgets/supprimer/<int:pk>/', views.supprimer_budget, name='supprimer_budget'),

    path('projets/', views.liste_projets, name='liste_projets'),
    path('projets/ajouter/', views.ajouter_projet, name='ajouter_projet'),
    path('projets/modifier/<int:pk>/', views.modifier_projet, name='modifier_projet'),
    path('projets/supprimer/<int:pk>/', views.supprimer_projet, name='supprimer_projet'),

    path('transactions/', views.liste_transactions, name='liste_transactions'),
    path('transactions/ajouter/', views.ajouter_transaction, name='ajouter_transaction'),
    path('transactions/modifier/<int:pk>/', views.modifier_transaction, name='modifier_transaction'),
    path('transactions/supprimer/<int:pk>/', views.supprimer_transaction, name='supprimer_transaction'),
]
