# List: your backpack 🎒

# A list is like a backpack. You can put things in, take things out, and change what's inside.
backpack = ["pencil", "notebook", "apple", "eraser"]

print(backpack[0])          # pencil  (Python starts counting at 0!)

backpack.append("crayons")  # put something new in
backpack.remove("apple")    # you ate the apple
backpack[1] = "comic book"  # swap the notebook for a comic book

print(backpack)

# ['pencil', 'comic book', 'eraser', 'crayons']


# Tuple: your birthday 🎂
# A tuple is for things that should never change, like the day you were born.
birthday = (2016, "March", 14)   # year, month, day
print(birthday[1])   # March



# Dictionary: a Pokédex or phone book 📖

# A dictionary pairs a name (the key) with information about it (the value). It works the way you look up a word in a real dictionary to find its meaning.
pet = {
    "name": "Buddy",
    "animal": "dog",
    "age": 3,
    "favorite_toy": "ball"
}

print(pet["name"])        # Buddy

pet["age"] = 4            # Buddy had a birthday
pet["color"] = "brown"    # add new info

print(pet)
# {'name': 'Buddy', 'animal': 'dog', 'age': 4, 'favorite_toy': 'ball', 'color': 'brown'}