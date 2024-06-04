from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from transactions.models import Wallet, Transaction
from decimal import Decimal


class WalletViewSetTest(APITestCase):

    def setUp(self):
        self.wallet1 = Wallet.objects.create(
            label="Wallet 1", balance=Decimal("9.999999999999999999")
        )
        self.wallet2 = Wallet.objects.create(
            label="Wallet 2", balance=Decimal("8.000000000000000000")
        )
        for i in range(3, 13):
            Wallet.objects.create(
                label=f"Wallet {i}", balance=Decimal("10.000000000000000000")
            )

    def test_list_wallets(self):
        url = reverse("wallet-list")
        response = self.client.get(url, HTTP_ACCEPT="application/vnd.api+json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 10)

    def test_wallets_pagination(self):
        url = reverse("wallet-list")
        response = self.client.get(
            url, {"page": 1, "page_size": 5}, HTTP_ACCEPT="application/vnd.api+json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 5)

        response = self.client.get(
            url, {"page": 2, "page_size": 5}, HTTP_ACCEPT="application/vnd.api+json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 5)

        response = self.client.get(
            url, {"page": 3, "page_size": 5}, HTTP_ACCEPT="application/vnd.api+json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 2)


class TransactionViewSetTest(APITestCase):
    def setUp(self):
        self.wallet = Wallet.objects.create(
            label="Test Wallet", balance=Decimal("0.000000000000000000")
        )
        self.transaction1 = Transaction.objects.create(
            wallet=self.wallet, txid="tx123", amount=Decimal("1.000000000000000000")
        )
        self.transaction2 = Transaction.objects.create(
            wallet=self.wallet, txid="tx124", amount=Decimal("2.000000000000000000")
        )
        for i in range(3, 23):
            Transaction.objects.create(
                wallet=self.wallet,
                txid=f"tx{i}",
                amount=Decimal("3.000000000000000000"),
            )

    def test_list_transactions(self):
        url = reverse("transaction-list")
        response = self.client.get(url, HTTP_ACCEPT="application/vnd.api+json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 10)

    def test_transactions_pagination(self):
        url = reverse("transaction-list")
        response = self.client.get(
            url, {"page": 1, "page_size": 10}, HTTP_ACCEPT="application/vnd.api+json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 10)

        response = self.client.get(
            url, {"page": 2, "page_size": 10}, HTTP_ACCEPT="application/vnd.api+json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 10)

        response = self.client.get(
            url, {"page": 3, "page_size": 10}, HTTP_ACCEPT="application/vnd.api+json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 2)

    def test_filter_transactions_by_wallet_id(self):
        url = reverse("transaction-list")
        response = self.client.get(
            url,
            {"filter[wallet_id]": self.wallet.id, "page_size": 100},
            HTTP_ACCEPT="application/vnd.api+json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 22)
