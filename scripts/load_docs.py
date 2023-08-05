from haystack.nodes import PreProcessor, PDFToTextConverter
from joblib import Parallel, delayed
import os
import json
from tqdm import tqdm

os.environ["TOKENIZERS_PARALLELISM"] = "true"

converter = PDFToTextConverter(remove_numeric_tables=True,multiprocessing=False)

preprocessor = PreProcessor(
        clean_empty_lines=True,
        clean_whitespace=True,
        clean_header_footer=True,
        split_by="word",
        split_overlap=0,
        split_length=1500,
        progress_bar=False,
        split_respect_sentence_boundary=True,
        max_chars_check=1750)

def load_file(directory : str):

    doc_pdf = converter.convert(file_path=directory)[0]

    return doc_pdf

def preproccess_document(document):

    doc_stacks = preprocessor.process([document])

    return doc_stacks

def data_pipeline(directory):

    try:
        doc = converter.convert(file_path=str(directory))[0]

        doc_stacks = preprocessor.process([doc])

        processed_data = {"documents":[]}

        for index, d_stack in enumerate(doc_stacks):
            dict_doc = {
                        "text" : d_stack.content,
                        "metadata" : {'doc_name':directory.split("-")[-1]},
                        "id" : str(index+1)}
            processed_data["documents"].append(dict_doc)

        json_name = "data/documents_stacks/"+directory.replace(".pdf",".json").split("-")[-1]
        with open(json_name, "w") as file:
            json.dump(processed_data, file, indent=6)
    
    except:
        return


if __name__ == "__main__":


    dir = "data/pdf_documents/"

    docs = [dir+d for d in os.listdir(dir)]

    workers = 2

    Parallel(n_jobs=workers)(delayed(data_pipeline)(path) for path in tqdm(docs))

