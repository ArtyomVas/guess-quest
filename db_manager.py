from pymongo import MongoClient
import bcrypt
from datetime import datetime

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
            "riddles": []
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


def get_user_dict(identifier):

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

        user_document = collection.find_one(search_filter)

        if user_document:
            return user_document
        else:
            return "Found no such user"

    except Exception as err:
        print(f"An error occurred while getting user data: {str(err)}")
        return "An error occurred while getting user data"

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

        return True

    except Exception as err:
        print(f"An error occurred while changing password for user ({identifier}): {str(err)}")
        return f"An error occurred while changing password for user ({identifier})"

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

        return True

    except Exception as err:
        print(f"An error occurred while changing email for user ({username}): {str(err)}")
        return f"An error occurred while changing email for user ({username})"

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


def update_user_start_riddle(user_id, riddle_id):
    try:
        current_time = datetime.now()
        client = db_connect()
        db = client[DB_NAME]
        collection = db.users
        search_filter = {"username": user_id, "riddles.riddleId": riddle_id}

        existing_riddle = collection.find_one(search_filter)

        if existing_riddle:
            print("User already has this riddle in progress")
            return False

        started_riddle_dict = {
            "riddleId": riddle_id,
            "startedIn": current_time,
            "status": "in_progress",
            "finishedAt": None,
            "totalWorkTimeSeconds": None
        }

        search_filter = {"username": user_id}
        update = {"$push": {"riddles": started_riddle_dict}}
        result = collection.update_one(search_filter, update)

        if result.matched_count > 0:
            print("Riddle added to user's riddles in progress")
            return True

    except Exception as err:
        print(f"An error occurred while adding riddle to user's riddles in progress: {str(err)}")
        return False

    finally:
        client.close()


def update_user_solved_riddle(user_id, riddle_id):
    try:
        current_time = datetime.now()
        client = db_connect()
        db = client[DB_NAME]
        collection = db.users
        user_dict = collection.find_one({"username": user_id, "riddles.riddleId": riddle_id}, {"riddles.$": 1})
        starting_time = user_dict['riddles'][0].get('startedIn')
        total_work_time_seconds = (current_time - starting_time).total_seconds()

        search_filter = {"username": user_id}
        update_fields = {
            'status': 'solved',
            'finishedAt': current_time,
            'totalWorkTimeSeconds': total_work_time_seconds
        }

        update_document = {f"riddles.$[riddle].{k}": v for k, v in update_fields.items()}

        result = collection.update_one(
            search_filter,
            {"$set": update_document},
            array_filters=[{"riddle.riddleId": riddle_id}]
        )

        if result.matched_count > 0:
            print("Riddle was updated as solved for user!")

        collection = db.riddleOfTheDay

        user_solved_entry = {
            "name": user_id,
            "timeInSeconds": total_work_time_seconds
        }

        update = {"$push": {"scores": user_solved_entry}}
        result = collection.update_one({}, update)

        if result.matched_count > 0:
            print("User solving time was added to the riddle scores")

        return True

    except Exception as err:
        print(f"An error occurred while solving riddle: {str(err)}")

    finally:
        client.close()


def update_user_gaveup_riddle(user_id, riddle_id):
    try:
        print("MDEBUG: start update_user_gaveup_riddle")
        print(f"MDEBUG: (update_user_gaveup_riddle) user_id - {user_id}")
        print(f"MDEBUG: (update_user_gaveup_riddle) riddle_id - {riddle_id}")

        current_time = datetime.now()
        client = db_connect()
        db = client[DB_NAME]
        collection = db.users
        user_dict = collection.find_one({"username": user_id, "riddles.riddleId": riddle_id}, {"riddles.$": 1})
        print(f"MDEBUG: (update_user_gaveup_riddle) user_dict - {user_dict}")
        starting_time = user_dict['riddles'][0].get('startedIn')
        print(f"MDEBUG: (update_user_gaveup_riddle) starting_time - {starting_time}")
        total_work_time_seconds = (current_time - starting_time).total_seconds()
        print(f"MDEBUG: (update_user_gaveup_riddle) total_work_time_seconds - {total_work_time_seconds}")

        search_filter = {"username": user_id}
        print(f"MDEBUG: (update_user_gaveup_riddle) search_filter - {search_filter}")

        update_fields = {
            'status': 'gaveup',
            'finishedAt': current_time,
            'totalWorkTimeSeconds': total_work_time_seconds
        }
        print(f"MDEBUG: (update_user_gaveup_riddle) update_fields - {update_fields}")

        update_document = {f"riddles.$[riddle].{k}": v for k, v in update_fields.items()}

        result = collection.update_one(
            search_filter,
            {"$set": update_document},
            array_filters=[{"riddle.riddleId": riddle_id}]
        )
        print(f"MDEBUG: (update_user_gaveup_riddle) after update gavup")

        if result.matched_count > 0:
            print("Riddle was updated as a gaveup for user")

        collection = db.riddleOfTheDay

        user_gaveup_entry = {
            "name": user_id,
            "timeInSeconds": total_work_time_seconds
        }

        update = {"$push": {"losers": user_gaveup_entry}}
        result = collection.update_one({}, update)

        if result.matched_count > 0:
            print("User losing time was added to the riddle losers scores")

        return True

    except Exception as err:
        print(f"An error occurred while updating gaveup riddle: {str(err)}")

    finally:
        client.close()