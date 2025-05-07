from django.contrib import admin
from .models import Budget, Projet, Transaction

@admin.register(Budget)
class BudgetAdmin(admin.ModelAdmin):
    list_display = ('annee', 'revenu_estime', 'depense_estimee', 'solde_estime')
    search_fields = ('annee',)
    list_filter = ('annee',)
    readonly_fields = ('solde_estime',)

@admin.register(Projet)
class ProjetAdmin(admin.ModelAdmin):
    list_display = ('nom', 'etat', 'budget', 'montant_recu', 'date_debut', 'date_fin', 'solde_projet')
    search_fields = ('nom',)
    list_filter = ('etat', 'date_debut', 'date_fin')
    readonly_fields = ('solde_projet',)

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('date', 'type', 'montant', 'description', 'projet', 'utilisateur')
    search_fields = ('description', 'projet__nom', 'utilisateur__username')
    list_filter = ('type', 'date', 'projet', 'utilisateur')
    date_hierarchy = 'date'
