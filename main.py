import uvage
import random

tick_count = 0

grace = False
grace_period = 0
zone_hit = ""
streak = 0
streak_display = ""
speed = 7
health = 390
regen = 5/30

camera = uvage.Camera(1000, 600)

# make start and ending screen
# make it so everything stops when health = 0
# score counter
# change so that arrow has to be entirely within zone to be perfect
okay_zone = uvage.from_color(400, 530, "white", 800, 50)
good_zone = uvage.from_color(400, 530, "white", 800, 30)
excellent_zone = uvage.from_color(400, 530, "white", 800, 10)
perfect_zone = uvage.from_color(400, 530, "black", 800, 5)
health_bar = uvage.from_image(900, 250, "health_bar.png")

target_arrows = []
hit_arrows = []
missed_arrows = []
all_arrows = []


def display_arrows(arrow_list):
    for item in arrow_list:
        item[0].y += speed
        camera.draw(item[0])
    return


def find_arrow_zone():
    global target_arrows, hit_arrows, streak, streak_display
    if target_arrows[0][0].touches(perfect_zone):
        return_zone = "perfect"
    elif target_arrows[0][0].touches(excellent_zone):
        return_zone = "excellent"
    elif target_arrows[0][0].touches(good_zone):
        return_zone = "good"
    else:
        return_zone = "okay"
    hit_arrows += [[uvage.from_image(target_arrows[0][0].x, target_arrows[0][0].y, target_arrows[0][1] + "_arrow_hit.png"), target_arrows[0][1]]]
    del(target_arrows[0])
    streak += 1
    streak_display = str(streak)
    return return_zone


def button_pressed(key):
    global zone_hit, streak, grace, missed_arrows, health
    zone_hit = "miss"
    if len(target_arrows) != 0:
        if target_arrows[0][1] == key and target_arrows[0][0].touches(okay_zone):
            zone_hit = find_arrow_zone()
        else:
            streak = 0
            health -= 50
            missed_arrows += [
                [uvage.from_image(target_arrows[0][0].x, target_arrows[0][0].y, target_arrows[0][1] + "_arrow_missed.png"),
                 target_arrows[0][1]]]
            del (target_arrows[0])
    else:
        health -= 50
        streak = 0
    grace = True
    return


def del_arrows(arrow_type):
    global streak, target_arrows, all_arrows, missed_arrows, hit_arrows, health
    if len(arrow_type) != 0 and arrow_type[0][0].top > camera.bottom:
        del (arrow_type[0])
        if arrow_type == target_arrows:
            streak = 0
            health -= 25
    return


def tick():
    global target_arrows, tick_count, grace, grace_period, zone_hit, hit_arrows, streak, missed_arrows, all_arrows, \
        streak_display, speed, regen, health

    speed = tick_count // 1000 + 7

    new_arrow = []

    camera.clear("white")

    camera.draw(okay_zone)
    camera.draw(good_zone)
    camera.draw(excellent_zone)
    camera.draw(perfect_zone)

    if grace_period % 10 == 0:
        grace = False
        grace_period = 0
        zone_hit = ""
        streak_display = ""

    del_arrows(target_arrows)
    del_arrows(hit_arrows)
    del_arrows(missed_arrows)
    del_arrows(all_arrows)

    if len(all_arrows) == 0 or all_arrows[-1][0].y >= 50:
        x = random.randint(0, 8)
        blank_arrow = [uvage.from_color(-100, -100, "black", 40, 40), "none"]
        if 1 <= x < 3:
            new_arrow = [uvage.from_image(100, -100, "left_arrow.png"), "left"]
        elif 3 <= x < 5:
            new_arrow = [uvage.from_image(300, -100, "down_arrow.png"), "down"]
        elif 5 <= x < 7:
            new_arrow = [uvage.from_image(500, -100, "up_arrow.png"), "up"]
        elif 7 <= x < 9:
            new_arrow = [uvage.from_image(700, -100, "right_arrow.png"), "right"]
        if new_arrow:
            target_arrows += [new_arrow]
        all_arrows += [blank_arrow]

    if not grace:
        if uvage.is_pressing("left arrow"):
            button_pressed("left")

        if uvage.is_pressing("up arrow"):
            button_pressed("up")

        if uvage.is_pressing("down arrow"):
            button_pressed("down")

        if uvage.is_pressing("right arrow"):
            button_pressed("right")

    display_arrows(target_arrows)
    display_arrows(hit_arrows)
    display_arrows(missed_arrows)
    display_arrows(all_arrows)

    zone_feedback = uvage.from_text(400, 200, zone_hit, 30, "black")

    camera.draw(zone_feedback)

    streak_counter = uvage.from_text(400, 300, streak_display, 30, "black")

    camera.draw(streak_counter)

    if streak >= 15 and health < 390:
        health += regen

    if health > 390:
        health = 390

    health_meter = uvage.from_color(900, 640 - health, "red", 40, 390)

    camera.draw(health_meter)

    camera.draw(health_bar)

    tick_count += 1
    if grace:
        grace_period += 1

    camera.display()


ticks_per_second = 30

uvage.timer_loop(ticks_per_second, tick)
