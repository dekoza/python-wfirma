# wFirma.pl Reference

## Overview

**Base URL:** `https://api2.wfirma.pl`

## Authentication

Supported authentication methods: oauth2, apikey

## Endpoints

### companies

#### companies/get

**Method:** `GET`

**Path:** `/{{host}}/companies/get/{{companyId}}?outputFormat=xml&inputFormat=xml&company_id={{companyId}}`

---

### company_accounts

#### company_accounts/find

**Method:** `GET`

**Path:** `/{{host}}/company_accounts/find?inputFormat=xml&outputFormat=xml&company_id={{companyId}}`

---

#### company_accounts/get

**Method:** `GET`

**Path:** `/{{host}}/company_accounts/get/{{companyAcoountId}}?inputFormat=xml&outputFormat=xml&company_id={{companyId}}`

---

### company_addresses

#### company_addresses/findMain

**Method:** `GET`

**Path:** `/{{host}}/company_addresses/findmain?outputFormat=xml&inputFormat=xml&company_id={{companyId}}`

---

### company_packs

#### company_packs/get

**Method:** `GET`

**Path:** `/{{host}}/company_packs/get/{{companyPackId}}?inputFormat=xml&outputFormat=xml&company_id={{companyId}}`

---

### contractors

#### contractors/add

**Method:** `POST`

**Path:** `/{{host}}/contractors/add?inputFormat=xml&outputFormat=xml&company_id={{companyId}}`

---

#### contractors/find

**Method:** `GET`

**Path:** `/{{host}}/contractors/find?outputFormat=xml&company_id={{companyId}}`

---

#### contractors/get

**Method:** `GET`

**Path:** `/{{host}}/contractors/get/{{contractorId}}?inputFormat=xml&outputFormat=xml&company_id={{companyId}}`

---

#### contractors/edit

**Method:** `POST`

**Path:** `/{{host}}/contractors/edit/{{contractorId}}?inputFormat=xml&outputFormat=xml&company_id={{companyId}}`

---

#### contractors/delete

**Method:** `DELETE`

**Path:** `/{{host}}/contractors/delete/{{contractorId}}?inputFormat=xml&outputFormat=xml&company_id={{companyId}}`

---

### declaration_body_jpkvat

#### declaration_body_jpkvat/get

**Method:** `GET`

**Path:** `/{{host}}/declaration_body_jpkvat/get/{{year}}/{{month}}?outputFormat=xml&inputFormat=xml&company_id={{companyId}}`

---

### declaration_body_pit

#### declaration_body_pit/get

**Method:** `GET`

**Path:** `/{{host}}/declaration_body_pit/get/{{type}}/{{year}}?outputFormat=xml&inputFormat=xml&company_id={{companyId}}`

---

### declaration_countries

#### declaration_countries/find

**Method:** `GET`

**Path:** `/{{host}}/declaration_countries/find?outputFormat=xml&inputFormat=xml&company_id={{companyId}}`

---

#### declaration_countries/get

**Method:** `GET`

**Path:** `/{{host}}/declaration_countries/get/{{declarationCountryId}}?outputFormat=xml&inputFormat=xml&company_id={{companyId}}`

---

### documents

#### documents/add

**Method:** `POST`

**Path:** `/{{host}}/documents/add?inputFormat=xml&outputFormat=xml&company_id={{companyId}}`

---

#### documents/find

**Method:** `GET`

**Path:** `/{{host}}/documents/find?outputFormat=xml&inputFormat=xml&company_id={{companyId}}`

---

#### documents/get

**Method:** `GET`

**Path:** `/{{host}}/documents/get/{{documentId}}?outputFormat=xml&inputFormat=xml&company_id={{companyId}}`

---

#### documents/download

**Method:** `GET`

**Path:** `/{{host}}/documents/download/{{documentId}}?outputFormat=xml&inputFormat=xml&company_id={{companyId}}`

---

#### documents/delete

**Method:** `DELETE`

**Path:** `/{{host}}/documents/delete/{{documentId}}?outputFormat=xml&inputFormat=xml&company_id={{companyId}}`

---

### expenses

#### expenses/find

**Method:** `GET`

**Path:** `/{{host}}/expenses/find?outputFormat=xml&inputFormat=xml&company_id={{companyId}}`

---

#### expenses/get

**Method:** `GET`

**Path:** `/{{host}}/expenses/get/{{expenseId}}?outputFormat=xml&inputFormat=xml&company_id={{companyId}}`

---

### goods

#### goods/add

**Method:** `POST`

**Path:** `/{{host}}/goods/add?outputFormat=xml&inputFormat=xml&company_id={{companyId}}`

---

#### goods/find

**Method:** `GET`

**Path:** `/{{host}}/goods/find?outputFormat=xml&inputFormat=xml&company_id={{companyId}}`

---

#### goods/get

**Method:** `GET`

**Path:** `/{{host}}/goods/get/{{goodId}}?outputFormat=xml&inputFormat=xml&company_id={{companyId}}`

---

#### goods/edit

**Method:** `POST`

**Path:** `/{{host}}/goods/edit/{{goodId}}?outputFormat=xml&inputFormat=xml&company_id={{companyId}}`

---

#### goods/delete

**Method:** `DELETE`

**Path:** `/{{host}}/goods/delete/{{goodId}}?outputFormat=xml&inputFormat=xml&company_id={{companyId}}`

---

### interests

#### interests/find

**Method:** `GET`

**Path:** `/{{host}}/interests/find?outputFormat=xml&inputFormat=xml&company_id={{companyId}}`

---

### invoice_deliveries

#### invoice_deliveries/add

**Method:** `POST`

**Path:** `/{{host}}/invoice_deliveries/add?outputFormat=xml&inputFormat=xml&company_id={{companyId}}`

---

#### invoice_deliveries/find

**Method:** `GET`

**Path:** `/{{host}}/invoice_deliveries/find?outputFormat=xml&inputFormat=xml&company_id={{companyId}}`

---

#### invoice_deliveries/get

**Method:** `GET`

**Path:** `/{{host}}/invoice_deliveries/get/{{invoiceDeliveryId}}?outputFormat=xml&inputFormat=xml&company_id={{companyId}}`

---

#### invoice_deliveries/delete

**Method:** `DELETE`

**Path:** `/{{host}}/invoice_deliveries/delete/{{invoiceDeliveryId}}?outputFormat=xml&inputFormat=xml&company_id={{companyId}}`

---

### invoice_descriptions

#### invoice_descriptions/find

**Method:** `GET`

**Path:** `/{{host}}/invoice_descriptions/find?outputFormat=xml&inputFormat=xml&company_id={{companyId}}`

---

#### invoice_descriptions/get

**Method:** `GET`

**Path:** `/{{host}}/invoice_descriptions/get/{{invoiceDescriptionsId}}?outputFormat=xml&inputFormat=xml&company_id={{companyId}}`

---

### invoice_ledger

#### invoices/add

**Method:** `POST`

**Path:** `/{{host}}/invoices/add?outputFormat=xml&inputFormat=xml&company_id={{companyId}}`

---

#### invoices/find

**Method:** `GET`

**Path:** `/{{host}}/invoices/find?outputFormat=xml&inputFormat=xml&company_id={{companyId}}`

---

#### invoices/get

**Method:** `GET`

**Path:** `/{{host}}/invoices/get/{{invoiceId}}?outputFormat=xml&inputFormat=xml&company_id={{companyId}}`

---

#### invoices/download

**Method:** `POST`

**Path:** `/{{host}}/invoices/download/{{invoiceId}}?outputFormat=xml&inputFormat=xml&company_id={{companyId}}`

---

#### invoices/send

**Method:** `POST`

**Path:** `/{{host}}/invoices/send/{{invoiceId}}?outputFormat=xml&inputFormat=xml&company_id={{companyId}}`

---

### invoices

#### invoices/add

**Method:** `POST`

**Path:** `/{{host}}/invoices/add?outputFormat=xml&inputFormat=xml&company_id={{companyId}}`

---

#### invoices/find

**Method:** `GET`

**Path:** `/{{host}}/invoices/find?outputFormat=xml&inputFormat=xml&company_id={{companyId}}`

---

#### invoices/get

**Method:** `GET`

**Path:** `/{{host}}/invoices/get/{{invoiceId}}?outputFormat=xml&inputFormat=xml&company_id={{companyId}}`

---

#### invoices/download

**Method:** `POST`

**Path:** `/{{host}}/invoices/download/{{invoiceId}}?outputFormat=xml&inputFormat=xml&company_id={{companyId}}`

---

#### invoices/fiscalize

**Method:** `GET`

**Path:** `/{{host}}/invoices/fiscalize/{{invoiceId}}?outputFormat=xml&inputFormat=xml&company_id={{companyId}}`

---

#### invoices/unfiscalize

**Method:** `GET`

**Path:** `/{{host}}/invoices/unfiscalize/{{invoiceId}}?outputFormat=xml&inputFormat=xml&company_id={{companyId}}`

---

#### invoices/send

**Method:** `POST`

**Path:** `/{{host}}/invoices/send/{{invoiceId}}?outputFormat=xml&inputFormat=xml&company_id={{companyId}}`

---

#### invoices/edit

**Method:** `POST`

**Path:** `/{{host}}/invoices/edit/{{invoiceId}}?outputFormat=xml&inputFormat=xml&company_id={{companyId}}`

---

#### invoices/delete

**Method:** `DELETE`

**Path:** `/{{host}}/invoices/delete/{{invoiceId}}?outputFormat=xml&inputFormat=xml&company_id={{companyId}}`

---

#### ereceipt_integration_receipt

**Method:** `GET`

**Path:** `/{{host}}/invoices/add?outputFormat=xml&inputFormat=xml&company_id={{companyId}}`

---

### invoices_correction

#### invoices/add

**Method:** `POST`

**Path:** `/{{host}}/invoices/add?outputFormat=xml&inputFormat=xml&company_id={{companyId}}`

---

### ledger_accountant_years

#### ledger_accountant_years/find

**Method:** `GET`

**Path:** `/{{host}}/ledger_accountant_years/find/?inputFormat=xml&outputFormat=xml&company_id={{companyId}}`

---

#### ledger_accountant_years/get

**Method:** `GET`

**Path:** `/{{host}}/ledger_accountant_years/get/625?inputFormat=xml&outputFormat=xml&company_id={{companyId}}`

---

### ledger_operation_schemas

#### ledger_operation_schemas/find

**Method:** `GET`

**Path:** `/{{host}}/ledger_operation_schemas/find?outputFormat=xml&inputFormat=xml&company_id={{companyId}}`

---

#### ledger_operation_schemas/get

**Method:** `GET`

**Path:** `/{{host}}/ledger_operation_schemas/get/{{ledger_operation_schemas_id}}?outputFormat=xml&inputFormat=xml&company_id={{companyId}}`

---

### notes

#### notes/add

**Method:** `POST`

**Path:** `/{{host}}/notes/add?outputFormat=xml&inputFormat=xml&company_id={{companyId}}`

---

#### notes/find

**Method:** `GET`

**Path:** `/{{host}}/notes/find?outputFormat=xml&inputFormat=xml&company_id={{companyId}}`

---

#### notes/get

**Method:** `GET`

**Path:** `/{{host}}/notes/get/{{noteId}}?outputFormat=xml&inputFormat=xml&company_id={{companyId}}`

---

#### notes/edit

**Method:** `POST`

**Path:** `/{{host}}/goods/notes/{{noteId}}?outputFormat=xml&inputFormat=xml&company_id={{companyId}}`

---

#### notes/delete

**Method:** `DELETE`

**Path:** `/{{host}}/notes/delete/{{noteId}}?outputFormat=xml&inputFormat=xml&company_id={{companyId}}`

---

### payment_cashboxes

#### payment_cashboxes/find

**Method:** `GET`

**Path:** `/{{host}}/payment_cashboxes/find?outputFormat=xml&inputFormat=xml&company_id={{companyId}}`

---

#### payment_cashboxes/get

**Method:** `GET`

**Path:** `/{{host}}/payment_cashboxes/get/{{paymentCashboxId}}?outputFormat=xml&inputFormat=xml&company_id={{companyId}}`

---

### payments

#### payments/add

**Method:** `POST`

**Path:** `/{{host}}/payments/add?outputFormat=xml&inputFormat=xml&company_id={{companyId}}`

---

#### payments/find

**Method:** `GET`

**Path:** `/{{host}}/payments/find?outputFormat=xml&inputFormat=xml&company_id={{companyId}}`

---

#### payments/get

**Method:** `GET`

**Path:** `/{{host}}/payments/get/{{paymentId}}?outputFormat=xml&inputFormat=xml&company_id={{companyId}}`

---

#### payments/edit

**Method:** `POST`

**Path:** `/{{host}}/payments/edit/{{paymentId}}?outputFormat=xml&inputFormat=xml&company_id={{companyId}}`

---

#### payments/delete

**Method:** `DELETE`

**Path:** `/{{host}}/payments/delete/{{paymentId}}?outputFormat=xml&inputFormat=xml&company_id={{companyId}}`

---

### series

#### series/add

**Method:** `POST`

**Path:** `/{{host}}/series/add?outputFormat=xml&inputFormat=xml&company_id={{companyId}}`

---

#### series/find

**Method:** `GET`

**Path:** `/{{host}}/series/find?outputFormat=xml&inputFormat=xml&company_id={{companyId}}`

---

#### series/get

**Method:** `GET`

**Path:** `/{{host}}/series/get/{{seriesId}}?outputFormat=xml&inputFormat=xml&company_id={{companyId}}`

---

#### series/edit

**Method:** `POST`

**Path:** `/{{host}}/series/notes/ID?outputFormat=xml&inputFormat=xml`

---

#### series/del

**Method:** `DELETE`

**Path:** `/{{host}}/series/del/ID?outputFormat=xml&inputFormat=xml`

---

### tags

#### tags/add

**Method:** `POST`

**Path:** `/{{host}}/tags/add?outputFormat=xml&inputFormat=xml&company_id={{companyId}}`

---

#### tags/find

**Method:** `GET`

**Path:** `/{{host}}/tags/find?outputFormat=xml&inputFormat=xml&company_id={{companyId}}`

---

#### tags/get

**Method:** `GET`

**Path:** `/{{host}}/tags/get/{{tagId}}?outputFormat=xml&inputFormat=xml&company_id={{companyId}}`

---

#### tags/edit

**Method:** `POST`

**Path:** `/{{host}}/tags/notes/{{termId}}?outputFormat=xml&inputFormat=xml&company_id={{companyId}}`

---

#### tags/delete

**Method:** `DELETE`

**Path:** `/{{host}}/tags/delete/{{termId}}?outputFormat=xml&inputFormat=xml&company_id={{companyId}}`

---

### taxregisters

#### taxregisters/get

**Method:** `GET`

**Path:** `/{{host}}/taxregisters/get/{{year}}/{{month}}?outputFormat=xml&inputFormat=xml&company_id={{companyId}}`

---

### term_groups

#### term_groups/add

**Method:** `POST`

**Path:** `/{{host}}/term_groups/add?outputFormat=xml&inputFormat=xml&company_id={{companyId}}`

---

#### term_groups/find

**Method:** `GET`

**Path:** `/{{host}}/term_groups/find?outputFormat=xml&inputFormat=xml&company_id={{companyId}}`

---

#### term_groups/get

**Method:** `GET`

**Path:** `/{{host}}/term_groups/get/{{termGroupId}}?outputFormat=xml&inputFormat=xml&company_id={{companyId}}`

---

#### term_groups/edit

**Method:** `POST`

**Path:** `/{{host}}/term_groups/notes/{{termGroupId}}?outputFormat=xml&inputFormat=xml&company_id={{companyId}}`

---

#### term_groups/delete

**Method:** `DELETE`

**Path:** `/{{host}}/term_groups/delete/{{termGroupId}}?outputFormat=xml&inputFormat=xml&company_id={{companyId}}`

---

### terms

#### terms/add

**Method:** `POST`

**Path:** `/{{host}}/terms/add?outputFormat=xml&inputFormat=xml&company_id={{companyId}}`

---

#### terms/find

**Method:** `GET`

**Path:** `/{{host}}/terms/find?outputFormat=xml&inputFormat=xml&company_id={{companyId}}`

---

#### terms/get

**Method:** `GET`

**Path:** `/{{host}}/terms/get/{{termId}}?outputFormat=xml&inputFormat=xml&company_id={{companyId}}`

---

#### terms/edit

**Method:** `POST`

**Path:** `/{{host}}/terms/notes/{{termId}}?outputFormat=xml&inputFormat=xml&company_id={{companyId}}`

---

#### terms/delete

**Method:** `DELETE`

**Path:** `/{{host}}/terms/delete/{{termId}}?outputFormat=xml&inputFormat=xml&company_id={{companyId}}`

---

### translation_languages

#### translation_languages/find

**Method:** `GET`

**Path:** `/{{host}}/translation_languages/find?outputFormat=xml&inputFormat=xml&company_id={{companyId}}`

---

#### translation_languages/get

**Method:** `GET`

**Path:** `/{{host}}/translation_languages/get/{{translationLanguageId}}?outputFormat=xml&inputFormat=xml&company_id={{companyId}}`

---

### user_companies

#### user_companies/find

**Method:** `GET`

**Path:** `/{{host}}/user_companies/find?inputFormat=xml&outputFormat=xml`

---

#### user_companies/get

**Method:** `GET`

**Path:** `/{{host}}/user_companies/get/{{userCompanyId}}?inputFormat=xml&outputFormat=xml`

---

### users

#### users/get

**Method:** `GET`

**Path:** `/{{host}}/users/get/{{userCompanyId}}?outputFormat=xml&inputFormat=xml&company_id={{companyId}}`

---

### vat_codes

#### vat_codes/find

**Method:** `GET`

**Path:** `/{{host}}/vat_codes/find?outputFormat=xml&inputFormat=xml&company_id={{companyId}}`

---

#### vat_codes/get

**Method:** `GET`

**Path:** `/{{host}}/vat_codes/get/{{vatCodeId}}?outputFormat=xml&inputFormat=xml&company_id={{companyId}}`

---

### vehicle_run_rates

#### vehicle_run_rates/find

**Method:** `GET`

**Path:** `/{{host}}/vehicle_run_rates/find?outputFormat=xml&inputFormat=xml&company_id={{companyId}}`

---

### vehicles

#### vehicles/add

**Method:** `POST`

**Path:** `/{{host}}/vehicles/add/?outputFormat=xml&inputFormat=xml&company_id={{companyId}}`

---

#### vehicles/delete

**Method:** `GET`

**Path:** `/{{host}}/vehicles/delete/{{vehicleId}}?outputFormat=xml&inputFormat=xml&company_id={{companyId}}`

---

#### vehicles/edit

**Method:** `POST`

**Path:** `/{{host}}/vehicles/edit/{{vehicleId}}?outputFormat=xml&inputFormat=xml&company_id={{companyId}}`

---

#### vehicles/get

**Method:** `GET`

**Path:** `/{{host}}/vehicles/get/{{vehicleId}}?outputFormat=xml&inputFormat=xml&company_id={{companyId}}`

---

#### vehicles/find

**Method:** `GET`

**Path:** `/{{host}}/vehicles/find?outputFormat=xml&inputFormat=xml&company_id={{companyId}}`

---

### warehouse_documents/p_w

#### warehouse_document_p_w/add

**Method:** `POST`

**Path:** `/warehouse_document_p_w/add?outputFormat=xml&inputFormat=xml&company_id={{companyId}}`

---

#### warehouse_document_p_w/find

**Method:** `GET`

**Path:** `/{{host}}/warehouse_document_p_w/find?outputFormat=xml&inputFormat=xml&company_id={{companyId}}`

---

#### warehouse_document_p_w/get

**Method:** `GET`

**Path:** `/{{host}}/warehouse_document_p_w/get/{{warehouseDocumentId}}?outputFormat=xml&inputFormat=xml&company_id={{companyId}}`

---

#### warehouse_document_p_w/edit

**Method:** `POST`

**Path:** `/{{host}}/warehouse_document_p_w/edit/{{warehouseDocumentId}}?outputFormat=xml&inputFormat=xml&company_id={{companyId}}`

---

#### warehouse_document_p_w/delete

**Method:** `DELETE`

**Path:** `/warehouse_document_p_w/delete/53487196?outputFormat=xml&inputFormat=xml&company_id={{companyId}}`

---

### warehouse_documents/p_z

#### warehouse_document_p_z/add

**Method:** `POST`

**Path:** `/{{host}}/warehouse_document_p_z/add?outputFormat=xml&inputFormat=xml&company_id={{companyId}}`

---

#### warehouse_document_p_z/find

**Method:** `GET`

**Path:** `/{{host}}/warehouse_document_p_z/find?outputFormat=xml&inputFormat=xml&company_id={{companyId}}`

---

#### warehouse_document_p_z/get

**Method:** `GET`

**Path:** `/{{host}}/warehouse_document_p_z/get/{{warehouseDocumentId}}?outputFormat=xml&inputFormat=xml&company_id={{companyId}}`

---

#### warehouse_document_p_z/edit

**Method:** `POST`

**Path:** `/{{host}}/warehouse_document_p_z/edit/{{warehouseDocumentId}}?outputFormat=xml&inputFormat=xml&company_id={{companyId}}`

---

#### warehouse_document_p_z/delete

**Method:** `DELETE`

**Path:** `/{{host}}/warehouse_document_p_z/delete/{{warehouseDocumentId}}?outputFormat=xml&inputFormat=xml&company_id={{companyId}}`

---

### warehouse_documents/r

#### warehouse_document_r/add

**Method:** `POST`

**Path:** `/{{host}}/warehouse_document_r/add?outputFormat=xml&inputFormat=xml&company_id={{companyId}}`

---

#### warehouse_document_r/find

**Method:** `GET`

**Path:** `/{{host}}/warehouse_document_r/find?outputFormat=xml&inputFormat=xml&company_id={{companyId}}`

---

#### warehouse_document_r/get

**Method:** `GET`

**Path:** `/{{host}}/warehouse_document_r/get/{{warehouseDocumentId}}?outputFormat=xml&inputFormat=xml&company_id={{companyId}}`

---

#### warehouse_document_r/edit

**Method:** `POST`

**Path:** `/{{host}}/warehouse_document_r/edit/{{warehouseDocumentId}}?outputFormat=xml&inputFormat=xml&company_id={{companyId}}`

---

#### warehouse_document_r/delete

**Method:** `DELETE`

**Path:** `/{{host}}/warehouse_document_r/delete/{{warehouseDocumentId}}?outputFormat=xml&inputFormat=xml&company_id={{companyId}}`

---

### warehouse_documents/r_w

#### warehouse_document_r_w/add

**Method:** `POST`

**Path:** `/{{host}}/warehouse_document_r_w/add?outputFormat=xml&inputFormat=xml&company_id={{companyId}}`

---

#### warehouse_document_r_w/find

**Method:** `GET`

**Path:** `/{{host}}/warehouse_document_r_w/find?outputFormat=xml&inputFormat=xml&company_id={{companyId}}`

---

#### warehouse_document_r_w/get

**Method:** `GET`

**Path:** `/{{host}}/warehouse_document_r_w/get/{{warehouseDocumentId}}?outputFormat=xml&inputFormat=xml&company_id={{companyId}}`

---

#### warehouse_document_r_w/edit

**Method:** `POST`

**Path:** `/{{host}}/warehouse_document_r_w/edit/{{warehouseDocumentId}}?outputFormat=xml&inputFormat=xml&company_id={{companyId}}`

---

#### warehouse_document_r_w/delete

**Method:** `DELETE`

**Path:** `/{{host}}/warehouse_document_r_w/delete/{{warehouseDocumentId}}?outputFormat=xml&inputFormat=xml&company_id={{companyId}}`

---

### warehouse_documents/w_z

#### warehouse_document_w_z/add

**Method:** `POST`

**Path:** `/{{host}}/warehouse_document_w_z/add?outputFormat=xml&inputFormat=xml&company_id={{companyId}}`

---

#### warehouse_document_w_z/find

**Method:** `GET`

**Path:** `/{{host}}/warehouse_document_w_z/find?outputFormat=xml&inputFormat=xml&company_id={{companyId}}`

---

#### warehouse_document_w_z/get

**Method:** `GET`

**Path:** `/{{host}}/warehouse_document_w_z/get/{{warehouseDocumentId}}?outputFormat=xml&inputFormat=xml&company_id={{companyId}}`

---

#### warehouse_document_w_z/edit

**Method:** `POST`

**Path:** `/{{host}}/warehouse_document_w_z/edit/{{warehouseDocumentId}}?outputFormat=xml&inputFormat=xml&company_id={{companyId}}`

---

#### warehouse_document_w_z/delete

**Method:** `DELETE`

**Path:** `/{{host}}/warehouse_document_w_z/delete/{{warehouseDocumentId}}?outputFormat=xml&inputFormat=xml&company_id={{companyId}}`

---

### warehouse_documents/z_d

#### warehouse_document_z_d/add

**Method:** `POST`

**Path:** `/{{host}}/warehouse_document_z_d/add?outputFormat=xml&inputFormat=xml&company_id={{companyId}}`

---

#### warehouse_document_z_d/find

**Method:** `GET`

**Path:** `/{{host}}/warehouse_document_z_d/find?outputFormat=xml&inputFormat=xml&company_id={{companyId}}`

---

#### warehouse_document_z_d/get

**Method:** `GET`

**Path:** `/{{host}}/warehouse_document_z_d/get/{{warehouseDocumentId}}?outputFormat=xml&inputFormat=xml&company_id={{companyId}}`

---

#### warehouse_document_z_d/edit

**Method:** `POST`

**Path:** `/{{host}}/warehouse_document_z_d/edit/{{warehouseDocumentId}}?outputFormat=xml&inputFormat=xml&company_id={{companyId}}`

---

#### warehouse_document_z_d/delete

**Method:** `DELETE`

**Path:** `/{{host}}/warehouse_document_z_d/delete/{{warehouseDocumentId}}?outputFormat=xml&inputFormat=xml&company_id={{companyId}}`

---

### warehouse_documents/z_p_d

#### warehouse_document_z_p_d/add

**Method:** `POST`

**Path:** `/{{host}}/warehouse_document_z_p_d/add?outputFormat=xml&inputFormat=xml&company_id={{companyId}}`

---

#### warehouse_document_z_p_d/find

**Method:** `GET`

**Path:** `/{{host}}/warehouse_document_z_p_d/find?outputFormat=xml&inputFormat=xml&company_id={{companyId}}`

---

#### warehouse_document_z_p_d/get

**Method:** `GET`

**Path:** `/{{host}}/warehouse_document_z_p_d/get/{{warehouseDocumentId}}?outputFormat=xml&inputFormat=xml&company_id={{companyId}}`

---

#### warehouse_document_z_p_d/edit

**Method:** `POST`

**Path:** `/{{host}}/warehouse_document_z_p_d/edit/{{warehouseDocumentId}}?outputFormat=xml&inputFormat=xml&company_id={{companyId}}`

---

#### warehouse_document_z_p_d/delete

**Method:** `DELETE`

**Path:** `/{{host}}/warehouse_document_z_p_d/delete/{{warehouseDocumentId}}?outputFormat=xml&inputFormat=xml&company_id={{companyId}}`

---

### warehouse_documents/z_p_m

#### warehouse_document_z_p_m/add

**Method:** `POST`

**Path:** `/{{host}}/warehouse_document_z_p_m/add?outputFormat=xml&inputFormat=xml&company_id={{companyId}}`

---

#### warehouse_document_z_p_m/find

**Method:** `GET`

**Path:** `/{{host}}/warehouse_document_z_p_m/find?outputFormat=xml&inputFormat=xml&company_id={{companyId}}`

---

#### warehouse_document_z_p_m/get

**Method:** `GET`

**Path:** `/{{host}}/warehouse_document_z_p_m/get/{{warehouseDocumentId}}?outputFormat=xml&inputFormat=xml&company_id={{companyId}}`

---

#### warehouse_document_z_p_m/edit

**Method:** `POST`

**Path:** `/{{host}}/warehouse_document_z_p_m/edit/{{warehouseDocumentId}}?outputFormat=xml&inputFormat=xml&company_id={{companyId}}`

---

#### warehouse_document_z_p_m/delete

**Method:** `DELETE`

**Path:** `/{{host}}/warehouse_document_z_p_m/delete/{{warehouseDocumentId}}?outputFormat=xml&inputFormat=xml&company_id={{companyId}}`

---

### warehouses

#### warehouses/find

**Method:** `GET`

**Path:** `/{{host}}/warehouses/find?outputFormat=xml&inputFormat=xml&company_id={{companyId}}`

---

#### warehouses/get

**Method:** `GET`

**Path:** `/{{host}}/warehouses/get/ID?outputFormat=xml&inputFormat=xml&company_id={{companyId}}`

---

### webhooks

#### webhooks/add

**Method:** `POST`

**Path:** `/{{host}}/webhooks/add?outputFormat=xml&inputFormat=xml&company_id={{companyId}}`

---

#### webhooks/find

**Method:** `GET`

**Path:** `/{{host}}/webhooks/find?outputFormat=xml&inputFormat=xml&company_id={{companyId}}`

---

#### webhooks/get

**Method:** `GET`

**Path:** `/{{host}}/webhooks/get/{{webhookId}}?outputFormat=xml&inputFormat=xml&company_id={{companyId}}`

---

#### webhooks/trigger

**Method:** `GET`

**Path:** `/{{host}}/webhooks/trigger/{{webhookId}}?outputFormat=xml&inputFormat=xml&company_id={{companyId}}`

---

#### webhooks/edit

**Method:** `PATCH`

**Path:** `/{{host}}/webhooks/edit/{{webhookId}}?outputFormat=xml&inputFormat=xml&company_id={{companyId}}`

---

#### webhooks/delete

**Method:** `DELETE`

**Path:** `/{{host}}/webhooks/delete/{{webhookId}}?outputFormat=xml&inputFormat=xml&company_id={{companyId}}`
