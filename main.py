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

fake_something = Faker()
payload = []

for i in range(1000):
    payload.append(
        {
            "id": i,
            "artist": fake_something.name(),
            "song": " ".join(fake_something.words()),
            "url_song": fake_something.url(),
            "country": fake_something.country(),
        }
    )

client.upsert(
    collection_name=my_collection,
    points=models.Batch(
        ids=index,
        vectors=data.tolist(),
        payloads=payload
    )
)

# Semantic search

living_la_vida_loca = np.random.uniform(low=-1.0, high=1.0, size=(100)).tolist()

result = client.search(
    collection_name=my_collection,
    query_vector=living_la_vida_loca,
    limit=10,
)

aussie_songs = models.Filter(
    must=[
        models.FieldCondition(
            key="country",
            match=models.MatchValue(value="Australia")
        )
    ]
)

result = client.search(
    collection_name=my_collection,
    query_vector=living_la_vida_loca,
    query_filter=aussie_songs,
    limit=3,
)


print(result)