import random

maze: list[str] = [
    "|--|--|--|  |--|--|",
    "|     |        |  |",
    "|  |--|  |  |  |  |",
    "|  |     |  |     |",
    "|  |  |  |--|--|--|",
    "|  |  |           |",
    "|  |  |--|--|--|  |",
    "|  |        |  |  |",
    "|  |--|--|  |  |  |",
    "|     |     |  |  |",
    "|--|  |  |--|  |  |",
    "|        |        |",
    "|--|--|--|--|--|--|",
]
legend = ["player: @@", "loot: ##", "danger: !!"]

# for i in maze:
#     print(i)
# print()

# generating loot an enemies in the corners
loot_pos = []
for row in range(1, len(maze) - 1):
    for col in range(1, len(maze[row]) - 1, 3):
        if maze[row][col] == " ":
            if sum([maze[row][col - 1] != " ",
                    maze[row][col + 2] != " ",
                    maze[row + 1][col] != " ",
                    maze[row - 1][col] != " "]) >= 3:
                loot_pos.append([row, col])

for row, col in loot_pos:
    # 1 for loot and 2 for danger
    loot_type = random.choice([1, 2])
    match loot_type:
        case 1:
            maze[row] = maze[row][:col] + "##" + maze[row][col + 2:]
        case 2:
            maze[row] = maze[row][:col] + "!!" + maze[row][col + 2:]

# initial coordinates:
pos = [11, 1]
new_pos = []
goal = [0, 10]

# player stats:
health = 50
score = 40
win = False

# putting the player in place
maze[pos[0]] = maze[pos[0]][:pos[1]] + "@@" + maze[pos[0]][pos[1] + 2:]

# intro messages
print("You are trapped in a maze.",
      "Be aware of the dangers!",
      "Try to escape from this maze!",
      "You can find treasures and defeat monsters to get some loot!"
      "You have a limited time!", sep="\n")
print()

# printing the legend:
print("Map markers info:")
for i in legend:
    print(i)

# printing the maze:
for i in maze:
    print(i)

# player should reach exit the maze before 40 tries:
for step in range(45):
    # showing the player stats:
    print("Health: {}, Time: {}".format(health, 35 - step))

    direction = ""
    directions = ["up", "down", "left", "right"]
    while True:
        bad_input = False
        direction = input("choose a direction (up, down, left, right): ")
        match direction:
            case "up":
                if maze[pos[0] - 1][pos[1]] != "-":
                    print("going up")
                    new_pos = [pos[0] - 1, pos[1]]
                else:
                    print("that way is blocked")
                    bad_input = True
            case "down":
                if maze[pos[0] + 1][pos[1]] != "-":
                    print("going down")
                    new_pos = [pos[0] + 1, pos[1]]
                else:
                    print("that way is blocked")
                    bad_input = True
            case "right":
                if maze[pos[0]][pos[1] + 2] != "|":
                    print("going right")
                    new_pos = [pos[0], pos[1] + 3]
                else:
                    print("that way is blocked")
                    bad_input = True
            case "left":
                if maze[pos[0]][pos[1] - 1] != "|":
                    print("going left")
                    new_pos = [pos[0], pos[1] - 3]
                else:
                    print("that way is blocked")
                    bad_input = True
            case _:
                print("Enter a correct direction!")
                bad_input = True
        if not bad_input:
            break

    # each step player will lose one point
    score -= 1
    health = min(health + 4, 100)

    # checking for events:
    match maze[pos[0]][pos[1]]:
        case "#":
            print("You found treasure and healed!")
            health = min(health + 20, 100)
            score += 10
        case "!" if health > 50:
            print("You defeated the monster and found treasures, but you gut injured!")
            health -= 50
            score += 16
        case "!":
            print("GAME OVER!!")
            print("You have been defeated by the enemy!")
            break
    # removing the player from previous position:
    maze[pos[0]] = maze[pos[0]][:pos[1]] + "  " + maze[pos[0]][pos[1] + 2:]

    # putting the player in the new pos
    pos = new_pos[:]
    maze[pos[0]] = maze[pos[0]][:pos[1]] + "@@" + maze[pos[0]][pos[1] + 2:]

    if pos == goal:
        win = True
        break

    # printing the maze:
    print()
    for i in maze:
        print(i)
else:
    print("GAME OVER!!")
    print("you did not escape from the maze in time, and monsters got you!")

if win:
    print("Congratulation. You escaped from the maze!")
    print("final score: {}".format(score))
