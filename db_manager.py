from pymongo import MongoClient
import bcrypt

# DB connection details
DB_NAME = "guessquest"
DB_USER = "admin"
DB_PASSWORD = "admin"
DB_HOST = "mongodb" # Cluster service name
DB_PORT = "27017"


# DB connector
def db_connect():
    mongo_uri = f"mongodb://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/"
    client = MongoClient(mongo_uri)

    return client


# Read all data (for debug)
def read_data(collection_name):
    client = db_connect()
    db = client[DB_NAME]
    collection = db[collection_name]
    documents = collection.find()

    for document in documents:
        print(document)

    client.close()


# Get DB collection as dict
def get_collection(collection_name):
    # return {"hints": ["9290", "9676", "1935", "3688"],
    #         "numberOfPossibleSolutions": 26,
    #         "scores": [{"name": "maya", "timeInSeconds": 30}, {"name": "arty", "timeInSeconds": 90}],
    #         "losers": [{"name": "max", "timeInSeconds": 120}, {"name": "max_again", "timeInSeconds": 800}]}
    client = db_connect()
    db = client[DB_NAME]

    collection = db[collection_name]
    documents = collection.find()
    collection_map = documents[0]
    client.close()

    return collection_map

# Add new user
def add_user(username, email, password):

    try:
        client = db_connect()
        db = client[DB_NAME]
        collection = db.users

        user_document = {
            "username": username,
            "email": email.lower(),
            "password": bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()),
            "streak": 0,
            "solvedRiddles": []
        }

        if collection.find_one({"username": username}):
            return f"Username {username} already exists!"

        elif collection.find_one({"email": email}):
            return f"Email {email} already exists!"

        else:
            collection.insert_one(user_document)
            print("User added successfully")
            return True

    except Exception as err:
        print(f"An error occurred while adding user: {str(err)}")
        return "An error occurred while adding user"

    finally:
        client.close()


# Change user password using email or username
def change_password(identifier, new_password):
    try:
        client = db_connect()
        db = client[DB_NAME]
        collection = db.users

        search_filter = {
            "$or": [
                {"username": {"$regex": f"^{identifier}$", "$options": "i"}},
                {"email": {"$regex": f"^{identifier}$", "$options": "i"}}
            ]
        }

        update = {"$set": {"password": bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())}}
        result = collection.update_one(search_filter, update)

        if result.matched_count > 0:
            print("Password changed successfully!")

    except Exception as err:
        print(f"An error occurred while changing password for user ({identifier}): {str(err)}")

    finally:
        client.close()


# Change user email using email or username
def change_email(username, email):
    try:
        client = db_connect()
        db = client[DB_NAME]
        collection = db.users
        search_filter = {"username": username}
        update = {"$set": {"email": email.lower()}}
        result = collection.update_one(search_filter, update)

        if result.matched_count > 0:
            print("Email changed successfully!")

    except Exception as err:
        print(f"An error occurred while changing email for user ({username}): {str(err)}")

    finally:
        client.close()


# Change user email using email or username
def update_solved_riddle(username, riddle_id, solving_time_seconds):
    try:
        client = db_connect()
        db = client[DB_NAME]
        collection = db.users
        search_filter = {"username": {"$regex": f"^{username}$", "$options": "i"}}
        update = {'$push': {'solvedRiddles': {"id": riddle_id, "solvingTimeSeconds": solving_time_seconds}}}
        result = collection.update_one(search_filter, update)

        if result.matched_count > 0:
            print("Solved riddle added successfully!")

    except Exception as err:
        print(f"An error occurred while adding solved riddle for user ({username}): {str(err)}")

    finally:
        client.close()


# Check user exists and that the password is correct
def validate_user(identifier, password):
    try:
        client = db_connect()
        db = client[DB_NAME]
        collection = db.users
        identifier_lower = identifier.lower()

        user = collection.find_one({
            "$or": [
                {"email": {"$regex": f"^{identifier_lower}$", "$options": "i"}},
                {"username": {"$regex": f"^{identifier_lower}$", "$options": "i"}}
            ]
        })

        if user:
            if isinstance(user["password"], str):
                stored_password = user["password"].encode('utf-8')
            else:
                stored_password = user["password"]

            if bcrypt.checkpw(password.encode('utf-8'), stored_password):
                return True
            else:
                return "Password is incorrect!"

        else:
            return f"User {identifier} doesn't exist!"

    except Exception as err:
        print(f"An error occurred while authenticating user ({identifier}): {str(err)}")
        return f"Failed to check user {identifier}"

    finally:
        client.close()