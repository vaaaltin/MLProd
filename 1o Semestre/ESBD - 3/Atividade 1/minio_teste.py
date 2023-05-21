# pip install minio
import pickle
from minio import Minio

client = Minio(
    "localhost:9000",
    access_key="minio",
    secret_key="minio123",
    secure=False
)

# Upload:
my_object = {
    "name": "Alice",
    "age": 30,
    "interests": ["reading", "hiking", "traveling"]
}

# Pickle the object
pickled_object = pickle.dumps(my_object)

# Upload the pickled object to Minio
client.put_object(
    bucket_name="mybucket",
    object_name="myobject.pkl",
    data=pickled_object,
    length=len(pickled_object),
    content_type="application/octet-stream"
)

# Download:
data = client.get_object(
    bucket_name="mybucket",
    object_name="myobject.pkl"
)
# Read the pickled data from the response
pickled_object = data.read()
# Unpickle the object
my_object = pickle.loads(pickled_object)