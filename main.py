import uvage
import random

tick_count = 0

camera = uvage.Camera(800, 600)

zone = uvage.from_color(400, 500, "white", 800, 40)

#speed = 20

arrows = []

def tick():
    global arrows
    global tick_count

    speed = tick_count // 500 + 5

    new_arrow = []

    camera.clear("black")

    camera.draw(zone)

    if len(arrows) != 0 and arrows[0].top > camera.bottom:
        del(arrows[0])

    if len(arrows) == 0 or arrows[-1].y >= 50:
        x = random.randint(0, 8)
        if x == 0:
            new_arrow = uvage.from_color(-100, -100, "black", 40, 40)
        if 1 <= x < 3:
            new_arrow = uvage.from_color(100, -100, "red", 40, 40)
        elif 3 <= x < 5:
            new_arrow = uvage.from_color(300, -100, "yellow", 40, 40)
        elif 5 <= x < 7:
            new_arrow = uvage.from_color(500, -100, "green", 40, 40)
        elif 7 <= x < 9:
            new_arrow = uvage.from_color(700, -100, "blue", 40, 40)
        arrows += [new_arrow]

    print(arrows)

    for item in arrows:
        item.y += speed
        camera.draw(item)

    tick_count += 1

    camera.display()

ticks_per_second = 30

uvage.timer_loop(ticks_per_second, tick)



