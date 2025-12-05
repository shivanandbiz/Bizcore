frappe.ui.form.on('Job Offer', {
    refresh: function(frm) {
        set_print_format(frm);
        customize_print_button(frm);
    },

    onload: function(frm) {
        set_print_format(frm);
    },

    custom_employment_type_: function(frm) {
        set_print_format(frm);
    },

    after_save: function(frm) {
        set_print_format(frm);
    }
});

function set_print_format(frm) {
    if (frm.doc.custom_employment_type_) {
        const print_format_map = {
            'FULL TIME EMPLOYEMENT-OFFER LETTER': 'Job Offer',
            'INTERNSHIP - OFFER LETTER': 'INTERNSHIP',
            'FREELANCE CONTRACT-JOB OFFER': 'FREELANCE CONTRACT-JOB OFFER'
        };

        let print_format = print_format_map[frm.doc.custom_employment_type_];

        if (print_format) {
            frm.meta.default_print_format = print_format;

            setTimeout(() => {
                if (frm.page && frm.page.print_sel) {
                    frm.page.print_sel.val(print_format);
                }
            }, 100);
        }
    }
}

function customize_print_button(frm) {
    setTimeout(() => {
        const print_btn = frm.page.btn_primary;

        if (print_btn && print_btn.text().includes('Print')) {
            print_btn.off('click');

            print_btn.on('click', function(e) {
                e.stopImmediatePropagation();

                const print_format_map = {
                    'FULL TIME EMPLOYEMENT-OFFER LETTER': 'FULL TIME EMPLOYEMENT-OFFER LETTER',
                    'INTERNSHIP - OFFER LETTER': 'INTERNSHIP - OFFER LETTER',
                    'FREELANCE CONTRACT-JOB OFFER': 'FREELANCE CONTRACT-JOB OFFER'
                };

                let print_format = print_format_map[frm.doc.custom_employment_type_];

                if (print_format) {
                    const print_url = frappe.urllib.get_full_url(
                        '/printview?doctype=' + encodeURIComponent(frm.doctype)
                        + '&name=' + encodeURIComponent(frm.doc.name)
                        + '&format=' + encodeURIComponent(print_format)
                    );

                    window.open(print_url);
                    return false;
                }

                frm.print_doc();
            });
        }
    }, 500);
}