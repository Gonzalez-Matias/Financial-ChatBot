import os
import json
import ijson
import re
import wordninja
import multiprocessing as mp
from tqdm import *

doc_id = 0
json_doc = open("data/clean_data.json", 'a')

def listener(q):
    """
    continue to listen for messages on the queue and writes to file when receive one
    if it receives a '#done#' message it will exit
    """
    global doc_id
    while True:
        m = q.get()
        if m == '#done#':
            break
        tx = "ID_"+str(doc_id)
        m["id"] = "ID_"+str(doc_id)
        if doc_id == 0:
            json_doc.write('{\n')
            json_doc.write('"'+tx+'":\n')
            doc_id += 1
            json.dump(m, json_doc, indent=3)
        else:
            doc_id += 1
            json_doc.write(',\n')
            json_doc.write('"'+tx+'":\n')
            json.dump(m, json_doc, indent=3)
    
def clean_document(document_stacks, q):
    for text_dict in document_stacks:
        text = text_dict["text"].lower()
        text = re.sub(r"(@\[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)|^rt|http.+?", "", text)
        text = " ".join(text.split())
        if len(text) >= 500 and text.count(" ") > 5:
            text = " ".join(wordninja.split(text))
            clean_text_dict = dict()
            clean_text_dict["text"] = text
            clean_text_dict["metadata"] = text_dict["metadata"]
            q.put(clean_text_dict)

def cleaning_pipeline(doc, q):
        with open(doc, "r") as f:
            objects = ijson.items(f,"documents.item")
            document_stacks = [o for o in objects]
            clean_document(document_stacks, q)


if __name__ == "__main__":

    dir = "data/documents_stacks/"

    docs = [dir+d for d in os.listdir(dir)]

    manager = mp.Manager()
    q = manager.Queue()
    file_pool = mp.Pool(1)
    file_pool.apply_async(listener, (q, ))

    pool = mp.Pool(3)
    jobs = []
    for doc in docs:
        job = pool.apply_async(cleaning_pipeline, (doc, q))
        jobs.append(job)

    for job in tqdm(jobs, "Documents"):
        job.get()

    q.put('#done#')  # all workers are done, we close the output file
    pool.close()
    pool.join()
    
    json_doc.seek(0, os.SEEK_END)              
    json_doc.seek(json_doc.tell() - 28, os.SEEK_SET)
    json_doc.truncate()
    json_doc.write('\n}')
    json_doc.close()
