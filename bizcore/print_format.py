import frappe

PRINT_FORMAT_MAP = {
    'FULL TIME EMPLOYEMENT-OFFER LETTER': 'Job Offer',
    'INTERNSHIP - OFFER LETTER': 'INTERNSHIP',
    'FREELANCE CONTRACT-JOB OFFER': 'FREELANCE CONTRACT-JOB OFFER'
}

@frappe.whitelist()
def set_print_format(doc, method=None):
    if doc.custom_employment_type_:
        print_format = PRINT_FORMAT_MAP.get(doc.custom_employment_type_)

        if print_format and frappe.db.exists('Print Format', print_format):

            frappe.db.sql("""
                DELETE FROM `tabProperty Setter`
                WHERE doc_type = 'Job Offer'
                AND property = 'default_print_format'
            """)

            frappe.get_doc({
                'doctype': 'Property Setter',
                'doctype_or_field': 'DocType',
                'doc_type': 'Job Offer',
                'property': 'default_print_format',
                'property_type': 'Data',
                'value': print_format
            }).insert(ignore_permissions=True)

            frappe.db.commit()

            frappe.clear_cache(doctype='Job Offer')
            frappe.clear_document_cache('Job Offer', doc.name)
