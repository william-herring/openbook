import weasyprint

def export_pdf(repository: str):
    weasyprint.HTML('https://raw.githack.com/' + repository[18:] + '/release/out/html/1.html').write_pdf('./uploads/textbook.pdf', stylesheets=[weasyprint.CSS('./static/src/css/textbook.css')])
    # collect html files
    # add each to a document and append to output
    # save output pdf to server
    # return upload location

if __name__ == '__main__':
    export_pdf('https://github.com/william-herring/example-textbook')