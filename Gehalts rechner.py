stundenlohn = input("Was ist dein Stundenlohn: ")
tag = 8 * int(stundenlohn)
Monat = 20 * tag
Jahr = Monat * 12

print("Dein Stundenlohn beträgt " + str(stundenlohn) + " Euro")
print("Du verdienst " + str(tag) + " Euro pro Tag")
print("Du verdienst " + str(Monat) + " Euro pro Monat")
print("Du hast ein Jahresgehalt von " + str(Jahr) + " Euro")

input("")


