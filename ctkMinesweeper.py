import customtkinter as ctk
import random 
from config import columns, rows, bombs
from PIL import Image

square_count = columns * rows

app = ctk.CTk()
app.title('Minesweeper')

#Images
one = ctk.CTkImage(Image.open('images/one.png'))
two = ctk.CTkImage(Image.open('images/two.png'))
three = ctk.CTkImage(Image.open('images/three.png'))
four = ctk.CTkImage(Image.open('images/four.png'))
five = ctk.CTkImage(Image.open('images/five.png'))
six = ctk.CTkImage(Image.open('images/six.png'))
seven = ctk.CTkImage(Image.open('images/seven.png'))
eight = ctk.CTkImage(Image.open('images/eight.png'))
bomb = ctk.CTkImage(Image.open('images/bomb.png'))
flag = ctk.CTkImage(Image.open('images/flag.png'), size = (12,12))
pixel_1 = ctk.CTkImage(Image.open('images/pixel_1.png'))
pixel_2 = ctk.CTkImage(Image.open('images/pixel_2.png'), size = ( 12,12))
happy = ctk.CTkImage(Image.open('images/smily.png'))
game_over = ctk.CTkImage(Image.open('images/game_over.png'))



header_frame = ctk.CTkFrame(app)
header_frame.grid(row=0, column=0)


game_frame = ctk.CTkFrame(app)
game_frame.grid(row = 1, column = 0)




bomb_seeds = []


def play():
    global bomb_seeds
    bomb_seeds.clear()
    for child in game_frame.winfo_children():
        child.destroy
    remaining_bombs_to_place = bombs
    while remaining_bombs_to_place >0:
        number = random.randint(0, square_count)
        if number in bomb_seeds:
            continue
        else:
            bomb_seeds.append(number)
            remaining_bombs_to_place -= 1
            print(f'{remaining_bombs_to_place=}')
    print(f'{bomb_seeds=}')

    for square in range(0, square_count):
        cel = cell(game_frame, square)
        #bomb setup






class cell(ctk.CTkFrame):
    def __init__(self, master, seed):
        super().__init__(master, border_width = 1, corner_radius=0, bg_color = 'transparent')

        self.seed = seed
        self.cell_value = 0

        if self.seed in bomb_seeds:
            self.cell_value += 9

        self.left = False
        self.right = False
        self.top = False
        self.bottom = False
        self.active = True

        if self.seed//columns == 0:
            self.top = True
        if self.seed%columns == 0:
            self.left = True
        if self.seed//columns == rows-1:
            self.bottom = True
        if self.seed%columns == rows-1:
            self.right = True

        adjacent_cells = {'top_left': self.seed - columns - 1, 
                            'top':self.seed - columns, 
                            'top_right':self.seed - columns + 1,
                            'left':self.seed - 1,
                            'right':self.seed + 1,
                            'bottom_left':self.seed + columns - 1,
                            'bottom':self.seed + columns,
                            'bottom_right':self.seed + columns + 1}
        
        if self.top:
            adjacent_cells['top'] = None
            adjacent_cells['top_left'] = None
            adjacent_cells['top_right'] = None
        if self.left:
            adjacent_cells['top_left'] = None
            adjacent_cells['bottom_left'] = None
            adjacent_cells['left'] = None
        if self.right:
            adjacent_cells['top_right'] = None
            adjacent_cells['bottom_right'] = None
            adjacent_cells['right'] = None
        if self.bottom:
            adjacent_cells['bottom'] = None
            adjacent_cells['bottom_left'] = None
            adjacent_cells['bottom_right'] = None


        adjacent_cells_list = list(adjacent_cells.values())
        self.adjacent_cells_list = adjacent_cells_list
        for neighbor in adjacent_cells_list:
            if neighbor in bomb_seeds:
                self.cell_value += 1

        
        
        self.cell_label = ctk.CTkLabel(self, text=None, image = pixel_1, height = 0, bg_color = 'transparent') 

        def assign_frame_images():
            
            if self.cell_value >= 9:
                self.cell_label.configure(image=bomb)
            
            if self.cell_value == 8:
                self.cell_label.configure(image=eight)

            if self.cell_value == 7:
                self.cell_label.configure(image=seven)

            if self.cell_value == 6:
                self.cell_label.configure(image=six)

            if self.cell_value == 5:
                self.cell_label.configure(image=five)

            if self.cell_value == 4:
                self.cell_label.configure(image=four)

            if self.cell_value == 3:
                self.cell_label.configure(image=three)

            if self.cell_value == 2:
                self.cell_label.configure(image=two)

            if self.cell_value == 1:
                self.cell_label.configure(image=one)

            self.cell_label.grid(column=0, row=0, sticky='nsew', padx = 2, pady=2)

        print(f'{self.seed=}, {adjacent_cells_list=}, {self.cell_value=}')
        assign_frame_images()


                



        def on_right_click():
            if self.button.cget('state') == 'normal':
                self.button.configure(state = 'disabled', image = flag)
                self.active = False
                for child in self.button.winfo_children():
                    child.bind('<Button-3>', lambda event: on_right_click())
                print(f'{self.button.winfo_children()}')
            elif self.button.cget('state') == 'disabled':
                self.button.configure(state = 'normal', image = pixel_2)
                self.active = True
            check_win()

        

        self.button = ctk.CTkButton(self.cell_label, width=20, height=20, corner_radius=2, text=None, fg_color = "#525252", command = lambda: check_cells(cell=self))
        self.button.bind('<Button-3>', lambda event:on_right_click())
        

        self.button.grid(column=0, row=0, sticky = 'nsew')

        self.grid(row=seed//columns, column=seed%columns, sticky='nsew')
        self.check_cells = lambda: check_cells(self)


def lose_game():
    print('Sorry!')
    for cell in game_frame.winfo_children():
        if cell.cell_value >=9 and cell.active:
            cell.button.destroy()
        cell.active = False


def check_win():
    for cell in game_frame.winfo_children():
        if cell.cell_value >= 9 and cell.active:
            return print('Still some bombs to go!')
    print('YOU WIN!')

def check_cells(cell:cell):
    if not cell.active:
        return
    cell.button.destroy()
    cell.active = False
    if cell.cell_value >= 1 and cell.cell_value <=8:
        return
    if cell.cell_value == 0:
        for square in game_frame.winfo_children():
            if square.seed in cell.adjacent_cells_list:
                square.check_cells()
    if cell.cell_value >= 9:
        lose_game()
        return
    check_win()






reset_button = ctk.CTkButton(header_frame, image = happy, command = lambda: play())
reset_button.grid(row=0,column=0)

app.mainloop()