import sys

# Function which displays pause screen and returns user actions
def pause():
    print "Paused!"
    cont = 1
    while cont == 1:
        event = raw_input()
        if event == "c":
            return

# Pseudo mainloop
while 1:
    event = raw_input()
    if event == "q":
        sys.exit()
    elif event == "p":
        pause()
    print "Shizz"
    print "More shizz"