from blessed import Terminal
#from pyfiglet import Figlet
import sys
import logging
import socket
from threading import Thread

logging.basicConfig(filename='example.log', level=logging.DEBUG)

border_tl = '╭'
border_tr = '╮'
border_bl = '╰'
border_br = '╯'
border_h = '─'
border_v = '│'

host = "10.0.0.67"
port = 9999

term = Terminal()
#fig = Figlet(font='slant')
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((host, port))


class Panel:
    def __init__(self, text, title=None, title_side="center", width=None, height=None, pos=("center", "center"), is_figlet=False, text_center=True, input_mode = False):
        self.text = text
        self.title = title
        self.side = title_side
        self.width = width
        self.height = height
        if not ((width or height) == None):
            self.pos = pos
        self.is_figlet = is_figlet
        self.text_center = text_center
        self.input_mode = input_mode

    def redraw(self):
        width = 0
        if self.width == None:
            if term.width % 2 == 0:
                width = term.width-4
            else:
                width = term.width-3
        else:
            if isinstance(self.width, float):
                width = int(self.width*(term.width-4))
            else:
                width = self.width
        
        strings = []
        string_middle = 0
        if not self.is_figlet:
            strings = term.wrap(self.text, width=width)
            string_middle = int((len(strings))/2)
        count = 0
        height = 0
        if self.height == None:
            height = term.height-1
        else:
            if isinstance(self.height, float):
                height = int(self.height*term.height)
            else:
                height = self.height
        middleIndex = (len(range(height)))//2
        margin = 0
        if self.title:
            title = " " + self.title + " "
            if self.side == "center":
                margin = ((width - term.length(self.title))//2)
        
        padding_x = 0
        padding_y = 0
        if self.pos[0] == "center":
            padding_x = int((term.width - width)/2)
        elif self.pos[0] == "left":
            padding_x = 0
        elif self.pos[0] == "right":
            padding_x = (term.width-3) - width

        if self.pos[1] == "center":
            padding_y = int((term.height - height)/2)
        elif self.pos[1] == "top":
            padding_y = 0
        elif self.pos[1] == "bottom":
            padding_y = (term.height-2) - height

        text_in_box = False
        
        if (self.text_center == True) or (self.input_mode == True):
            for i in range(height):
                if i == 0:
                    if not (padding_y == 0):
                        for i in range(padding_y):
                            print("")
                    if self.title:
                        if self.side == "center":
                            if (term.length(self.title) % 2) == 0:
                                print((" " * padding_x) + border_tl + border_h * (margin-0) + title + (border_h * (margin-2)) + border_tr)
                            else:
                                print((" " * padding_x) + border_tl + border_h * (margin-0) + title + (border_h * (margin-1)) + border_tr)
    
                        elif self.side == "left":
                            print((" " * padding_x) + border_tl + border_h * (2) + title + (border_h * (width-term.length(self.title)-4)) + border_tr)
                        elif self.side == "right":
                            print((" " * padding_x) + border_tl + border_h * (width-term.length(self.title)-4) + title + (border_h * (2)) + border_tr)
                    else:
                        print((" " * padding_x) + border_tl + border_h * (width-0) + border_tr)
                elif i == middleIndex-(string_middle-count):
                    text_in_box = True
                    if self.is_figlet:
                        print((" " * padding_x) + border_v + self.text + border_v)
                    else:
                        if not self.text_center:
                            if self.input_mode:
                                print((" " * padding_x) + border_v + term.white + strings[count] + term.blue + term.blink(border_v) + (" " * (width-term.length(strings[count])-1)) + border_v)
                            else:
                                print(((" " * padding_x) + border_v + strings[count] + border_v))
                        else:
                            print((" " * padding_x) + border_v + term.white + term.center(strings[count], width) + term.blue + border_v)

                    if self.is_figlet != True:
                        if count != len(strings)-1:
                            count += 1
                elif i == height-1:
                    print((" " * padding_x) + border_bl + border_h * width + border_br)
                else:
                    print((" " * padding_x) + border_v+ (" " * (width)) + border_v)
        else:
            for i in range(height):
                if i == 0:
                    if not (padding_y == 0):
                        for i in range(padding_y):
                            print("")
                    if self.title:
                        if self.side == "center":
                            if (term.length(self.title) % 2) == 0:
                                print((" " * padding_x) + border_tl + border_h * (margin-0) + title + (border_h * (margin-2)) + border_tr)
                            else:
                                print((" " * padding_x) + border_tl + border_h * (margin-0) + title + (border_h * (margin-1)) + border_tr)

                        elif self.side == "left":
                            print((" " * padding_x) + border_tl + border_h * (2) + title + (border_h * (width-term.length(self.title)-4)) + border_tr)
                        elif self.side == "right":
                            print((" " * padding_x) + border_tl + border_h * (width-term.length(self.title)-4) + title + (border_h * (2)) + border_tr)
                    else:
                        print((" " * padding_x) + border_tl + border_h * (width-0) + border_tr)
                elif i == height-1:
                    print((" " * padding_x) + border_bl + border_h * width + border_br)
                else:
                    try:
                        if count != len(strings):
                            print((" " * padding_x) + border_v + (" " * 1) + term.white + strings[count] + term.blue + (" " * (width-term.length(strings[count])-1)) + border_v)
                            count += 1
                        else:
                            print((" " * padding_x) + border_v+ (" " * (width)) + border_v)
                    except IndexError as e:
                        print((" " * padding_x) + border_v+ (" " * (width)) + border_v)
    
    def ret_lines(self):
        width = 0
        if self.width == None:
            if term.width % 2 == 0:
                width = term.width-4
            else:
                width = term.width-3
        else:
            if isinstance(self.width, float):
                width = int(self.width*(term.width-4))
            else:
                width = self.width
        
        self.width = width
        
        stringsi = []
        string_middle = 0
        if not self.is_figlet:
            strings = term.wrap(self.text, width=width)
            string_middle = int((len(strings))/2)
        count = 0
        height = 0
        if self.height == None:
            height = term.height-1
        else:
            if isinstance(self.height, float):
                height = int(self.height*term.height)
            else:
                height = self.height
        
        self.height = height
        middleIndex = (len(range(height)))//2
        margin = 0
        if self.title:
            title = " " + self.title + " "
            if self.side == "center":
                margin = ((width - term.length(self.title))//2)
        
        padding_x = 0
        padding_y = 0
        if self.pos[0] == "center":
            padding_x = int((term.width - width)/2)
        elif self.pos[0] == "left":
            padding_x = 0
        elif self.pos[0] == "right":
            padding_x = (term.width-3) - width

        if self.pos[1] == "center":
            padding_y = int((term.height - height)/2)
        elif self.pos[1] == "top":
            padding_y = 0
        elif self.pos[1] == "bottom":
            padding_y = (term.height-2) - height
        self.padding_x = padding_x

        text_in_box = False
        
        if (self.text_center == True) or (self.input_mode == True):
            for i in range(height):
                if i == 0:
                    if not (padding_y == 0):
                        for i in range(padding_y):
                            stringsi.append("")
                    if self.title:
                        if self.side == "center":
                            if (term.length(self.title) % 2) == 0:
                                stringsi.append((" " * padding_x) + border_tl + border_h * (margin-0) + title + (border_h * (margin-2)) + border_tr)
                            else:
                                stringsi.append((" " * padding_x) + border_tl + border_h * (margin-0) + title + (border_h * (margin-1)) + border_tr)
    
                        elif self.side == "left":
                            stringsi.append((" " * padding_x) + border_tl + border_h * (2) + title + (border_h * (width-term.length(self.title)-4)) + border_tr)
                        elif self.side == "right":
                            stringsi.append((" " * padding_x) + border_tl + border_h * (width-term.length(self.title)-4) + title + (border_h * (2)) + border_tr)
                    else:
                        stringsi.append((" " * padding_x) + border_tl + border_h * (width-0) + border_tr)
                elif i == middleIndex-(string_middle-count):
                    text_in_box = True
                    if self.is_figlet:
                        stringsi.append((" " * padding_x) + border_v + self.text + border_v)
                    else:
                        if not self.text_center:
                            if self.input_mode:
                                stringsi.append((" " * padding_x) + border_v + term.white + strings[count] + term.blue + term.blink(border_v) + (" " * (width-term.length(strings[count])-1)) + border_v)
                            else:
                                stringsi.append(((" " * padding_x) + border_v + strings[count] + border_v))
                        else:
                            stringsi.append((" " * padding_x) + border_v + term.white + term.center(strings[count], width) + term.blue + border_v)

                    if self.is_figlet != True:
                        if count != len(strings)-1:
                            count += 1
                elif i == height-1:
                    stringsi.append((" " * padding_x) + border_bl + border_h * width + border_br)
                else:
                    stringsi.append((" " * padding_x) + border_v+ (" " * (width)) + border_v)
        else:
            for i in range(height):
                if i == 0:
                    if not (padding_y == 0):
                        for i in range(padding_y):
                            stringsi.append("")
                    if self.title:
                        if self.side == "center":
                            if (term.length(self.title) % 2) == 0:
                                stringsi.append((" " * padding_x) + border_tl + border_h * (margin-0) + title + (border_h * (margin-2)) + border_tr)
                            else:
                                stringsi.append((" " * padding_x) + border_tl + border_h * (margin-0) + title + (border_h * (margin-1)) + border_tr)

                        elif self.side == "left":
                            stringsi.append((" " * padding_x) + border_tl + border_h * (2) + title + (border_h * (width-term.length(self.title)-4)) + border_tr)
                        elif self.side == "right":
                            stringsi.append((" " * padding_x) + border_tl + border_h * (width-term.length(self.title)-4) + title + (border_h * (2)) + border_tr)
                    else:
                        stringsi.append((" " * padding_x) + border_tl + border_h * (width-0) + border_tr)
                elif i == height-1:
                    stringsi.append((" " * padding_x) + border_bl + border_h * width + border_br)
                else:
                    try:
                        if count != len(strings):
                            stringsi.append((" " * padding_x) + border_v + (" " * 1) + term.white + strings[count] + term.blue + (" " * (width-term.length(strings[count])-1)) + border_v)
                            count += 1
                        else:
                            stringsi.append((" " * padding_x) + border_v+ (" " * (width)) + border_v)
                    except IndexError as e:
                        stringsi.append((" " * padding_x) + border_v+ (" " * (width)) + border_v)
                    
        
        return stringsi

def start(username):
    print(term.clear)
    friends = {
        "friend1": {
            "messages": []
        }
    }
    people = [f"1. {username[12:]}"]
    a = Panel(" ", title="People", width=0.5, pos=("right", "top"))
    b = Panel("\n".join(friends["friend1"]["messages"]), title="Chat Box", width=0.5, height=0.899, pos=("left", "top"), text_center=False)
    c = Panel(" > ", title="Chat Input", width=0.5, height=3, pos=("right", "bottom"), title_side="left", text_center=False, input_mode=True)

    times_called = 0
    def update_messages():
        print(term.home + "", end="")
        nonlocal times_called
        times_called += 1
        logging.debug("times called: " + str(times_called))
        with term.hidden_cursor():
            b.text = "\n".join(friends["friend1"]["messages"])
            if not people == []:
                a.text = "\n".join(people)
            else:
                a.text = " "
            b_lines = b.ret_lines()
            a_lines = a.ret_lines()
            logging.debug(people)
            for i in range(len(a_lines)):
                try:
                    print(a_lines[i].strip() + b_lines[i].strip())
                    #Logging
                    #with open("log.txt", "ab") as f:
                    #    f.write((a[i].strip() + b_lines[i].strip() + "\n").encode("utf-8"))
                except:
                    try:
                        print(a_lines[i].strip())
                    except: 
                        print(a_lines[i].strip())

    def redraw():
        print(term.home)
        c_lines = c.ret_lines()
        for i in range(len(c_lines)):
            print(term.move_x(term.width-c.width-2) + c_lines[i].strip()) 

    def listen_for_messages():
        while True:
            message = client.recv(2048).decode()
            friends["friend1"]["messages"].append(message)
            if "has joined the chat" in message:
                people.append(str(len(people)+1) + ". " + message[1:-22])
                logging.debug("people: " + str(len(people)+1) + ". " + message[1:-22])
            update_messages()
            logging.debug("test")

    t = Thread(target=listen_for_messages)
    t.daemon = True
    t.start()

    update_messages()
    redraw()

    thing = "!name: " + username[12:]
    client.send(thing.encode())

    while True:
        with term.hidden_cursor(), term.cbreak():
            try:
                inp = term.inkey()
            except:
                continue

        if inp.is_sequence:
            if inp.name == "KEY_BACKSPACE":
                c.text = c.text[:-1]
                try:
                    redraw()
                except IndexError:
                    pass
            if inp.name == "KEY_ENTER":
                msg = None
                if "> " in c.text[:3]:
                    msg = c.text[3:]
                else:
                    msg = c.text

                friends["friend1"]["messages"].append(username[12:] + ": " + msg)
                client.send(msg.encode())
                update_messages()
                
                c.text = " > "
                redraw()

            if inp.name == "KEY_ESCAPE":
                print(term.clear + term.normal)
                sys.exit()
        else:
            c.text += inp
            redraw()
            



def confirm(username):
    with term.hidden_cursor():
        print(term.home + term.clear + term.move_y(-30))
        #for line in fig.renderText("Messanger").split("\n"):
        #    print(term.center(term.blue + line))
        print(term.move_down(5))
        print(term.center(term.blue + "Logged in as: " + term.white + username))
        print(term.center(term.blue + "Press " + term.red + "ENTER" + term.blue + " to continue"))
        while True:
            with term.cbreak():
                try:
                    inp = term.inkey()
                except:
                    continue
                
            if inp.name == "KEY_ENTER":
                start(username)
            if inp.name == "KEY_ESCAPE":
                print(term.clear + term.normal)
                loginScreen()

login_menu = 0
def loginScreen():
    global login_menu

    with term.hidden_cursor():
        print(term.home + term.move_y(-30))
        #for line in fig.renderText("Messanger").split("\n"):
        #    print(term.center(term.blue + line))

        if login_menu == 0:
            print(term.blue + term.move_down(5) + term.center("> Log In <"))
        else:
            print(term.white + term.move_down(5) + term.center("Log In"))
            
        if login_menu == 1:
            print(term.blue + term.move_down(1) + term.center("> Sign Up <"))
        else:
            print(term.white + term.move_down(1) + term.center("Sign Up"))

    return

def login():
    logging.debug("ran")
    print(term.home + term.clear)
    a = Panel("  Username: ", title="Input", width=0.5, height=3, pos=("center", "center"), input_mode=True, text_center=False, title_side="left")
    a.redraw()
    print(term.move_up(5) + term.center(f"{term.blue}What's your name?", term.width))

    while True:
        print(term.home)
        with term.cbreak(), term.hidden_cursor():
            try:
                inp = term.inkey()
            except:
                continue
        if inp.is_sequence:
            if inp.name == "KEY_ESCAPE":
                print(term.home + term.clear + term.normal)
                sys.exit()
            if inp.name == "KEY_BACKSPACE":
                a.text = a.text[:-1]
                a.redraw()
            if inp.name == "KEY_ENTER":
                msg = None
                if "> " in a.text[:12]:
                    msg = a.text[12:]
                else:
                    msg = a.text
                confirm(msg)
        else:
            a.text += inp
            a.redraw()

def main():
    global login_menu
    print(term.clear)
    loginScreen()
    while True:
        print(term.home)
        with term.cbreak(), term.hidden_cursor():
            try:
                inp = term.inkey()
            except:
                continue

        if inp.name == "KEY_DOWN":
            if login_menu == 0:
                login_menu = 1
                loginScreen()
                
            elif login_menu == 1:
                login_menu = 0
                loginScreen()
        elif inp.name == "KEY_UP":
            if login_menu == 0:
                login_menu = 1
                loginScreen()

            elif login_menu == 1:
                login_menu = 0
                loginScreen()

        elif inp.name == "KEY_ENTER":
            if login_menu == 0:
                login()
            elif login_menu == 1:
                #signup()
                pass
        elif inp.name == "KEY_ESCAPE":
            sys.exit()
                
if __name__ == "__main__":
    main()
