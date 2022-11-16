import uvage
import random

# need to separate none arrows from arrow list so that missing a blank turns next arrow red
# need to check if last none arrow > 50 (if none arrows exist) as well as reg arrows to create new arrow
# then delete last none arrow so not double counted
# also doesn't set streak to 0 if none arrow missed

tick_count = 0

grace = False
grace_period = 0
zone_hit = ""
streak = 0

camera = uvage.Camera(800, 600)

okay_zone = uvage.from_color(400, 530, "black", 800, 140)
good_zone = uvage.from_color(400, 530, "black", 800, 100)
excellent_zone = uvage.from_color(400, 530, "black", 800, 60)
perfect_zone = uvage.from_color(400, 530, "white", 800, 20)

arrows = []
hit_arrows = []
missed_arrows = []


def find_arrow_zone():
    global arrows, hit_arrows, streak
    if arrows[0][0].touches(perfect_zone):
        return_zone = "perfect"
    elif arrows[0][0].touches(excellent_zone):
        return_zone = "excellent"
    elif arrows[0][0].touches(good_zone):
        return_zone = "good"
    else:
        return_zone = "okay"
    hit_arrows += [[uvage.from_image(arrows[0][0].x, arrows[0][0].y, arrows[0][1] + "_arrow_hit.png"), arrows[0][1]]]
    del(arrows[0])
    streak += 1
    return return_zone


def tick():
    global arrows, tick_count, grace, grace_period, zone_hit, hit_arrows, streak, missed_arrows

    speed = tick_count // 1000 + 7

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
        streak = 0

    if len(hit_arrows) != 0 and hit_arrows[0][0].top > camera.bottom:
        del(hit_arrows[0])

    if len(missed_arrows) != 0 and missed_arrows[0][0].top > camera.bottom:
        del(missed_arrows[0])

    if len(arrows) == 0 or arrows[-1][0].y >= 50:
        x = random.randint(0, 8)
        if x == 0:
            new_arrow = [uvage.from_color(-100, -100, "black", 40, 40), "none"]
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
                streak = 0
                missed_arrows += [
                    [uvage.from_image(arrows[0][0].x, arrows[0][0].y, arrows[0][1] + "_arrow_missed.png"), arrows[0][1]]]
                del (arrows[0])
            grace = True

        if uvage.is_pressing("up arrow"):
            if arrows[0][1] == "up" and arrows[0][0].touches(okay_zone):
                zone_hit = find_arrow_zone()
            else:
                zone_hit = "miss"
                streak = 0
                missed_arrows += [
                    [uvage.from_image(arrows[0][0].x, arrows[0][0].y, arrows[0][1] + "_arrow_missed.png"),
                     arrows[0][1]]]
                del (arrows[0])
            grace = True

        if uvage.is_pressing("down arrow"):
            if arrows[0][1] == "down" and arrows[0][0].touches(okay_zone):
                zone_hit = find_arrow_zone()
            else:
                zone_hit = "miss"
                streak = 0
                missed_arrows += [
                    [uvage.from_image(arrows[0][0].x, arrows[0][0].y, arrows[0][1] + "_arrow_missed.png"),
                     arrows[0][1]]]
                del (arrows[0])
            grace = True

        if uvage.is_pressing("right arrow"):
            if arrows[0][1] == "right" and arrows[0][0].touches(okay_zone):
                zone_hit = find_arrow_zone()
            else:
                zone_hit = "miss"
                streak = 0
                missed_arrows += [
                    [uvage.from_image(arrows[0][0].x, arrows[0][0].y, arrows[0][1] + "_arrow_missed.png"),
                     arrows[0][1]]]
                del (arrows[0])
            grace = True

    for item in arrows:
        item[0].y += speed
        camera.draw(item[0])

    for item in hit_arrows:
        item[0].y += speed
        camera.draw(item[0])

    for item in missed_arrows:
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



