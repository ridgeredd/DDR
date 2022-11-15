import uvage
import random

tick_count = 0

camera = uvage.Camera(800, 600)

okay_zone = uvage.from_color(400, 530, "black", 800, 140)
good_zone = uvage.from_color(400, 530, "black", 800, 100)
excellent_zone = uvage.from_color(400, 530, "black", 800, 60)
perfect_zone = uvage.from_color(400, 530, "white", 800, 20)

arrows = []

def tick():
    global arrows
    global tick_count

    zone_hit = "miss"

    speed = tick_count // 500 + 5

    new_arrow = []

    camera.clear("black")

    camera.draw(okay_zone)
    camera.draw(good_zone)
    camera.draw(excellent_zone)
    camera.draw(perfect_zone)

    if len(arrows) != 0 and arrows[0][0].top > camera.bottom:
        del(arrows[0])

    if len(arrows) == 0 or arrows[-1][0].y >= 50:
        x = random.randint(0, 8)
        if x == 0:
            new_arrow = [uvage.from_color(-100, -100, "black", 40, 40), "black"]
        if 1 <= x < 3:
            new_arrow = [uvage.from_color(100, -100, "red", 40, 40), "red"]
        elif 3 <= x < 5:
            new_arrow = [uvage.from_color(300, -100, "yellow", 40, 40), "yellow"]
        elif 5 <= x < 7:
            new_arrow = [uvage.from_color(500, -100, "green", 40, 40), "green"]
        elif 7 <= x < 9:
            new_arrow = [uvage.from_color(700, -100, "blue", 40, 40), "blue"]
        arrows += [new_arrow]

    for item in arrows:
        item[0].y += speed
        camera.draw(item[0])

    if uvage.is_pressing("left arrow"):
        if arrows[0][1] == "red":
            if arrows[0][0].touches(perfect_zone):
                zone_hit = "perfect"
            elif arrows[0][0].touches(excellent_zone):
                zone_hit = "excellent"
            elif arrows[0][0].touches(good_zone):
                zone_hit = "good"
            elif arrows[0][0].touches(okay_zone):
                zone_hit = "okay"

    if uvage.is_pressing("up arrow"):
        if arrows[0][1] == "yellow":
            if arrows[0][0].touches(perfect_zone):
                zone_hit = "perfect"
            elif arrows[0][0].touches(excellent_zone):
                zone_hit = "excellent"
            elif arrows[0][0].touches(good_zone):
                zone_hit = "good"
            elif arrows[0][0].touches(okay_zone):
                zone_hit = "okay"

    if uvage.is_pressing("down arrow"):
        if arrows[0][1] == "green":
            if arrows[0][0].touches(perfect_zone):
                zone_hit = "perfect"
            elif arrows[0][0].touches(excellent_zone):
                zone_hit = "excellent"
            elif arrows[0][0].touches(good_zone):
                zone_hit = "good"
            elif arrows[0][0].touches(okay_zone):
                zone_hit = "okay"

    if uvage.is_pressing("right arrow"):
        if arrows[0][1] == "blue":
            if arrows[0][0].touches(perfect_zone):
                zone_hit = "perfect"
            elif arrows[0][0].touches(excellent_zone):
                zone_hit = "excellent"
            elif arrows[0][0].touches(good_zone):
                zone_hit = "good"
            elif arrows[0][0].touches(okay_zone):
                zone_hit = "okay"

    zone_feedback = uvage.from_text(400, 200, zone_hit, 30, "white")

    camera.draw(zone_feedback)

    tick_count += 1

    camera.display()

ticks_per_second = 30

uvage.timer_loop(ticks_per_second, tick)



