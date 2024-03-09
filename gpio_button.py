from gpiozero import Button
button = Button(7)
button.wait_for_press()
print('You pushed me')
