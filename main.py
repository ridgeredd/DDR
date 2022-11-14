import uvage
import random

camera = uvage.Camera(800, 600)

speed = 1

arrows = [uvage.from_color(100, 0, "red", 40, 40)]

def tick():
    global arrows

    camera.clear("black")

    if arrows[-1].top > camera.bottom:
        del(arrows[-1])
        x = random.randint(0, 5)
        if x == 1:
            new_arrow = uvage.from_color(100, 0, "red", 40, 40)
        elif x == 2:
            new_arrow = uvage.from_color(300, 0, "yellow", 40, 40)
        elif x == 3:
            new_arrow = uvage.from_color(500, 0, "green", 40, 40)
        elif x == 4:
            new_arrow = uvage.from_color(700, 0, "blue", 40, 40)
        if x != 0:
            arrows += [new_arrow]

    for item in arrows:
        item.y += speed
        camera.draw(item)

        camera.display

uvage.timer_loop(30, tick)



