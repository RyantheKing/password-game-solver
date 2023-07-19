# a redesign of the main program. Designed to only implement rules once necessary to increase speed and robustness
import controller
import solver

# states: 
# 0: pre-captcha
# 1: pre-location
# 2: pre-chess
# 3: pre-fire
# 3: pre-video
# 5: pre-unused
# 6: pre-color
# 7: pre-final

def play_game():
    """
    Attempts to complete the password game
    """
    password = solver.generate_password(0)
    
    # initial password to obtain captcha
    controller.type_password_html(solver.password_to_html(0, password + solver.sum_25(password)))

    # get captcha answer to make geoguesser available
    captcha = controller.get_captcha_answer()
    password = solver.generate_password(1, captcha)
    controller.type_password_html(solver.password_to_html(1, password + solver.sum_25(password)))

    # get location to make chess available
    location = controller.get_location().lower()
    password = solver.generate_password(2, captcha, location)
    controller.type_password_html(solver.password_to_html(2, password + solver.sum_25(password)))

    # get chess move to make fire available
    chess_move = controller.get_chess_move()
    password = solver.generate_password(3, captcha, location, chess_move)
    password += solver.sum_25(password) + solver.get_element_string(password)
    html_pass = solver.password_to_html(3, password)
    controller.type_password_html(html_pass)

    # remove fire
    controller.type_password_html(html_pass)

    # get video to make unused letters available
    link = controller.get_video()
    solver.birth_paul()
    password = solver.generate_password(4, captcha, location, chess_move, link)
    old_password = password
    password += solver.sum_25(password) + solver.get_element_string(password)
    controller.type_password_html(solver.password_to_html(4, password))

    # click banned letters
    unused = solver.get_unused_letters(password)[-2:]
    controller.click_unused(unused)

    # get color to make final button available
    color = controller.get_color(old_password, unused)
    password = solver.generate_password(5, captcha, location, chess_move, link, color)
    password += solver.sum_25(password) + solver.get_element_string(password)
    password += solver.dot_string(password)
    html_pass = solver.password_to_html(5, password)
    controller.type_password_html(html_pass)

    controller.click_final_button()
    controller.set_final_text_box()
    controller.type_password_html(html_pass)

play_game()