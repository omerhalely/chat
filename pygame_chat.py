from network import network
from functions import *

width = 500
height = 500
chat_width = 300
chat_height = 30
win = pygame.display.set_mode((width, height))


def main():
    run = True
    rect = rect_class(width / 2 - (chat_width / 2), height / 2 - (chat_height / 2) + 200, "~",
                      "red", chat_height, chat_width, win)
    chat_box = None
    pressed_key = None
    first_chat_box = create_chat_box([rect], win)
    second_chat_box = create_chat_box([rect], win)
    temp = 0
    n = network()
    p = n.getP()
    last_massage = ["0", "0", "0"]
    current_message = 1
    caps_lock_tracker = 0

    my_name = ["Player " + str(n.id)]
    contact_names = get_rest_names(my_name[0], my_name)
    contact_blocks = []
    for i in range(1, len(contact_names)):
        j = i - 1
        contact_blocks.append(rect_class(5 + j * 100 + j, 5, contact_names[i], "white", chat_height - 10, 100, win))
    all_contact_chat_box = [first_chat_box, second_chat_box]
    run_count = 0
    while run:  # game while loop
        p2 = n.send(p).split(",")
        different_msg_temp = get_different_msg(last_massage, contact_blocks, p2, int(n.id))
        different_msg_lst = different_msg_temp[0]
        different_msg_real = different_msg_temp[1]
        if different_msg_lst != []:
            for k in range(0, len(different_msg_lst)):
                push_message(all_contact_chat_box[different_msg_lst[k]], p2[different_msg_real[k]])
            last_massage = p2
            current_message += 1

        change_colors_for_connected_players(contact_blocks, p2)

        if temp == 1:
            rect.text = "~"
            temp = 0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            keys = pygame.key.get_pressed()
            if keys[pygame.K_ESCAPE]:  # exit game
                run = False
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                clicked_contact = mouse_click(pos, contact_blocks)
                if clicked_contact != None:
                    chat_box = all_contact_chat_box[clicked_contact]
                    read_message(chat_box, contact_blocks, clicked_contact)
            if chat_box != None:
                if event.type == pygame.KEYDOWN:
                    pressed_key = pygame.key.name(event.key)  # get pressed key
                    if pressed_key == "caps lock":
                        caps_lock_tracker += 1
        if chat_box != None:
            temp = write(rect, pressed_key, chat_box, caps_lock_tracker)
            pressed_key = None
            p = rect.text
            redrawWindow(win, chat_box, contact_blocks)
        else:
            for contact in contact_blocks:
                contact.draw()
            pygame.display.update()


main()
