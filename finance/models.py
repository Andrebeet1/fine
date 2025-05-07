from django.db import models
from django.contrib.auth.models import User

class Budget(models.Model):
    annee = models.IntegerField(unique=True)  # Garantir que l'année est unique
    revenu_estime = models.DecimalField(max_digits=12, decimal_places=2)
    depense_estimee = models.DecimalField(max_digits=12, decimal_places=2)

    @property
    def solde_estime(self):
        return self.revenu_estime - self.depense_estimee

    def __str__(self):
        return f"Budget {self.annee}"

    class Meta:
        verbose_name = "Budget"
        verbose_name_plural = "Budgets"


class Projet(models.Model):
    nom = models.CharField(max_length=255)
    description = models.TextField(blank=True)  # Description peut être vide
    budget = models.ForeignKey(Budget, on_delete=models.SET_NULL, null=True, blank=True)
    montant_recu = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    etat = models.CharField(max_length=50, choices=[('en_cours', 'En Cours'), ('termine', 'Terminé')], default='en_cours')
    date_debut = models.DateField()
    date_fin = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.nom

    @property
    def solde_projet(self):
        return self.montant_recu - self.budget.revenu_estime if self.budget else 0

    class Meta:
        verbose_name = "Projet"
        verbose_name_plural = "Projets"


class Transaction(models.Model):
    TYPE_CHOICES = [
        ('revenu', 'Revenu'),
        ('depense', 'Dépense'),
    ]
    date = models.DateField(auto_now_add=True)  # Date de la transaction, auto remplie lors de l'ajout
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    montant = models.DecimalField(max_digits=12, decimal_places=2)
    description = models.TextField(blank=True)  # Description peut être vide
    projet = models.ForeignKey(Projet, on_delete=models.CASCADE, related_name='transactions', null=True, blank=True)
    utilisateur = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.get_type_display()} - {self.montant} FC le {self.date}"

    class Meta:
        verbose_name = "Transaction"
        verbose_name_plural = "Transactions"
        ordering = ['-date']  # Trier les transactions par date, les plus récentes en premier
