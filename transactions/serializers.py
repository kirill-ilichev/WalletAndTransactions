from rest_framework_json_api import serializers
from rest_framework.exceptions import ValidationError
from .models import Wallet, Transaction


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = "__all__"

    def update(self, instance, validated_data):
        raise ValidationError("Editing transactions is not allowed.")


class WalletSerializer(serializers.ModelSerializer):
    transactions = TransactionSerializer(many=True, read_only=True)

    class Meta:
        model = Wallet
        fields = "__all__"

    def update(self, instance, validated_data):
        if "balance" in validated_data:
            raise ValidationError("Editing wallet balance is not allowed.")
        return super().update(instance, validated_data)
