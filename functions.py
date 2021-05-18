import pygame
import winsound

pygame.font.init()
myfont = pygame.font.SysFont("arial", 20)
players_list = ["Player 0", "Player 1", "Player 2"]
class rect_class:
    def __init__(self, x, y, text, color, height, width, win):
        self.x = x
        self.y = y
        self.text = text
        self.color = color
        self.height = height
        self. width = width
        self.win = win
        self.rect = (x, y, width, height)
        self.border = False
    def change_color(self, new_color):
        self.color = new_color
    def create_border(self):
        self.border = True
    def update(self):
        self.rect = (self.x, self.y, self.width, self.height)
    def draw(self):
        pygame.draw.rect(self.win, self.color, self.rect)
        if self.border:
            x_up_border = rect_class(self.x, self.y, "", "white", 2, self.width, self.win)
            y_left_border = rect_class(self.x, self.y, "", "white", self.height, 2, self.win)
            x_bottom_border = rect_class(self.x, self.y + self.height - 2, "", "white", 2, self.width, self.win)
            y_right_border = rect_class(self.x + self.width - 2, self.y, "", "white", self.height, 2, self.win)
            pygame.draw.rect(self.win, "white", x_up_border.rect)
            pygame.draw.rect(self.win, "white", y_left_border.rect)
            pygame.draw.rect(self.win, "white", x_bottom_border.rect)
            pygame.draw.rect(self.win, "white", y_right_border.rect)
        self.win.blit(myfont.render(self.text, False, (0, 0, 0)), (self.x, self.y))
def change_colors_for_connected_players(contacts, connected_msg):
    for i in range(0, len(contacts)):
        player = int(contacts[i].text[-1])
        if connected_msg[player] == "1":
            contacts[i].color = "green"
        if connected_msg[player] == "0":
            contacts[i].color = "red"

def get_different_msg(last_msg, all_contact_chat_box, p2, id):
    index_lst = []
    real_index = []
    for i in range(0, len(p2)):
        if p2[i] != last_msg[i]:
            real_index.append(i)
            if i > id:
                index_lst.append(i - 1)
            if i < id:
                index_lst.append(i)
    for i in range(0, len(index_lst)):
        all_contact_chat_box[index_lst[i]].color = "blue"
    return (index_lst, real_index)

def redrawWindow(win, rec_lst, contacts):
    win.fill((0, 0, 0))
    for rec in rec_lst:
        rec.draw()
    for contact in contacts:
        contact.draw()
    pygame.display.update()

def mouse_click(pos, contacts):
    on_click = None
    for j in range(0, len(contacts)):
        contacts[j].border = False
    for i in range(0, len(contacts)):
        x_area = (contacts[i].x, contacts[i].x + contacts[i].width)
        y_area = (contacts[i].y, contacts[i].y + contacts[i].height)
        if pos[0] <= x_area[1] and pos[0] >= x_area[0]:
            if pos[1] <= y_area[1] and pos[1] >= y_area[0]:
                on_click = contacts[i]
                contacts[i].border = True
                break
    if on_click == None:
        return on_click
    return i

def read_message(chat_box, contact_blocks, clicked_contact):
    flag = 0
    for i in range(0, len(chat_box)):
        if chat_box[i].color == "blue":
            chat_box[i].color = "yellow"
            flag = 1
    if flag == 1:
        contact_blocks[clicked_contact].color = "green"

def write(rect, pressed_key, chat_box, caps_lock_tracker):
    if pressed_key == None:
        return 0
    if len(chat_box[0].text) >= 24:
        return 0
    if len(pressed_key) == 1:
        if caps_lock_tracker % 2 == 1:
            pressed_key = pressed_key.upper()
        rect.text += pressed_key
        return 0
    if pressed_key == "return":  # enter
        for i in range(len(chat_box) - 1, 0, -1):
            chat_box[i].text = chat_box[i - 1].text  # push message
            chat_box[i].color = chat_box[i - 1].color  # push color
        rect.text += "."
        return 1

    if pressed_key == "backspace":  # delete
        if rect.text == "~":
            return 0
        rect.text = rect.text[:-1]
        return 0
    if pressed_key == "space":  # space
        rect.text += " "
        return 0

def get_rest_names(name, lst):
    for i in range(0, len(players_list)):
        if players_list[i] == name:
            continue
        lst.append(players_list[i])
    return lst


def make_noise():
    duration = 700
    frequency = 400
    winsound.Beep(frequency, duration)

def create_chat_box(chat_box, win):
    rect = chat_box[0]
    chat_height = 30
    chat_width = 300
    for i in range(1, 13):
        new_rec = rect_class(rect.x, rect.y - i * rect.height - 2, "", "white",
                             chat_height, chat_width, win)
        chat_box.append(new_rec)
    return chat_box

def push_message(chat_box, message):
    temp_text = chat_box[0].text
    chat_box[0].text = message
    chat_box[0].color = "blue"
    for i in range(len(chat_box) - 1, 0, -1):
        chat_box[i].text = chat_box[i - 1].text
        chat_box[i].color = chat_box[i - 1].color
    chat_box[0].text = temp_text
    chat_box[0].color = "white"
    make_noise()
