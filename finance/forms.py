from django import forms
from .models import Budget, Projet, Transaction

class BudgetForm(forms.ModelForm):
    class Meta:
        model = Budget
        fields = ['annee', 'revenu_estime', 'depense_estimee']
        widgets = {
            'annee': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Année'}),
            'revenu_estime': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Revenu estimé'}),
            'depense_estimee': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Dépense estimée'}),
        }
    
    def clean_annee(self):
        annee = self.cleaned_data.get('annee')
        if annee < 1900 or annee > 2100:
            raise forms.ValidationError("L'année doit être entre 1900 et 2100.")
        return annee

class ProjetForm(forms.ModelForm):
    class Meta:
        model = Projet
        fields = ['nom', 'description', 'budget', 'montant_recu', 'etat']
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom du projet'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Description du projet'}),
            'budget': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Budget du projet'}),
            'montant_recu': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Montant reçu'}),
            'etat': forms.Select(attrs={'class': 'form-control'}),
        }

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        exclude = ['date']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields['date'] = forms.DateField(
                initial=self.instance.date,
                disabled=True,
                required=False
            )


    def clean_montant(self):
        montant = self.cleaned_data.get('montant')
        if montant <= 0:
            raise forms.ValidationError("Le montant doit être un nombre positif.")
        return montant
