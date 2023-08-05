import os
import json
from sentence_transformers import SentenceTransformer
import pinecone
import tqdm

api_key = os.getenv("PINECONE_API_KEY")
environment = os.getenv("PINECONE_ENV")

pinecone.init(
	api_key=api_key,
	environment=environment
)
index = pinecone.Index('documents-vector')

transformer = SentenceTransformer("all-MiniLM-L6-v2")

def create_pinecone_db(objects):
  c = 0
  l = []
  m = 0
  for id in tqdm(objects,"Transformed_docs",len(objects)):
    c +=1
    emb = transformer.encode(objects[id]["text"]).tolist()
    l.append((id,emb))
    objects[id]["embedding"] = emb
    if c%100 == 0:
      m += 1
      index.upsert(
            vectors=l[100*(m-1):100*(m)],
            namespace="documents-vect")

if __name__ == "__main__":

  with open("data/clean_data.json","r") as f:
    data = json.load(f)
    
  create_pinecone_db(data)