from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db.models import Sum
from .models import Consommation,  Operation

@receiver(post_save, sender=Consommation)
@receiver(post_delete, sender=Consommation)
def update_operation_montant_engage(sender, instance, **kwargs):
    operation = instance.operation
    total = Consommation.objects.filter(operation=operation).aggregate(
        total=Sum('montant_engage')
    )['total'] or 0
    operation.montant_engage = total
    operation.save()

@receiver(post_save, sender=Operation)
@receiver(post_delete, sender=Operation)
def update_tache_montant_engage(sender, instance, **kwargs):
    tache = instance.tache
    total = Operation.objects.filter(tache=tache).aggregate(
        total=Sum('montant')
    )['total'] or 0
    tache.montant_operation_restant = total
    tache.save()
