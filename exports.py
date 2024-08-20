import weasyprint

def export_pdf(repository: str, book_code: str):
    """
    The PDF export function uses the Weasyprint library to convert a single HTML file created by the textbook engine
    to a PDF file with styles. It is then added to the uploads folder as [book_code].pdf
    """
    weasyprint.HTML('https://raw.githack.com/' + repository[18:] + '/release/out/html/pdftemplate.html').write_pdf(
        f'./uploads/{book_code}.pdf')
    return f'{book_code}.pdf'
