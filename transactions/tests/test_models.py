from django.test import TestCase
from django.core.exceptions import ValidationError
from transactions.models import Wallet, Transaction
from decimal import Decimal


class WalletModelTest(TestCase):

    def setUp(self):
        self.wallet = Wallet.objects.create(label="Test Wallet")

    def test_wallet_creation(self):
        self.assertEqual(self.wallet.label, "Test Wallet")
        self.assertEqual(self.wallet.balance, Decimal("0"))

    def test_update_balance_positive(self):
        self.wallet.update_balance(Decimal("100.00"))
        self.assertEqual(self.wallet.balance, Decimal("100.00"))

    def test_update_balance_negative(self):
        self.wallet.update_balance(Decimal("50.00"))
        self.assertEqual(self.wallet.balance, Decimal("50.00"))
        self.wallet.update_balance(Decimal("-50.00"))
        self.assertEqual(self.wallet.balance, Decimal("0"))

    def test_update_balance_negative_exception(self):
        with self.assertRaises(ValidationError):
            self.wallet.update_balance(Decimal("-1.00"))


class TransactionModelTest(TestCase):
    def setUp(self):
        self.wallet = Wallet.objects.create(label="Test Wallet")

    def test_transaction_creation(self):
        transaction = Transaction.objects.create(
            wallet=self.wallet, txid="tx123", amount=Decimal("100.00")
        )
        self.assertEqual(transaction.txid, "tx123")
        self.assertEqual(transaction.amount, Decimal("100.00"))
        self.assertEqual(self.wallet.balance, Decimal("100.00"))

    def test_transaction_creation_updates_wallet_balance(self):
        Transaction.objects.create(
            wallet=self.wallet, txid="tx123", amount=Decimal("100.00")
        )
        self.assertEqual(self.wallet.balance, Decimal("100.00"))

    def test_transaction_deletion_updates_wallet_balance(self):
        transaction = Transaction.objects.create(
            wallet=self.wallet, txid="tx123", amount=Decimal("100.00")
        )
        self.assertEqual(self.wallet.balance, Decimal("100.00"))
        transaction.delete()
        self.assertEqual(self.wallet.balance, Decimal("0.00"))

    def test_transaction_editing_exception(self):
        transaction = Transaction.objects.create(
            wallet=self.wallet, txid="tx123", amount=Decimal("100.00")
        )
        with self.assertRaises(ValidationError):
            transaction.save()
