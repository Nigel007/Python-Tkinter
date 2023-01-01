# class Trial():
#     def __init__(self):
#         pass

# a = Trial()
# print(type(a) is Trial)
import random
from tkinter import *
# alist = {(1,2): 3, (4,5): 6, (7,8): 9}
# b = 4.0,5.0
# print(alist[7,8])
# if b in alist:
#     print("Hello")
#     alist.pop(b)
# else: 
#     print("NO")
# print(alist)
# def displaya(t):
#     displayf("Frightened")

# times = {
#         "Scatter" : 10,
#         "Chase" : 10, 
#         "Frightened" : 5
#     }


# def displays(state):
#     global main_state
#     main_state = state

# def displayc(state):
#     global main_state
#     main_state = state

# def displayf(state):
#     global main_state
#     main_state = state



# def displayb(state):
#     global main_state
#     if state == "Scatter":
#         new_state = "Chase"
#         displays(state)
#         time = times[state]

#     elif state == "Chase":
#         new_state = "Scatter"
#         displayc(state)
#         time = times[state]

#     elif state == "Frightened":
#         new_state = main_state
#         time = times[state]
#         displayc(state)
#     print(main_state)

#     main_state = new_state
#     root.after(time*1000, lambda: displayb(new_state))

# main_state = "Scatter"
def keydown(event):
    print("down")

def keyup(event):
    print("up")
root = Tk()
root.geometry("100x100")
root.bind("<KeyPress>", keydown)
root.bind("<KeyRelease>", keyup)
root.mainloop()


# for l in alist:
#     if alist[l] >2:
#         print(l)

