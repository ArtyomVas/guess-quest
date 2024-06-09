# color_list = ["red","green","white","black"]
# length = len(color_list)
# print(color_list[length-length])
# print(color_list[length-1])



# num1 = int(input("input the first number"))
# num2 = int(input("input the second number"))
# num3 = int(input("input the third number"))
# if num1 == num2 and num2 == num3:
#    print((num1+num2+num3) * 3)
# else:
#    print(num1 + num2 + num3)



#def list_concatenate(List):
#    con_word = ""
#     for i in List:
#         con_word = con_word + str(i)
#
#     return con_word
#
# x = ["I", 2, "myself"]
# print (list_concatenate(x))



# def cut_lists(list1,list2):
#     final_list = list1
#     for i in list1:
#         for j in list2:
#             if i == j:
#                 final_list.remove(i)
#     return final_list
#
# color_list_1 = ["White", "Black", "Red"]
# color_list_2 = ["Red", "Green"]
# print(cut_lists(color_list_1,color_list_2))



# def swap(x,y):
#     x, y = y, x
#     return x, y
# print(swap(1, "maya"))



import random

def rand_word():
    words = ["miracle", "leftover", "driver", "cousin", "chimpanzee", "geography", "culture", "construction"]
    random_word = random.choice(words)
    return random_word


def check_letter(letter):
    if letter.isalpha() and letter not in listed_letters and len(letter) == 1:
        return True
    elif letter.isalpha() and letter not in listed_letters:
        error = "You need to pick only one letter"
        return error
    elif letter.isalpha() and len(letter) == 1:
        error = "You already picked this letter"
        return error
    elif letter not in listed_letters and len(letter) == 1:
        error = "You need to pick a letter"
        return error


current_word = rand_word()
num_of_guesses = 10
current_letter = input("Type in a letter").lower()

while num_of_guesses != 0:
    if check_letter(current_letter):
        if





