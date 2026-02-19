"""Synchronous resource implementations."""

from wfirma.sync.resources.company import CompanyResource
from wfirma.sync.resources.company_accounts import CompanyAccountsResource
from wfirma.sync.resources.company_packs import CompanyPacksResource
from wfirma.sync.resources.contractors import ContractorResource
from wfirma.sync.resources.declaration_body_jpkvat import DeclarationBodyJpkvatResource
from wfirma.sync.resources.declaration_body_pit import DeclarationBodyPitResource
from wfirma.sync.resources.declaration_countries import DeclarationCountriesResource
from wfirma.sync.resources.documents import DocumentsResource
from wfirma.sync.resources.expenses import ExpensesResource
from wfirma.sync.resources.goods import GoodsResource
from wfirma.sync.resources.interests import InterestsResource
from wfirma.sync.resources.invoice_deliveries import InvoiceDeliveriesResource
from wfirma.sync.resources.invoice_descriptions import InvoiceDescriptionsResource
from wfirma.sync.resources.invoices import InvoicesResource
from wfirma.sync.resources.ledger_accountant_years import LedgerAccountantYearsResource
from wfirma.sync.resources.ledger_operation_schemas import LedgerOperationSchemasResource
from wfirma.sync.resources.notes import NotesResource
from wfirma.sync.resources.payment_cashboxes import PaymentCashboxesResource
from wfirma.sync.resources.payments import PaymentsResource
from wfirma.sync.resources.series import SeriesResource
from wfirma.sync.resources.tags import TagsResource
from wfirma.sync.resources.taxregisters import TaxregistersResource
from wfirma.sync.resources.term_groups import TermGroupsResource
from wfirma.sync.resources.terms import TermsResource
from wfirma.sync.resources.translation_languages import TranslationLanguagesResource
from wfirma.sync.resources.user_companies import UserCompaniesResource
from wfirma.sync.resources.users import UsersResource
from wfirma.sync.resources.vat_codes import VatCodesResource
from wfirma.sync.resources.vehicle_run_rates import VehicleRunRatesResource
from wfirma.sync.resources.vehicles import VehiclesResource
from wfirma.sync.resources.warehouse_documents_p_z import WarehouseDocumentPZResource
from wfirma.sync.resources.warehouse_documents_pw import WarehouseDocumentPWResource
from wfirma.sync.resources.warehouse_documents_r import WarehouseDocumentRResource
from wfirma.sync.resources.warehouse_documents_r_w import WarehouseDocumentRWResource
from wfirma.sync.resources.warehouse_documents_w_z import WarehouseDocumentWZResource
from wfirma.sync.resources.warehouse_documents_z_d import WarehouseDocumentZDResource
from wfirma.sync.resources.warehouse_documents_z_p_d import WarehouseDocumentZPDResource
from wfirma.sync.resources.warehouse_documents_z_p_m import WarehouseDocumentZPMResource
from wfirma.sync.resources.warehouses import WarehousesResource
from wfirma.sync.resources.webhooks import WebhooksResource

__all__ = [
    "CompanyAccountsResource",
    "CompanyPacksResource",
    "CompanyResource",
    "ContractorResource",
    "DeclarationBodyJpkvatResource",
    "DeclarationBodyPitResource",
    "DeclarationCountriesResource",
    "DocumentsResource",
    "ExpensesResource",
    "GoodsResource",
    "InterestsResource",
    "InvoiceDeliveriesResource",
    "InvoiceDescriptionsResource",
    "InvoicesResource",
    "LedgerAccountantYearsResource",
    "LedgerOperationSchemasResource",
    "NotesResource",
    "PaymentCashboxesResource",
    "PaymentsResource",
    "SeriesResource",
    "TagsResource",
    "TaxregistersResource",
    "TermGroupsResource",
    "TermsResource",
    "TranslationLanguagesResource",
    "UserCompaniesResource",
    "UsersResource",
    "VatCodesResource",
    "VehicleRunRatesResource",
    "VehiclesResource",
    "WarehouseDocumentPWResource",
    "WarehouseDocumentPZResource",
    "WarehouseDocumentRResource",
    "WarehouseDocumentRWResource",
    "WarehouseDocumentWZResource",
    "WarehouseDocumentZDResource",
    "WarehouseDocumentZPDResource",
    "WarehouseDocumentZPMResource",
    "WarehousesResource",
    "WebhooksResource",
]
