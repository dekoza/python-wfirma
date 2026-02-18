"""Synchronous resource implementations."""

from wfirma.sync.resources.company import CompanyResource
from wfirma.sync.resources.company_accounts import CompanyAccountsResource
from wfirma.sync.resources.company_packs import CompanyPacksResource
from wfirma.sync.resources.contractors import ContractorResource
from wfirma.sync.resources.declaration_countries import DeclarationCountriesResource
from wfirma.sync.resources.expenses import ExpensesResource
from wfirma.sync.resources.goods import GoodsResource
from wfirma.sync.resources.interests import InterestsResource
from wfirma.sync.resources.invoice_descriptions import InvoiceDescriptionsResource
from wfirma.sync.resources.invoices import InvoicesResource
from wfirma.sync.resources.ledger_accountant_years import LedgerAccountantYearsResource
from wfirma.sync.resources.ledger_operation_schemas import LedgerOperationSchemasResource
from wfirma.sync.resources.payment_cashboxes import PaymentCashboxesResource
from wfirma.sync.resources.payments import PaymentsResource
from wfirma.sync.resources.tags import TagsResource
from wfirma.sync.resources.translation_languages import TranslationLanguagesResource
from wfirma.sync.resources.vat_codes import VatCodesResource
from wfirma.sync.resources.warehouse_documents_pw import WarehouseDocumentPWResource

__all__ = [
    "CompanyAccountsResource",
    "CompanyPacksResource",
    "CompanyResource",
    "ContractorResource",
    "DeclarationCountriesResource",
    "ExpensesResource",
    "GoodsResource",
    "InterestsResource",
    "InvoicesResource",
    "InvoiceDescriptionsResource",
    "LedgerAccountantYearsResource",
    "LedgerOperationSchemasResource",
    "PaymentCashboxesResource",
    "PaymentsResource",
    "TagsResource",
    "TranslationLanguagesResource",
    "VatCodesResource",
    "WarehouseDocumentPWResource",
]
