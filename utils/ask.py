import os
from sentence_transformers import SentenceTransformer
import ijson
import pinecone      

api_key = os.getenv("PINECONE_API_KEY")
environment = os.getenv("PINECONE_ENV")

transformer = SentenceTransformer("all-MiniLM-L6-v2")

pinecone.init(      
	api_key=api_key,      
	environment=environment      
)      
index = pinecone.Index('documents-vector')

def get_id(query):
    """
    Search for the most similar vector in a vector database based on a given query.

    Parameters:
        query (str): The query string to be converted into a vector representation and compared with the vectors in the database.

    Returns:
        str: The ID of the most similar vector in the database.

    Description:
        This function takes a query string and searches for the most similar vector in a pre-existing vector database.
        The database is accessed through the 'index' object.
        The 'st' object represents a vector encoder used to convert the query string into a vector representation.

        The function performs the following steps:
        1. Encodes the query string into a vector using 'st.encode()' and converts it into a Python list.
        2. Submits the encoded query to the 'index.query()' method to search for the most similar vector in the database.
           The 'vector' parameter is set to the encoded query, 'top_k' is set to 1 (return only the closest match),
           and 'namespace' is specified as "documents-vect" to ensure the search is performed in the correct namespace.

        The function returns the ID of the most similar vector found in the database, which is extracted from the 'res'
        dictionary returned by the 'index.query()' method.
    """
    
    # Encode the query string using 'st.encode()' and convert it to a list
    embd = transformer.encode(query).tolist()

    # Search for the most similar vector in the database
    res = index.query(
                vector=embd,
                top_k=1,
                namespace="documents-vect"
                )

    # Extract and return the ID of the most similar vector
    return res["matches"][0]["id"]

def get_document(id):
    """
    Retrieve a document from a JSON file based on its ID.

    Parameters:
        id (str): The unique ID of the document to be retrieved from the JSON file.

    Returns:
        dict: The document represented as a Python dictionary.

    Description:
        This function searches for a specific document in a JSON file containing multiple documents,
        each identified by a unique ID. The function reads the JSON file and extracts the document with the given ID.

        The function performs the following steps:
        1. Opens the JSON file.
        2. Uses the 'ijson' library to efficiently parse the JSON file in a streaming fashion.
           The 'ijson' library allows reading JSON data incrementally, which is memory-efficient for large JSON files.
           It reads the JSON file in chunks and searches for the specified 'id'.
        3. When the desired 'id' is found, the corresponding 'objects' (document) are extracted.
           'objects' is a Python dictionary representing the document.
        4. The function returns the retrieved document.
    """
    # Open the JSON file in read mode and use 'ijson' to efficiently parse it
    with open("data/clean_data.json", "r") as doc:
        # Use 'ijson.items()' to read the JSON file in chunks and search for the specified 'id'
        objects = next(ijson.items(doc, id))
        # Return the retrieved document represented as a Python dictionary
        return objects
    
def get_context(query):
    """
    Retrieve the context for a given query from a JSON file.

    Parameters:
        query (str): The query string used to search for the context in the JSON file.

    Returns:
        str or None: The context text corresponding to the given query if found, or None if the query does not match any document.

    Description:
        This function retrieves the context for a given query from a JSON file containing multiple documents.
        It first searches for the most similar document ID using the 'get_id' function based on the query.
        Then, it retrieves the document using the 'get_document' function based on the obtained ID.
        Finally, it extracts and returns the 'text' field from the retrieved document.

        The function performs the following steps:
        1. Calls the 'get_id' function with the 'query' parameter to obtain the most similar document ID.
        2. Calls the 'get_document' function with the obtained ID to retrieve the corresponding document.
        3. Extracts the 'text' field from the retrieved document and returns it.

        If the query does not match any document, the function returns None.
    """
    # Obtain the most similar document ID based on the query
    id = get_id(query)

    # Retrieve the document using the obtained ID
    doc = get_document(id)

    # If the document is found, extract and return the 'text' field from the document
    if doc:
        return doc["text"]
    else:
        # If the document is not found, return None
        return None