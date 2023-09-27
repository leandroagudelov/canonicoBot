import re
from chromadb.config import Settings
import chromadb
client = chromadb.EphemeralClient()

document_id = 1


def process_files(documents):
    chroma_client = chromadb.PersistentClient(
        path="local_db" ,
        settings=Settings(anonymized_telemetry=False))
    collection = chroma_client.get_or_create_collection(name="docs_canonico_collection")

    for file in documents:
        print("processing file: " + file.filename)
        try:
            markdown_text = file.read().decode('utf-8')
            chunks = split_text(markdown_text)
            document_title = get_title(markdown_text)
            generate_embeddings(chunks, document_title, file.filename, collection)
        except UnicodeDecodeError:
            print(f"Error: No se pudo decodificar el archivo {file.filename} como UTF-8.")
##    chroma_client.persist()


def generate_embeddings(chunks, document_title, file_name, collection):
    global document_id
    pattern = r'https?://\S+'
    for chunk in chunks:
        match = re.search(pattern, chunk)
        if match:
            url = match.group(0)
           ## print("Pattern found:", url)
        else:
            url = ""
        document_title = get_title(chunk)
        collection.add(
            metadatas={
                "document_title": document_title if document_title is not None else "",
                "file_name": url,
                "URL": url
            },
            documents=chunk,
            ids=[str(document_id)]
        )
        document_id = document_id + 1
##        print("Fin processing file: " + file_name + url + document_title)
##    print("Fin processing file: " + file_name + re.findall(url_pattern, chunk)+ document_title)

def get_title(file):
    match = re.search(r"Entidad:\s+(.+)\s+", file)
    if match:
        title = match.group(1)
        return title
    else:
        " "

def split_text(file):
    separator = "\n### "
    return file.split(separator)


def query_collection(query):
    chroma_client = chromadb.PersistentClient(
        path="local_db" ,
        settings=Settings(anonymized_telemetry=False))
    collection = chroma_client.get_or_create_collection(name="docs_canonico_collection")
    return collection.query(
        query_texts=[query],
        n_results=10,
    )
