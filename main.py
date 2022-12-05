import uvage
import random

tick_count = 0

game_on = False
start_ticks = 0
draw_sps = True

health_sides = [uvage.from_color(100, 50, "gray", 206, 54), uvage.from_color(700, 50, "gray", 206, 54)]
health_background = uvage.from_color(400, 50, "white", 400, 54)
upper_background = uvage.from_color(400, 0, "gray", 800, 200)
grace = False
game_over = False
grace_period = 0
zone_hit = ""
streak = 0
streak_display = ""
speed = 7
health = 400
regen = 5/30
points = 0

highlight = uvage.from_color(-100, -100, "black", 40, 40)

camera = uvage.Camera(800, 600)

# make better ending screen
# file writing for score
# score counter in top left next to health bar
# different scores for perfect, good, etc

# zones
okay_zone = uvage.from_color(400, 530, "white", 800, 50)
good_zone = uvage.from_color(400, 530, "white", 800, 30)
excellent_zone = uvage.from_color(400, 530, "white", 800, 15)
perfect_zone = uvage.from_color(400, 530, "black", 800, 4)
health_bar = uvage.from_image(400, 50, "health_bar.png")


starting_screen = [uvage.from_text(400, 200, "COMPUTER SCIENCE", 50, "blue"),
                   uvage.from_text(400, 250, "COMPUTER SCIENCE", 50, "purple"),
                   uvage.from_text(400, 300, "REVOLUTION", 50, "green")]
space_to_start = uvage.from_text(400, 400, "press space bar to start", 50, "black")

game_over_screen = uvage.from_text(400, 300, "GAME OVER", 50, "red", bold = True)

left_target = uvage.from_image(100, 530, "left_arrow_hit.png")

down_target = uvage.from_image(300, 530, "down_arrow_hit.png")

up_target = uvage.from_image(500, 530, "up_arrow_hit.png")

right_target = uvage.from_image(700, 530, "right_arrow_hit.png")


target_arrows = []
hit_arrows = []
missed_arrows = []
all_arrows = []


def display_arrows(arrow_list):
    """
    changes y value and draws all arrows in list
    :param arrow_list: arrows being manipulated
    :return:
    """
    for item in arrow_list:
        # only fall if no missed arrows
        # gives player time to readjust after missing
        if game_on and not missed_arrows:
            item[0].y += speed
        camera.draw(item[0])
    return


def find_arrow_zone():
    """
    finds feedback zone of arrow hit
    :return: string feed_back zone. value depends on timing in hitting arrows
    """
    global target_arrows, hit_arrows, streak, streak_display, points
    # checks if perfect first
    if target_arrows[0][0].touches(perfect_zone):
        return_zone = "PERFECT!"
        points += 100
    elif target_arrows[0][0].touches(excellent_zone):
        return_zone = "excellent!"
        points += 70
    elif target_arrows[0][0].touches(good_zone):
        return_zone = "good"
        points += 50
    else:
        return_zone = "okay"
        points += 40
    # creates gray arrow with same x and y value as arrow hit
    hit_arrows += [[uvage.from_image(target_arrows[0][0].x, target_arrows[0][0].y, target_arrows[0][1] + "_arrow_hit.png"), target_arrows[0][1]]]
    # deletes arrow hit
    del(target_arrows[0])
    streak += 1
    streak_display = str(streak)
    return return_zone


def button_pressed(key):
    """
    when user presses key makes appropriate changes to health and streak
    :param key: string of key input pressed
    :return:
    """
    global zone_hit, streak, grace, missed_arrows, health
    zone_hit = "miss"
    # checks that there are arrows needed to be hit so can index
    if len(target_arrows) != 0:
        # checks if orientation of arrow is same as key pressed
        # checks if user hit key within acceptable range
        if target_arrows[0][1] == key and target_arrows[0][0].touches(okay_zone):
            # calles function to find feedback for arrow
            zone_hit = find_arrow_zone()
        else:
            # if not hit or arrow is wrong, reset streak, lose health
            streak = 0
            health -= 50
            # add red arrow to show user which arrow was missed
            missed_arrows += [
                [uvage.from_image(target_arrows[0][0].x, target_arrows[0][0].y, target_arrows[0][1] + "_arrow_missed.png"),
                 target_arrows[0][1]]]
            # delete arrow missed
            del (target_arrows[0])
    else:
        # if button pressed but no arrows, reset streak and lose health
        health -= 50
        streak = 0
    # start grace period so inputs are not double counted
    grace = True
    return


def del_arrows(arrow_type):
    """
    deletes first arrow in the desired arrow list if is below the screen
    :param arrow_type: list of arrows deleting offscreen arrows for
    :return:
    """
    global streak, target_arrows, all_arrows, missed_arrows, hit_arrows, health
    # checks length to avoid indexing error
    # if first arrow in list is below screen, delete it
    if len(arrow_type) != 0 and arrow_type[0][0].top > camera.bottom:
        del (arrow_type[0])
        # if target arrows go below screen reset streak and lose health
        if arrow_type == target_arrows:
            streak = 0
            health -= 50
    return


def tick():
    global target_arrows, tick_count, grace, grace_period, zone_hit, hit_arrows, streak, missed_arrows, all_arrows, \
        streak_display, speed, regen, health, game_on, highlight, game_over, start_ticks, draw_sps

    # clears camera
    camera.clear("white")

    speed = 7 + tick_count // 500

    # draws the hit zones which register how well arrow was hit
    camera.draw(okay_zone)
    camera.draw(good_zone)
    camera.draw(excellent_zone)
    camera.draw(perfect_zone)

    # draws arrows at bottom of screen
    camera.draw(left_target)
    camera.draw(right_target)
    camera.draw(up_target)
    camera.draw(down_target)

    if game_on:

        new_arrow = []

        # highlights the arrow that was hit
        if grace_period:
            camera.draw(highlight)

        # leaves missed arrows on screen for short period
        # deletes them after
        if grace_period and grace_period % 10 == 0:
            if missed_arrows:
                del missed_arrows[0]

        # ends grace period
        # resets variables showing zone of last arrow hit and current streak
        if grace_period % 10 == 0:
            grace = False
            grace_period = 0
            zone_hit = ""
            streak_display = ""

        # deletes arrows if they are outside camera range
        del_arrows(target_arrows)
        del_arrows(hit_arrows)
        del_arrows(missed_arrows)
        del_arrows(all_arrows)

        # adds new arrow if no current arrows or an arrow goes offscreen
        if len(all_arrows) == 0 or all_arrows[-1][0].y >= 50:
            # arrow is either left, right, up, down or just a space
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

        # inputs aren't valid during grace period so cannot spam button
        if not grace:
            # highlights the arrow pressed at the bottom of screen
            # registers what arrow was pressed
            if uvage.is_pressing("left arrow"):
                button_pressed("left")
                highlight = uvage.from_image(100, 530, "left_arrow.png")
            if uvage.is_pressing("down arrow"):
                button_pressed("down")
                highlight = uvage.from_image(300, 530, "down_arrow.png")
            if uvage.is_pressing("up arrow"):
                button_pressed("up")
                highlight = uvage.from_image(500, 530, "up_arrow.png")
            if uvage.is_pressing("right arrow"):
                button_pressed("right")
                highlight = uvage.from_image(700, 530, "right_arrow.png")
        # when health is < 0 game ends
        if health <= 0:
            game_on = False
            game_over = True

        # displays text showing how well arrow was hit
        zone_feedback = uvage.from_text(400, 250, zone_hit, 30, "black")
        camera.draw(zone_feedback)

        # displays current streak of arrows hit
        streak_counter = uvage.from_text(400, 300, streak_display, 30, "black")
        camera.draw(streak_counter)

        # if health is not full and streak threshold is hit regain health
        if streak >= 15 and health < 400:
            health += regen

        # if health goes over max from regen reset to max
        if health > 400:
            health = 400

        # increment amount of ticks game has been on for
        tick_count += 1
        # increment how long grace period has lasted
        if grace:
            grace_period += 1

    # display all arrows either hit, missed, meant to be hit
    display_arrows(target_arrows)
    display_arrows(hit_arrows)
    display_arrows(missed_arrows)
    display_arrows(all_arrows)

    # draws part of gray border for health bar
    camera.draw(upper_background)

    # creates red box representing amount of health
    health_meter = uvage.from_color(health, 50, "red", 400, 54)

    # draws white behind health meter for contrast
    camera.draw(health_background)

    # draws health meter overtop background
    camera.draw(health_meter)

    # draws sides of gray border so health meter does not spill past border when health decreases
    for x in health_sides:
        camera.draw(x)

    # if game is not on and player has not lost draw starting screen
    if not game_on:
        if not game_over:
            start_ticks += 1
            for x in starting_screen:
                camera.draw(x)
            if start_ticks % 10 == 0:
                draw_sps = not draw_sps
            if draw_sps:
                camera.draw(space_to_start)
        # if game is not on because player lost draw game over
        else:
            camera.draw(game_over_screen)
        # if player presses space game is reset to true
        if uvage.is_pressing("space"):
            game_on = True

    # draws casing for health meter
    camera.draw(health_bar)

    camera.display()


ticks_per_second = 30

uvage.timer_loop(ticks_per_second, tick)
