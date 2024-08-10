import weasyprint


def export_pdf(repository: str, book_code: str):
    weasyprint.HTML('https://raw.githack.com/' + repository[18:] + '/release/out/html/pdftemplate.html').write_pdf(
        f'./uploads/{book_code}.pdf')
    return f'{book_code}.pdf'
