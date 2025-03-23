from qdrant_client import QdrantClient
from qdrant_client.http import models
import numpy as np
from faker import Faker

client = QdrantClient(host="localhost", port=6333)

my_collection = "first_collection"

try:
    existing_collection = client.get_collection(collection_name=my_collection)
    print(f"Collection {my_collection} already exists.")
except Exception as e:
    # If collection does not exist, create it
    print(f"Creating collection {my_collection}.")
    client.create_collection(
        collection_name=my_collection,
        vectors_config=models.VectorParams(size=100, distance=models.Distance.COSINE),
    )

data = np.random.uniform(low=-1.0, high=1.0, size=(1000, 100))
index = list(range(1000))

client.upsert(
    collection_name=my_collection,
    points=models.Batch(
        ids=index,
        vectors=data.tolist(),
    )
)

client.retrieve(
    collection_name=my_collection,
    ids=[10, 14, 500],
#     with_vectors=True,
)