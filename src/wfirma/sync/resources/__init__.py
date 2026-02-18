"""Synchronous resource implementations."""

from wfirma.sync.resources.company import CompanyResource
from wfirma.sync.resources.company_accounts import CompanyAccountsResource
from wfirma.sync.resources.contractors import ContractorResource
from wfirma.sync.resources.goods import GoodsResource
from wfirma.sync.resources.invoices import InvoicesResource
from wfirma.sync.resources.payments import PaymentsResource
from wfirma.sync.resources.tags import TagsResource
from wfirma.sync.resources.warehouse_documents_pw import WarehouseDocumentPWResource

__all__ = [
    "CompanyAccountsResource",
    "CompanyResource",
    "ContractorResource",
    "GoodsResource",
    "InvoicesResource",
    "PaymentsResource",
    "WarehouseDocumentPWResource",
    "TagsResource",
]
