from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase

from apps.finance.models.category import Category
from apps.finance.models.financial_account import FinancialAccount
from apps.finance.models.tag import Tag
from apps.finance.models.transaction import Transaction
from apps.finance.services.transaction_service import TransactionService


class TransactionServiceTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="tester",
            email="tester@example.com",
            password="12345678",
        )

        self.account = FinancialAccount.objects.create(
            user=self.user,
            name="Conta principal",
            account_type=FinancialAccount.AccountType.BANK,
        )

        self.category = Category.objects.create(
            user=self.user,
            name="Salário",
            type=Category.CategoryType.INCOME,
            color="#112233",
        )

        self.tag = Tag.objects.create(
            user=self.user,
            name="fixo",
            color="#445566",
        )

    def test_list_returns_only_user_transactions(self):
        other_user = get_user_model().objects.create_user(
            username="other",
            email="other@example.com",
            password="12345678",
        )
        other_account = FinancialAccount.objects.create(
            user=other_user,
            name="Outra conta",
            account_type=FinancialAccount.AccountType.BANK,
        )

        Transaction.objects.create(
            user=self.user,
            account=self.account,
            category=self.category,
            description="Recebimento",
            amount=Decimal("100.00"),
            type=Transaction.TransactionType.INCOME,
            date="2024-01-10",
        )
        Transaction.objects.create(
            user=other_user,
            account=other_account,
            category=self.category,
            description="Outro recebimento",
            amount=Decimal("200.00"),
            type=Transaction.TransactionType.INCOME,
            date="2024-01-11",
        )

        transactions = TransactionService.list(self.user)

        self.assertEqual(transactions.count(), 1)
        self.assertEqual(transactions[0].description, "Recebimento")

    def test_create_assigns_user_and_account(self):
        data = {
            "account": self.account,
            "category": self.category,
            "tags": [self.tag],
            "description": "Pagamento de aluguel",
            "amount": Decimal("250.00"),
            "type": Transaction.TransactionType.EXPENSE,
            "date": "2024-01-12",
            "status": Transaction.TransactionStatus.COMPLETED,
            "notes": "Cobrança mensal",
        }

        transaction = TransactionService.create(self.user, data)

        self.assertEqual(transaction.user, self.user)
        self.assertEqual(transaction.account, self.account)
        self.assertEqual(transaction.category, self.category)
        self.assertEqual(transaction.tags.count(), 1)
