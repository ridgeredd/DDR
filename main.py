import uvage
import random

tick_count = 0

grace = False
grace_period = 0
zone_hit = ""

camera = uvage.Camera(800, 600)

okay_zone = uvage.from_color(400, 530, "black", 800, 140)
good_zone = uvage.from_color(400, 530, "black", 800, 100)
excellent_zone = uvage.from_color(400, 530, "black", 800, 60)
perfect_zone = uvage.from_color(400, 530, "white", 800, 20)

arrows = []
hit_arrows = []


def find_arrow_zone():
    if arrows[0][0].touches(perfect_zone):
        return_zone = "perfect"
    elif arrows[0][0].touches(excellent_zone):
        return_zone = "excellent"
    elif arrows[0][0].touches(good_zone):
        return_zone = "good"
    else:
        return_zone = "okay"
    hit_arrows += [uvage.from_image(arrows[0].x, arrows[0].y, arrows[1] + "_arrow_hit.png"), arrows[1]]
    del(arrows[0])
    return return_zone


def tick():
    global arrows
    global tick_count
    global grace
    global grace_period
    global zone_hit
    global hit_arrows

    speed = tick_count // 250 + 5

    new_arrow = []

    camera.clear("black")

    camera.draw(okay_zone)
    camera.draw(good_zone)
    camera.draw(excellent_zone)
    camera.draw(perfect_zone)

    if grace_period % 10 == 0:
        grace = False
        grace_period = 0
        zone_hit = ""

    if len(arrows) != 0 and arrows[0][0].top > camera.bottom:
        del(arrows[0])

    if len(arrows) != 0 and hit_arrows[0][0].top > camera.bottom:
        del(arrows[0])

    if len(arrows) == 0 or arrows[-1][0].y >= 50:
        x = random.randint(0, 8)
        if x == 0:
            new_arrow = [uvage.from_color(-100, -100, "black", 40, 40), "black"]
        if 1 <= x < 3:
            new_arrow = [uvage.from_image(100, -100, "left_arrow.png"), "left"]
        elif 3 <= x < 5:
            new_arrow = [uvage.from_image(300, -100, "down_arrow.png"), "down"]
        elif 5 <= x < 7:
            new_arrow = [uvage.from_image(500, -100, "up_arrow.png"), "up"]
        elif 7 <= x < 9:
            new_arrow = [uvage.from_image(700, -100, "right_arrow.png"), "right"]
        arrows += [new_arrow]

    if not grace:
        if uvage.is_pressing("left arrow"):
            if arrows[0][1] == "left" and arrows[0][0].touches(okay_zone):
                zone_hit = find_arrow_zone()
            else:
                zone_hit = "miss"
            grace = True

        if uvage.is_pressing("up arrow"):
            if arrows[0][1] == "up" and arrows[0][0].touches(okay_zone):
                zone_hit = find_arrow_zone()
            else:
                zone_hit = "miss"
            grace = True

        if uvage.is_pressing("down arrow"):
            if arrows[0][1] == "down" and arrows[0][0].touches(okay_zone):
                zone_hit = find_arrow_zone()
            else:
                zone_hit = "miss"
            grace = True

        if uvage.is_pressing("right arrow"):
            if arrows[0][1] == "right" and arrows[0][0].touches(okay_zone):
                zone_hit = find_arrow_zone()
            else:
                zone_hit = "miss"
            grace = True

    for item in arrows:
        item[0].y += speed
        camera.draw(item[0])

    zone_feedback = uvage.from_text(400, 200, zone_hit, 30, "white")

    camera.draw(zone_feedback)

    tick_count += 1
    if grace:
        grace_period += 1

    camera.display()


ticks_per_second = 30

uvage.timer_loop(ticks_per_second, tick)



