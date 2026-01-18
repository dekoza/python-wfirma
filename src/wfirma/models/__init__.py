"""Pydantic models for wFirma API data structures."""

from wfirma.models.base import (
    BaseXMLModel,
    DateTimeField,
    OptionalDateTimeField,
    ResponseParameters,
    ResponseStatus,
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

__all__ = [
    # Base models
    "BaseXMLModel",
    "DateTimeField",
    "OptionalDateTimeField",
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
]

