import django_filters
from .models import Transaction, Wallet


class TransactionFilter(django_filters.FilterSet):
    min_amount = django_filters.NumberFilter(field_name="amount", lookup_expr="gte")
    max_amount = django_filters.NumberFilter(field_name="amount", lookup_expr="lte")
    wallet_id = django_filters.NumberFilter(field_name="wallet__id")

    class Meta:
        model = Transaction
        fields = ["amount", "wallet_id"]


class WalletFilter(django_filters.FilterSet):
    min_balance = django_filters.NumberFilter(field_name="balance", lookup_expr="gte")
    max_balance = django_filters.NumberFilter(field_name="balance", lookup_expr="lte")

    class Meta:
        model = Wallet
        fields = ["balance"]
