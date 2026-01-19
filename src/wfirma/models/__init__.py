"""Pydantic models for wFirma API data structures."""

from wfirma.models.base import (
    BaseXMLModel,
    DateTimeField,
    OptionalDateTimeField,
    ResponseParameters,
    ResponseStatus,
    TimestampedFieldsMixin,
    WFirmaBaseModel,
    format_wfirma_datetime,
    parse_wfirma_datetime,
)
from wfirma.models.common import (
    Address,
    BankAccount,
    CountryCode,
    Currency,
    Email,
    Money,
    Phone,
    PhoneNumber,
    TaxIdType,
    VATRate,
)
from wfirma.models.company import (
    CompanyAccount,
    CompanyAddress,
    CompanyDetail,
    UserCompany,
)
from wfirma.models.contractor import (
    Contractor,
    ContractorDetail,
)
from wfirma.models.employee import (
    User,
)
from wfirma.models.good import (
    Good,
    GoodType,
    WarehouseType,
)
from wfirma.models.invoice import (
    DisposalDateFormat,
    Invoice,
    InvoiceContent,
    InvoiceType,
    PaymentMethod,
    PaymentState,
)
from wfirma.models.payment import (
    Payment,
    PaymentCashbox,
    PaymentObjectType,
    PaymentType,
)
from wfirma.models.warehouse import (
    WarehouseDocument,
    WarehouseDocumentContent,
    WarehouseDocumentType,
)

__all__ = [
    # Base models
    "BaseXMLModel",
    "DateTimeField",
    "OptionalDateTimeField",
    "TimestampedFieldsMixin",
    "ResponseParameters",
    "ResponseStatus",
    "WFirmaBaseModel",
    "format_wfirma_datetime",
    "parse_wfirma_datetime",
    # Common models
    "Address",
    "BankAccount",
    "CountryCode",
    "Currency",
    "Email",
    "Money",
    "Phone",
    "PhoneNumber",
    "TaxIdType",
    "VATRate",
    # Company models
    "CompanyAccount",
    "CompanyAddress",
    "CompanyDetail",
    "UserCompany",
    # Contractor models
    "Contractor",
    "ContractorDetail",
    # Employee/User models
    "User",
    # Good models
    "Good",
    "GoodType",
    "WarehouseType",
    # Invoice models
    "DisposalDateFormat",
    "Invoice",
    "InvoiceContent",
    "InvoiceType",
    "PaymentMethod",
    "PaymentState",
    # Payment models
    "Payment",
    "PaymentCashbox",
    "PaymentObjectType",
    "PaymentType",
    # Warehouse models
    "WarehouseDocument",
    "WarehouseDocumentContent",
    "WarehouseDocumentType",
]
