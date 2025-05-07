from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .models import Budget, Projet, Transaction
from .forms import BudgetForm, ProjetForm, TransactionForm
from django.contrib.auth import authenticate, login


def connexion(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('dashboard')
        else:
            return render(request, 'login.html', {'error': 'Identifiants invalides'})
    return render(request, 'login.html')


def ajouter_ou_modifier(request, form_class, model_class, template, success_message, redirect_url, pk=None):
    instance = None
    if pk:
        instance = get_object_or_404(model_class, pk=pk)

    if request.method == 'POST':
        form = form_class(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            messages.success(request, success_message)
            return redirect(redirect_url)
    else:
        form = form_class(instance=instance)
    
    return render(request, template, {'form': form})

@login_required
def dashboard(request):
    return render(request, 'finance/dashboard.html')

@login_required
def liste_budgets(request):
    budgets = Budget.objects.all().order_by('-annee')  # Tri par année décroissante
    paginator = Paginator(budgets, 10)  # 10 budgets par page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'finance/liste_budgets.html', {'page_obj': page_obj})

@login_required
def liste_projets(request):
    projets = Projet.objects.all().order_by('-date_debut')  # Tri par date de début
    paginator = Paginator(projets, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'finance/liste_projets.html', {'page_obj': page_obj})

@login_required
def liste_transactions(request):
    transactions = Transaction.objects.all().order_by('-date')  # Tri par date
    paginator = Paginator(transactions, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'finance/liste_transactions.html', {'page_obj': page_obj})

@login_required
def ajouter_budget(request):
    if not request.user.is_staff:  # Vérifie si l'utilisateur est administrateur
        messages.error(request, 'Vous n\'avez pas les permissions nécessaires.')
        return redirect('dashboard')
    
    return ajouter_ou_modifier(
        request,
        BudgetForm,
        Budget,
        'finance/formulaire.html',
        'Budget ajouté avec succès',
        'liste_budgets'
    )

@login_required
def ajouter_projet(request):
    if not request.user.is_staff:  # Vérifie si l'utilisateur est administrateur
        messages.error(request, 'Vous n\'avez pas les permissions nécessaires.')
        return redirect('dashboard')

    return ajouter_ou_modifier(
        request,
        ProjetForm,
        Projet,
        'finance/formulaire.html',
        'Projet ajouté avec succès',
        'liste_projets'
    )

@login_required
def ajouter_transaction(request):
    if not request.user.is_staff:  # Vérifie si l'utilisateur est administrateur
        messages.error(request, 'Vous n\'avez pas les permissions nécessaires.')
        return redirect('dashboard')

    return ajouter_ou_modifier(
        request,
        TransactionForm,
        Transaction,
        'finance/formulaire.html',
        'Transaction ajoutée avec succès',
        'liste_transactions'
    )

@login_required
def modifier_budget(request, pk):
    if not request.user.is_staff:
        messages.error(request, 'Vous n\'avez pas les permissions nécessaires.')
        return redirect('dashboard')

    return ajouter_ou_modifier(
        request,
        BudgetForm,
        Budget,
        'finance/formulaire.html',
        'Budget mis à jour avec succès',
        'liste_budgets',
        pk
    )

@login_required
def modifier_projet(request, pk):
    if not request.user.is_staff:
        messages.error(request, 'Vous n\'avez pas les permissions nécessaires.')
        return redirect('dashboard')

    return ajouter_ou_modifier(
        request,
        ProjetForm,
        Projet,
        'finance/formulaire.html',
        'Projet mis à jour avec succès',
        'liste_projets',
        pk
    )

@login_required
def modifier_transaction(request, pk):
    if not request.user.is_staff:
        messages.error(request, 'Vous n\'avez pas les permissions nécessaires.')
        return redirect('dashboard')

    return ajouter_ou_modifier(
        request,
        TransactionForm,
        Transaction,
        'finance/formulaire.html',
        'Transaction mise à jour avec succès',
        'liste_transactions',
        pk
    )

@login_required
def supprimer_budget(request, pk):
    if not request.user.is_staff:
        messages.error(request, 'Vous n\'avez pas les permissions nécessaires.')
        return redirect('dashboard')

    budget = get_object_or_404(Budget, pk=pk)
    budget.delete()
    messages.success(request, 'Budget supprimé avec succès')
    return redirect('liste_budgets')

@login_required
def supprimer_projet(request, pk):
    if not request.user.is_staff:
        messages.error(request, 'Vous n\'avez pas les permissions nécessaires.')
        return redirect('dashboard')

    projet = get_object_or_404(Projet, pk=pk)
    projet.delete()
    messages.success(request, 'Projet supprimé avec succès')
    return redirect('liste_projets')

@login_required
def supprimer_transaction(request, pk):
    if not request.user.is_staff:
        messages.error(request, 'Vous n\'avez pas les permissions nécessaires.')
        return redirect('dashboard')

    transaction = get_object_or_404(Transaction, pk=pk)
    transaction.delete()
    messages.success(request, 'Transaction supprimée avec succès')
    return redirect('liste_transactions')
