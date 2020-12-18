import csv
import io
import os
import sys

import PyPDF2
from reportlab.pdfgen import canvas
from reportlab.lib import pagesizes


def write_cheat_sheet(base_template, name, username, password, output_dir):
    bytez = io.BytesIO()
    url = 'https://workshop-server.qiime2.org/%s' % username
    base_fn = name.replace(' ', '-').replace('.', '')
    base_fn = base_fn.replace('--', '-').lower()
    out_fn = os.path.join(output_dir, '%s-%s.pdf' % (base_fn, username))

    c = canvas.Canvas(bytez, pagesize=pagesizes.A4)
    c.setFillColorRGB(1, 1, 1)

    # You will need to update these, if the layout changes
    row_1_y, row_2_y = 518, 490
    col_1_x, col_2_x = 23, 370

    # Write out the dynamic content
    c.drawString(col_1_x, row_1_y, name)
    c.drawString(col_1_x, row_2_y, url)
    c.drawString(col_2_x, row_1_y, username)
    c.drawString(col_2_x, row_2_y, password)

    c.save()

    bytez.seek(0)
    overlay = PyPDF2.PdfFileReader(bytez)

    with open(base_template, 'rb') as fh_in, open(out_fn, 'wb') as fh_out:
        template = PyPDF2.PdfFileReader(fh_in)
        output_pdf = PyPDF2.PdfFileWriter()
        page = template.getPage(0)
        page.mergePage(overlay.getPage(0))
        output_pdf.addPage(page)
        output_pdf.write(fh_out)


def write_cert(base_template, name, output_dir):
    bytez = io.BytesIO()
    base_fn = name.replace(' ', '-').replace('.', '')
    base_fn = base_fn.replace('--', '-').lower()
    out_fn = os.path.join(output_dir, '%s.pdf' % base_fn)

    c = canvas.Canvas(bytez, pagesize=pagesizes.A4)
    c.setFont('Helvetica', 36)

    # Write out the dynamic content
    c.drawCentredString(425, 415, name)

    c.save()

    bytez.seek(0)
    overlay = PyPDF2.PdfFileReader(bytez)

    with open(base_template, 'rb') as fh_in, open(out_fn, 'wb') as fh_out:
        template = PyPDF2.PdfFileReader(fh_in)
        output_pdf = PyPDF2.PdfFileWriter()
        page = template.getPage(0)
        page.mergePage(overlay.getPage(0))
        output_pdf.addPage(page)
        output_pdf.write(fh_out)


if __name__ == '__main__':
    base_pdf = sys.argv[1]
    base_cert = sys.argv[2]
    roster = sys.argv[3]
    output_pdf_dir = sys.argv[4]
    output_cert_dir = sys.argv[5]
    os.mkdir(output_pdf_dir)
    os.mkdir(output_cert_dir)
    # Name, Email, Cohort, Username, Password, + extra columns
    with open(roster) as fh:
        reader = csv.reader(fh, delimiter=',')
        next(reader)  # skip first row
        for row in reader:
            name, username, password = row[0], row[3], row[4]
            print('writing `%s` `%s` `%s`' % (name, username, password))
            write_cheat_sheet(base_pdf, name, username, password,
                              output_pdf_dir)
            write_cert(base_cert, name, output_cert_dir)
