import tkinter as tk
from config import columns, rows, bombs
import random
from tkinter import ttk
squares = columns * rows

app = tk.Tk()
app.title('Minesweeper')
app.columnconfigure(0, minsize=10)

pixel = tk.PhotoImage(file=r'images\pixel.png')
bomb = tk.PhotoImage(file=r'images\bomb.png')
flag = tk.PhotoImage(file=r'images\flag.png')

remaining_bombs_to_place = bombs

bomb_seeds = []
while remaining_bombs_to_place >0:
    number = random.randint(0, squares)
    if number in bomb_seeds:
        continue
    else:
        bomb_seeds.append(number)
        remaining_bombs_to_place -= 1
        print(f'{remaining_bombs_to_place=}')
print(bomb_seeds)

game_matt = tk.Frame(app)
game_matt.pack()
class square(tk.Frame):
    def __init__(self, master, seed = None):
        super().__init__(master, borderwidth=0.1)

        self.seed=seed
        self.cell_value = 0
        self.top = False
        self.bottom = False
        self.left = False
        self.right = False
        if self.seed // columns <= 1:
            self.top = True
        if self.top:
            print(f'top:{self.seed=}')
            self.configure(background='red')
        self.adjacent_squares = [self.seed - columns - 1, 
                            self.seed - columns, 
                            self.seed - columns + 1,
                            self.seed + 1,
                            self.seed - 1,
                            self.seed + columns - 1,
                            self.seed + columns,
                            self.seed + columns + 1]


        

        if self.seed in bomb_seeds:
            self.label = tk.Label(self, image=bomb)
            self.cell_value += 9
        else:
            
            for cell in self.adjacent_squares:
                if cell in bomb_seeds:
                    self.cell_value += 1
            self.label = tk.Label(self, text=str(self.cell_value))
        self.label.grid(row=0, column=0)



        self.columnconfigure(0, minsize=12)
        self.rowconfigure(0, minsize=12)
        self.grid(row=seed//columns, column=seed%columns)
        self.button = tk.Button(self,image=pixel, height=15, width=15, command= lambda: on_click())
        self.button.grid(row=0, column=0, sticky ='nsew')
        self.button.bind('<Button-3>', lambda event:on_rightclick())



        def on_click():
            if self.cell_value == 0:
                self.button.destroy()               
                for cell in game_matt.winfo_children():
                    if cell.button:
                        if cell.seed in self.adjacent_squares and cell.cell_value == 0:
                            cell.button.destroy()
                cleanup()
            else:
                self.button.destroy()

        def cleanup():
            print('cleaning up')
            for cell in game_matt.winfo_children():
                #if the cell value is zero and its button is missing
                #if cell.cell_value == 0: # and not cell.button:
                if not isinstance(cell.button, tk.Button):
                    print(f"{cell.seed}'s neighbords should be destroyed")
                    for other_cell in game_matt.winfo_children():
                        if other_cell.seed in self.adjacent_squares:
                            other_cell.button.destroy()
                    


        print(f'{self.seed=}')
        print(f'{self.adjacent_squares=}')



        def on_rightclick():
            print(f'Old state: {self.button.cget('state')}')
            if self.button.cget('state') == 'normal':
                
                self.button.configure(state ='disabled', image = flag)
                print(f'New state: {self.button.cget('state')}')
                return
            if self.button.cget('state') == 'disabled':
                
                self.button.configure(state='normal')
                self.button.configure(image=pixel)
                print(f'New state: {self.button.cget('state')}')
                return

            


            # self.button.config(state='disabled')
        # def cascade_buttons():
        #     for button in game_matt.winfo_children():
        #         if button.seed in self.adjacent_squares

        #     self.button.destroy()




for item in range(0, squares):
    test = square(game_matt, item)


app.mainloop()


#game behavior:
#if you click on a 0, all adjacent cells are clicked
#if a cell contains a non-zero digit, only that cell is clicked
#if a cell contains a bomb, game is lost.