from pymongo import MongoClient
from pymongo.common import UuidRepresentation
from bson.binary import Binary, UUID_SUBTYPE
from bson.codec_options import (
    CodecOptions,
    TypeRegistry,
    TypeEncoder,
    TypeDecoder,
)

import os
import uuid

DATABASE_URL = os.environ.get("DATABASE_URL")
DB_NAME = os.environ.get("DB_NAME")


class BinaryUUIDDecoder(TypeDecoder):
    bson_type = Binary  # The BSON type we're decoding

    def transform_bson(self, value):
        return uuid.UUID(bytes=value)


class StringUUIDDecoder(TypeDecoder):
    bson_type = str  # The BSON type we're decoding

    def transform_bson(self, value):
        try:
            # Try converting the string to a UUID
            return uuid.UUID(value)
        except ValueError:
            # If it's not a valid UUID, return the string as-is
            return value


class SetEncoder(TypeEncoder):
    python_type = set  # Python type to encode

    def transform_python(self, value):
        return list(value)  # Convert set to list before saving to MongoDB


# Create a TypeRegistry with our encoders and decoders
type_registry = TypeRegistry(
    [SetEncoder(), BinaryUUIDDecoder(), StringUUIDDecoder()]
)

# Create a CodecOptions with the type registry
codec_options = CodecOptions(
    type_registry=type_registry,
    uuid_representation=UuidRepresentation.STANDARD,
)

# uuidRepresentation allows for work directly with uuid.UUID objects without additional conversion

client = MongoClient(DATABASE_URL)
# db = client[DB_NAME]
db = client.get_database(DB_NAME, codec_options=codec_options)
