from qdrant_client import QdrantClient
from qdrant_client.http import models
import numpy as np
from faker import Faker

client = QdrantClient(host="localhost", port=6333)

print(client)