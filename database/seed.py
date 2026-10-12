"""
seed.py
-------

Seeds MongoDB with initial AyurLife data.

Collections:
- users
- remedies
- herbs
- dinacharya
- chat_history

Usage:
python database/seed.py
"""

import json
import os
from pymongo import MongoClient


# -----------------------------
# MongoDB Configuration
# -----------------------------
MONGO_URI = "mongodb://localhost:27017/"
DB_NAME = "ayurlife"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MONGODB_DIR = os.path.join(BASE_DIR, "mongodb")


# -----------------------------
# Utility Functions
# -----------------------------
def load_json(filename):
    """Load JSON file from mongodb folder"""
    path = os.path.join(MONGODB_DIR, filename)
    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


def seed_collection(db, collection_name, data, unique_field=None):
    """
    Seed a MongoDB collection safely.

    Parameters:
    - db: MongoDB database
    - collection_name: name of collection
    - data: list of documents
    - unique_field: field used to prevent duplicates
    """
    collection = db[collection_name]

    inserted = 0
    for doc in data:
        query = {}
        if unique_field and unique_field in doc:
            query = {unique_field: doc[unique_field]}

        if query and collection.find_one(query):
            continue

        collection.insert_one(doc)
        inserted += 1

    print(f"✔ {collection_name}: {inserted} documents inserted")


# -----------------------------
# Main Seeder
# -----------------------------
def main():
    print("🔹 Connecting to MongoDB...")
    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]

    print("🔹 Seeding database...\n")

    seed_collection(
        db,
        "users",
        load_json("users.json"),
        unique_field="email"
    )

    seed_collection(
        db,
        "remedies",
        load_json("remedies.json"),
        unique_field="remedy_id"
    )

    seed_collection(
        db,
        "herbs",
        load_json("herbs.json"),
        unique_field="herb_id"
    )

    seed_collection(
        db,
        "dinacharya",
        load_json("dinacharya.json"),
        unique_field="task_id"
    )

    seed_collection(
        db,
        "chat_history",
        load_json("chat_history.json"),
        unique_field="chat_id"
    )

    print("\n✅ Database seeding completed successfully!")


if __name__ == "__main__":
    main()
