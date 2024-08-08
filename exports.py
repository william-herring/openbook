import aspose.words as aw

def export_pdf(repository: str):
    output = aw.Document()
    output.remove_all_children()

    # collect html files
    # add each to a document and append to output
    # save output pdf to server
    # return upload location