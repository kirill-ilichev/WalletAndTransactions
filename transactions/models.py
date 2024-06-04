from decimal import Decimal
from django.db import models, transaction
from django.core.exceptions import ValidationError


class Wallet(models.Model):
    label = models.CharField(max_length=255)
    balance = models.DecimalField(max_digits=38, decimal_places=18, default=0)

    def update_balance(self, by_amount):
        with transaction.atomic():
            Wallet.objects.select_for_update().get(pk=self.pk)
            current_balance = self.balance
            future_balance = current_balance + by_amount
            # Validation to ensure the wallet balance never goes negative
            if future_balance < Decimal("0"):
                raise ValidationError("Wallet balance cannot be negative.")
            self.balance = future_balance
            self.save(
                update_fields=["balance"]
            )  # Update only the balance field to optimize the save operation

    def __str__(self):
        return self.label


class Transaction(models.Model):
    wallet = models.ForeignKey(
        Wallet, related_name="transactions", on_delete=models.PROTECT
    )
    txid = models.CharField(max_length=255, unique=True)
    amount = models.DecimalField(max_digits=38, decimal_places=18)

    def save(self, *args, **kwargs):
        # Prevent editing of existing transactions
        if self.pk is not None:
            raise ValidationError("Editing of existing transactions is not supported.")
        with transaction.atomic():
            super().save(*args, **kwargs)
            self.wallet.update_balance(
                self.amount
            )  # Update the wallet balance after saving the transaction

    def delete(self, *args, **kwargs):
        with transaction.atomic():
            super().delete(*args, **kwargs)
            self.wallet.update_balance(
                -self.amount
            )  # Adjust the wallet balance when a transaction is deleted

    def __str__(self):
        return self.txid
