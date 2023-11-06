import bibtexparser
from bibtexparser.bparser import BibTexParser
from txtai import Embeddings
import gc


def parse_bibtex(bib_file):
    with open(bib_file, encoding='utf8') as bibtex_file:
        bib_database = bibtexparser.load(bibtex_file)

    abstracts = {}
    for entry in bib_database.entries:
        # print(entry)
        # Assuming each entry has an 'ID' and 'abstract' field.
        abstracts[entry['ID']] = entry.get('abstract', '')
        # abstracts[entry['year']] = entry.get('year', '')
        # abstracts[entry['title']] = entry.get('title', '')

    return abstracts





# Load collection
# bib_file = 'FDXstuff.bib'
bib_file = 'Dissertation.bib'

personal_abstracts = parse_bibtex(bib_file)

# Load the PubMedBERT Embeddings model with a smaller batch size
embeddings = Embeddings(path="neuml/pubmedbert-base-embeddings", content=True, batchsize=8)

# Index personal collection abstracts
indexed_abstracts = [(str(pmid), text) for pmid, text in personal_abstracts.items()]
embeddings.index(indexed_abstracts)

# URI, esto es for optimization purposes, yo intentaria sin esto primero y si no te corre anadelo de vuelta
del indexed_abstracts
gc.collect()
# fin de optimization code

# Helper function to parse the BibTeX entry and return the required details
def extract_details_from_bibtex(bibtex_entry):
    parser = BibTexParser(common_strings=True)
    bib_database = bibtexparser.loads(bibtex_entry, parser=parser)

    if not bib_database.entries:
        return '', '', ''  # Return empty strings if there's no entry

    entry = bib_database.entries[0]
    author = entry.get('author', '')
    title = entry.get('title', '')
    year = entry.get('year', '')
    return author, title, year


def extract_bib_details(bib_path, excerpt, topn=5):
    results = embeddings.search(excerpt, limit=topn)

    # Parse the .bib file
    with open(bib_path, 'r') as bibfile:
        bib_database = bibtexparser.load(bibfile)

    extracted_details = []

    # Iterate over search_references and get matching entries from .bib file
    for entry in results:
        bib_id = entry['id']
        for bib_entry in bib_database.entries:
            if bib_entry['ID'] == bib_id:
                detail = {
                    "Title": bib_entry.get('title', 'N/A'),
                    "Author": bib_entry.get('author', 'N/A'),
                    "Date": bib_entry.get('year', 'N/A')
                }
                extracted_details.append(detail)
                break

    return extracted_details


excerpt = "Copper inhibits FDX1-mediated protein lipoylation"

references = extract_bib_details(bib_file, excerpt)

for citation in references:
    print(f"Citation: {citation}")
