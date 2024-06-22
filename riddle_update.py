from riddle_generator import *
from db_manager import *

hint1, hint2, hint3, hint4 = create_riddle()
print(f"created hints: {hint1} {hint2} {hint3} {hint4}")
new_hints = [hint1, hint2, hint3, hint4]
print(f"new_hints: {new_hints}")
new_number_of_possible_solutions = get_number_of_riddle_solutions(hint1, hint2, hint3, hint4)
print(f"new_number_of_possible_solutions: {new_number_of_possible_solutions}")

print(f"DB_NAME - {DB_NAME}")

client = db_connect()
print("created client")
db = client[DB_NAME]
print("created db")
collection = db.riddleOfTheDay
print("pulled collection riddleOfTheDay")
delete_result = collection.delete_many({})

new_riddle = {
    'hints': new_hints,
    'numberOfPossibleSolutions': new_number_of_possible_solutions,
    'scores': [],
    'losers': []
}

insert_result = collection.insert_one(new_riddle)

if insert_result.inserted_id:
    print("Riddle updated successfully")
else:
    print("The riddle wasn't updated")

client.close()
