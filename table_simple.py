from PIL import ImageTk, Image
import tkinter as tk
from tkinter import font, ttk
from tkinter.messagebox import askokcancel

import textwrap

### Configurar os grids para posicionamento de forma padrão input>>toolbar>>table
### Configurar para exibir widgets por chamada única da SimpleTable ex: show_toolbar=True, show_input_field=True

class SimpleTable(tk.Frame):

    def __init__(self, parent=None, elements_list=None, grid_on=None, select_mode='browse', max_rows=10, stripped=[False], column_name='Nome', width_default=400, inplace_list=False):
        super().__init__(parent)

        self.parent = parent
        self.select_mode = select_mode # 'extended'(múltiplos), 'browse' (único), 'none'(nenhum)
        self.position_grid(grid_on)

        self.selected_record = None

        self.elements_list = elements_list
        self.inplace_list = inplace_list # Habilita se alterações na lista atual podem interferir na lista original

        self.reset_selected() # mantem objeto de retorno Vazio/Nulo. Só carrega quando clicado
 
        self.style = ttk.Style()

        #LARGE_FONT= ("Verdana", 10)
        #SMALL_FONT= ("Verdana", 8)

        LARGE_FONT = 9
        SMALL_FONT = 9

        # Pick a theme 
        self.style.theme_use("default")

        # When LARGE_FONT is set to 12, the row height is set to 35. When SMALL_FONT
        # is set to 12, the row height is calculated as 30.
        #self.style.configure("Treeview.Heading",
        #                     font=("Verdana", LARGE_FONT),
        #                     rowheight=int(LARGE_FONT*2.5)
        #                     )
        self.style.configure("Treeview.Heading",
                             font=("Verdana", LARGE_FONT)
                             )
        
        # Configure outr treeview rows colors
        self.style.configure("Treeview",
                             background="#D3D3D3",
                             foreground="black",
                             fieldbackground="#D3D3D3",
                             font=("Verdana", SMALL_FONT),
                             rowheight=int(SMALL_FONT*2.5)
                             )
        
        # Change selected color
        self.style.map("Treeview", background=[('selected', 'blue')])

        # Scrollbar para Table Treeview
        self.tb_scroll_v = tk.Scrollbar(self, orient='vertical')
        self.tb_scroll_v.grid(row=0, column=1, stick='ns')
        self.tb_scroll_h = tk.Scrollbar(self, orient='horizontal')
        self.tb_scroll_h.grid(row=1, column=0, stick='we')


        # Create Treeview
        self.table = ttk.Treeview(self,
                                  height=max_rows,
                                  yscrollcommand=lambda f,l: self.autoscroll(self.tb_scroll_v, f, l),
                                  xscrollcommand=lambda f,l: self.autoscroll(self.tb_scroll_h, f, l),
                                  #selectmode='browse'
                                  selectmode=self.select_mode,
                                  takefocus=True
                                  )
        self.table.grid(row=0, column=0, padx=5, pady=5, stick='nswe')

        # Associar as barras de scroll às vistas 'x' e 'y' do objeto Treeview
        self.tb_scroll_v.configure(command=self.table.yview)
        self.tb_scroll_h.configure(command=self.table.xview)
        
        self.table['columns'] = ('name')
        self.table['displaycolumns'] = ('name')

        self.table.column("#0", width=0, stretch='NO')
        self.table.column("name", width=width_default, anchor='w')

        self.table.heading("#0", text='')
        self.table.heading("name", text=column_name, anchor='center')

        if stripped[0]:
            try:
                color1 = stripped[1]
                try:
                    color2 = stripped[2]
                except:
                    color2 = "lightgray"
            except:
                color1 = "white"
                color2 = "lightgray"

            self.stripped_table(color1, color2)
        else:
            self.stripped_table("white", "white")
        
        self.charge_table()

        self.table.bind("<Double-Button-1>", self.table_clicker)
        
        # Create Display: Total entities
        frm_display = tk.Frame(self)
        frm_display.grid(row=2, column=0, padx=5, stick='w')

        self.lbl_Total = tk.Label(frm_display,
                                  text="Total: ",
                                  font=font.Font(size=9, weight='bold'))
        self.lbl_Total.grid(row=0, column=0, padx=0, pady=0, stick='w')

        self.display = tk.IntVar()
        self.lbl_display = tk.Label(frm_display,
                                    textvariable=self.display,
                                    font=font.Font(size=9, weight='bold'))
        self.lbl_display.grid(row=0, column=1, padx=0, pady=0, stick='w')                        

        self.display.set(len(self.get_allrows_id()))


    def stripped_table(self, color1, color2):
        # Create striped row tags
        self.table.tag_configure('oddrow', background=color1)
        self.table.tag_configure('evenrow', background=color2)

    def position_grid(self, grid_on):
        row = grid_on['row'] if 'row' in grid_on.keys() else 0
        column = grid_on['column'] if 'column' in grid_on.keys() else 0
        columnspan = grid_on['columnspan'] if 'columnspan' in grid_on.keys() else 1
        padx = grid_on['padx'] if 'padx' in grid_on.keys() else 0
        pady = grid_on['pady'] if 'pady' in grid_on.keys() else 0
        
        self.grid(row=row, column=column, columnspan=columnspan, padx=padx, pady=pady)

    # Método Scroll para Table Treeview
    def autoscroll(self, sbar, first, last):
        # Hide and show scrollbar as need
        first, last = float(first), float(last)
        if first <= 0 and last >=1:
            sbar.grid_remove()
        else:
            sbar.grid()
        sbar.set(first, last)

    def charge_table(self):
        count = 0

        if len(self.elements_list) > 0:
            for element in self.elements_list:
                if count % 2 == 0:
                    self.table.insert(parent='', index='end', iid=count, values=(element,), tags=('oddrow'))
                else:
                    self.table.insert(parent='', index='end', iid=count, values=(element,), tags=('evenrow'))
                count += 1
        else:
            pass

       
    def table_clicker(self, event):
        self.selected_record = self.table.selection()[0]
        #print("Elemento selecionado:", self.table.item(self.selected_record,'values'))

    def wrap(self, string, lenght=50):
        return '\n'.join(textwrap.wrap(string, lenght))

    def clean_all(self):
        for item in self.table.get_children():
            self.table.delete(item)

    def recharge_table(self, elements_list):
        self.clean_all()
        self.elements_list = elements_list
        self.charge_table()
        self.display.set(len(self.get_allrows_id()))

    def get_selected(self):
        return self.element_selected if not self.element_selected is None else None

    def get_selected_record(self):
        return self.table.item(self.selected_record,'values')

    def reset_selected(self):
        self.element_selected = None
        
    def get_selecteds(self):
        list_selecteds = []

        for record_iid in self.table.selection():
            list_selecteds.append(record_iid)

        return list_selecteds

    def get_allrows_id(self):
        list_selecteds = []
        for record_iid in self.table.get_children():
            list_selecteds.append(record_iid)

        return list_selecteds

    def get_allrows_values(self):
        list_selecteds = []
        for record_iid in self.table.get_children():
            list_selecteds.append(self.table.item(record_iid, 'values'))

        return list_selecteds

    # implementar métodos
    # Adjust Stripped Color (recarregar com a lista atual para ordenar as cores)

    # Move Up
    def up(self):
        rows = self.table.selection()
        for row in reversed(rows):
            self.table.move(row, self.table.parent(row), self.table.index(row)-1)
            
    # Move Down
    def down(self):
        rows = self.table.selection()
        for row in reversed(rows):
            self.table.move(row, self.table.parent(row), self.table.index(row)+1)

    # Remove item
    def remove_item(self):

        if askokcancel("Remove", "Are you sure you want to remove the item?"):
            selecteds = self.table.selection()
            for selected in selecteds:
                if self.inplace_list:
                    # Obter selecionados
                    self.elements_list.remove(self.table.item(selected, 'values')[0])
                    #print("valor:", selected)
                    print("valor:", self.table.item(selected, 'values'))
                    #print("lista:", self.get_selecteds())
                self.table.delete(selected)


            self.display.set(len(self.get_allrows_id()))


    # Refresh Table with initial list
    def refresh(self):
        if askokcancel("Refresh", "Are you sure you want to refresh the table?"):
            self.clean_all()
            self.charge_table()
            self.display.set(len(self.get_allrows_id()))

    # Get Id
    def get_id(self):
        return self.table.selection()[0]

    # Get length records
    def get_length_records(self):
        return len(self.get_allrows_id())

    # Get Last Id
    def get_last_id(self):
        return self.get_length_records() - 1

    # Get BeforeId
    def get_before_id(self):
        before_id = int(self.get_id()) - 1
        if before_id < 0:
            before_id = self.get_last_id()
        self.selected_record = before_id
        return before_id

    # Get NextId
    def get_next_id(self):
        next_id = int(self.get_id()) + 1
        if next_id == self.get_length_records():
            next_id = 0
        self.selected_record = next_id
        return next_id

    # Get Before Value
    def get_before_value(self):
        return self.table.item(self.get_before_id(), 'values')[0]

    # Get Next Value
    def get_next_value(self):
        return self.table.item(self.get_next_id(), 'values')[0]

    # Get Value
    def get_value_by_id(self, record_iid):
        return self.table.item(record_iid, 'values')

    # Set selected
    def set_selected_by_id(self, record_iid):
        self.table.selection_set(record_iid)

    # Add element on table
    def set_element_on_table(self, new_item):
        if len(new_item) > 0:
            if not new_item in self.elements_list:
                self.elements_list.append(new_item)
                self.recharge_table(self.elements_list)
            else:
                tkmsg.showinfo('Aviso', 'A lista já contém o item informado!')
    
    
class SimpleTableNavigationToolbar(tk.Frame):

    def __init__(self, parent, simpleTable, grid_on=None):
        super().__init__(parent)

        self.table = simpleTable
        self.position_grid(grid_on)

        # Image Arrow Up
        self.arrow_up = Image.open('images/arrow_up_line.png')
        # Resize
        self.arrow_up = self.arrow_up.resize((15,15), Image.ANTIALIAS)
        self.arrow_up = ImageTk.PhotoImage(self.arrow_up)

        # Image Arrow Down
        self.arrow_down = Image.open('images/arrow_down_line.png')
        # Resize
        self.arrow_down = self.arrow_down.resize((15,15), Image.ANTIALIAS)
        self.arrow_down = ImageTk.PhotoImage(self.arrow_down)

        # Image Delete
        self.delete = Image.open('images/delete_bin_2_line.png')
        # Resize
        self.delete = self.delete.resize((15,15), Image.ANTIALIAS)
        self.delete = ImageTk.PhotoImage(self.delete)

        # Image Refresh
        self.refresh = Image.open('images/restart_line.png')
        # Resize
        self.refresh = self.refresh.resize((15,15), Image.ANTIALIAS)
        self.refresh = ImageTk.PhotoImage(self.refresh)

        self.body()
        
    def body(self):
        btn_up = tk.Button(self, borderwidth=0, relief='flat',
                          cursor='hand2',
                          image=self.arrow_up,
                          compound='top',
                          text="Up",
                          command=self.table.up)
        btn_up.grid(row=0, column=0, padx=5, pady=0, stick='nesw') #pack(side='left', fill='both')

        btn_down = tk.Button(self, borderwidth=0, relief='flat',
                          cursor='hand2',
                          image=self.arrow_down,
                          compound='top',
                          text="Down",
                          command=self.table.down)
        btn_down.grid(row=0, column=1, padx=5, pady=0, stick='nesw') #pack(side='left', fill='both')

        btn_delete = tk.Button(self, borderwidth=0, relief='flat',
                          cursor='hand2',
                          image=self.delete,
                          compound='top',
                          text="Delete",
                          command=self.table.remove_item)
        btn_delete.grid(row=0, column=2, padx=5, pady=0, stick='nesw') #pack(side='left', fill='both')

        btn_refresh = tk.Button(self, borderwidth=0, relief='flat',
                          cursor='hand2',
                          image=self.refresh,
                          compound='top',
                          text="Refresh",
                          command=self.table.refresh)
        btn_refresh.grid(row=0, column=3, padx=5, pady=0, stick='nesw') #pack(side='left', fill='both')

        if self.table.inplace_list:
            btn_refresh['state'] = 'disabled'

        

    def position_grid(self, grid_on):
        row = grid_on['row'] if 'row' in grid_on.keys() else 0
        column = grid_on['column'] if 'column' in grid_on.keys() else 0
        columnspan = grid_on['columnspan'] if 'columnspan' in grid_on.keys() else 1
        padx = grid_on['padx'] if 'padx' in grid_on.keys() else 0
        pady = grid_on['pady'] if 'pady' in grid_on.keys() else 0
        
        self.grid(row=row, column=column, columnspan=columnspan, padx=padx, pady=pady)

    
class SimpleTableInputField(tk.Frame):

    def __init__(self, parent, simpleTable, grid_on=None):
        super().__init__(parent)

        self.table = simpleTable
        self.position_grid(grid_on)

        # Image Add Item
        self.img_add = Image.open('images/add_line.png')
        # Resize
        self.img_add = self.img_add.resize((15,15), Image.ANTIALIAS)
        self.img_add = ImageTk.PhotoImage(self.img_add)

        self.body()

    def body(self):

        self.input_new_item = tk.Entry(self, width=50)
        self.input_new_item.grid(row=0, column=0, padx=5, pady=5, ipadx=5, ipady=5, stick='we')

        btn_add_item = tk.Button(self,
                                 text='',
                                 cursor='hand2',
                                 image=self.img_add,
                                 compound='top',
                                 width=50,
                                 font=font.Font(size=11, weight='bold'),
                                 command=lambda: [self.table.set_element_on_table(self.input_new_item.get().strip()), self.input_clear()]
                                 )
        btn_add_item.grid(row=0, column=2, padx=5, pady=0, stick='nesw')
        

    def position_grid(self, grid_on):
        row = grid_on['row'] if 'row' in grid_on.keys() else 0
        column = grid_on['column'] if 'column' in grid_on.keys() else 0
        columnspan = grid_on['columnspan'] if 'columnspan' in grid_on.keys() else 1
        padx = grid_on['padx'] if 'padx' in grid_on.keys() else 0
        pady = grid_on['pady'] if 'pady' in grid_on.keys() else 0
        
        self.grid(row=row, column=column, columnspan=columnspan, padx=padx, pady=pady)


    def input_clear(self):
        self.input_new_item.delete(0,'end')
    
