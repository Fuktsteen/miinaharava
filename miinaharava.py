import sweeperlib
import random
import time
import datetime

state = {
    "field": [],
    "shown": [],
    "stats": [],
    "aika": [0, 0],
    "kello": 0,
    "pommit": 0,
    "merkatut": 0
}

def count_ninjas(x, y, lista):
    """
    Counts the ninjas surrounding one tile in the given room and
    returns the result. The function assumes the selected tile does
    not have a ninja in it - if it does, it counts that one as well.
    """
    if lista[y][x] == "x":
        return "x"
    pommit = 0
    vasen = x - 1
    if vasen < 0: vasen = 0
    oikia = x + 2
    if oikia >= len(state["field"][0]) + 2: oikia = len(state["field"][0])
    yla = y - 1
    if yla < 0: yla = 0
    ala = y + 1
    if ala >= len(state["field"]): ala = len(state["field"]) - 1
    while yla <= ala:
        for i in lista[yla][vasen:oikia]:
            if i == "x":
                pommit += 1
        yla += 1
    return pommit

def handle_mouse(x, y, button, mods):
    """
    This function is called when a mouse button is clicked inside the game window.
    Prints the position and clicked button of the mouse to the terminal.
    """
    try:
        x = int(x / 40)
        y = int(y / 40)
        if button == 1:
            if state["shown"][y][x] == "f":
                pass
            elif state["field"][y][x] == "x":
                voittocheck(1)
            elif state["field"][y][x] == "0":
                state["shown"][y][x] = state["field"][y][x]
                floodfill(state["field"], x, y)
                voittocheck(0)
            else:
                state["shown"][y][x] = state["field"][y][x]
                voittocheck(0)
        elif button == 4:
            if state["shown"][y][x] == " ":
                if state["merkatut"] == state["pommit"]:
                    pass
                else:
                    state["shown"][y][x] = "f"
                    state["merkatut"] += 1
                    voittocheck(0)
            elif state["shown"][y][x] == "f":
                state["shown"][y][x] = " "
                state["merkatut"] -= 1
            else:
                pass
    except IndexError:
        pass

def voittocheck(w):
    muuttuja = 0
    for i in state["shown"]:
        for j in i:
            if j == " ":
                muuttuja += 1
    if muuttuja == 0 or w == 1:
        if w == 1:
            print("\nGame over - you stepped on a mine!")
            voitto = "Lost -"
        else:
            print("\nVictory!")
            voitto = "Victory -"
        pommifound = 0
        pommilkm = 0
        for i in state["field"]:
            for j in i:
                if j == "x":
                    pommilkm += 1
        for iidx, i in enumerate(state["shown"]):
            for jidx, j in enumerate(i):
                if j == "f":
                    if state["field"][iidx][jidx] == "x":
                        pommifound += 1
        state["shown"] = state["field"]
        print(f"You found {pommifound} mine(s) out of {pommilkm} mine(s).")

        state["aika"][1] = time.time()
        alku, loppu = state["aika"]
        kesto = round(loppu - alku)
        now = datetime.datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M")
        state["stats"].append(f"{dt_string}, {kesto} second game: {voitto} found {pommifound} mine(s) out of {pommilkm} mine(s)")

        print("Closing window...")
        aika = 4
        for i in range(4):
            print(aika)
            aika -= 1
            time.sleep(1)
        sweeperlib.close()

def draw_field():
    """
    A handler function that draws a field represented by a two-dimensional list
    into a game window. This function is called whenever the game engine requests
    a screen update.
    """
    sweeperlib.clear_window()
    sweeperlib.draw_background()
    sweeperlib.begin_sprite_draw()
    for iidx, i in enumerate(state["shown"]):
        for jidx, j in enumerate(i):
            if j == "x":
                sweeperlib.prepare_sprite("x", jidx * 40, iidx * 40)
            elif j == "f":
                sweeperlib.prepare_sprite("f", jidx * 40, iidx * 40)
            elif j == " ":
                sweeperlib.prepare_sprite(" ", jidx * 40, iidx * 40)
            else:
                for k in range(9):
                    if j == str(k):
                        sweeperlib.prepare_sprite(str(k), jidx * 40, iidx * 40)

    sweeperlib.prepare_sprite(("f"), 5, len(state["field"])*40+5)
    sweeperlib.draw_sprites()
    sweeperlib.draw_text(str(state["merkatut"]) + " / " + str(state["pommit"]), 50, len(state["field"])*40-5, font="Hydrophilia Iced")
    sweeperlib.draw_text(str(state["kello"]), len(state["field"][0])*40-100, len(state["field"])*40-5, font="Hydrophilia Iced") 
    #Sweeperlib default fontti ei toiminut, asensin sitten tämän "Hydrophilia Iced" fontin. Fonttitiedosto mukana miinaharava-kansiossa.

def place_mines(fieldlist, availabletileslist, noofmines):
    """
    Places N mines to a field in random tiles.
    """
    for i in range(noofmines):
        x, y = availabletileslist[random.randint(0, len(availabletileslist)-1)]
        availabletileslist.remove([x, y])
        fieldlist[y][x] = "x"
    state["field"] = fieldlist

def floodfill(list, x, y):
    """
    Marks previously unknown connected areas as safe, starting from the given
    x, y coordinates.
    """
    check = [[x, y]]

    while True:
        if len(check) == 0:
            break
        x, y = check.pop(-1)
        try:
            if list[y][x] != "x":
                state["shown"][y][x] = list[y][x]
                for i in range(-1, 2):
                    ya = y + i
                    for j in range(-1, 2):
                        xa = x + j
                        if xa >= 0 and ya >= 0 and state["shown"][ya][xa] == " " and list[ya][xa] != "x":
                            if state["shown"][y][x] != "0":
                                pass
                            else:
                                check.append([xa, ya])
            else:
                print("floodfill() error")
                break
        except IndexError:
            continue

def intervalli(x):
    state["kello"] += 1

def main():
    """
    Loads the game graphics, creates a game window, and sets a draw handler
    """
    sweeperlib.load_sprites("sprites")
    sweeperlib.create_window(len(state["field"][0])*40, len(state["field"])*40+50)
    sweeperlib.set_draw_handler(draw_field)
    sweeperlib.set_mouse_handler(handle_mouse)
    sweeperlib.set_interval_handler(intervalli, 60/60)
    sweeperlib.start()

def aloitus():
    state["kello"] = 0
    state["pommit"] = 0
    state["merkatut"] = 0
    while True:
        try:
            leveys = int(input("\nInput grid width: "))
            korkeus = int(input("Input grid height: "))
            if leveys < 2 or korkeus < 2:
                print("Grid too small.")
                continue
            else:
                break
        except NameError:
            print("Check input.")
        except ValueError:
            print("Integers please.")

    state["aika"][0] = time.time()

    field = []
    shown = []
    for row in range(korkeus):
        field.append([])
        shown.append([])
        for col in range(leveys):
            field[-1].append(" ")
            shown[-1].append(" ")

    state["shown"] = shown

    available = []
    for x in range(leveys):
        for y in range(korkeus):
            available.append([x, y])

    pommit = 0
    for i in field:
        for j in i:
            pommit += 1
    if pommit / 7 < 1:
        pommit = 1
    else:
        pommit = int(pommit / 7)
    place_mines(field, available, pommit)
    state["pommit"] = pommit

    for iidx, i in enumerate(field):
        for jidx, j in enumerate(i):
            state["field"][iidx][jidx] = str(count_ninjas(jidx, iidx, field))

if __name__ == "__main__":

    print("\nWelcome to Minesweeper!")
    while True:
        print("\n1 New game")
        print("2 Stats")
        print("3 Quit")
        inputti = input("What would you like to do: ")
        if inputti == "1":
            aloitus()
            main()
        elif inputti == "2":
            if len(state["stats"]) == 0:
                print("No stats yet - play Minesweeper to gather stats!")
            else:
                for i in state["stats"]:
                    print(i)
        elif inputti == "3":
            break
        else:
            print("Invalid input!")
