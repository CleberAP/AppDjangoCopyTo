# -*- ISO-8859-1 -*-
# project: App DjangoCopyTo
# file: main.py
#
# Created by Cleber Almeida Pereira
# e-mail: cleber.ap.desenvolvedor@gmail.com
#
# programming language: Python v3.10.2

from multiprocessing import Queue
from PIL import ImageTk, Image
from table_simple import SimpleTable, SimpleTableNavigationToolbar, SimpleTableInputField
from tkinter import font
from tkinter import ttk
import os
import re
import shutil
import sys
import threading
import time
import tkinter as tk
import tkinter.filedialog as  fdlg
import tkinter.messagebox as tkmsg
import tkinter.scrolledtext as tkst

class my_App:
    def __init__(self, **kw):
        self.root = tk.Tk()
        self.root.title('App DjangoCopyTo')
        self.root.geometry('%dx%d+%d+%d'%(800,600,0,0))
        self.root.configure(background='light grey')
        self.root.resizable(width=False, height=False)
        self.root.iconbitmap("images\image001.ico")

        self.config_dict = {}
        self.charge_config_dict()

        self.create_list_blocked_items()

        self.add_text = Image.open(os.getcwd()+'/images/add_line.png')
        self.add_text = self.add_text.resize((15,15))
        self.add_text = ImageTk.PhotoImage(self.add_text)

        self.launch_jan_lbi()

        self.create_area()

        self.charge_configs()

        self.check_list_blocked_items()
        
        #gripObj = ttk.Sizegrip(self.root)
        #gripObj.pack(side= 'right', anchor= 'se')

    def execute(self):
        self.root.mainloop()

    def end_app(self):
        self.root.quit()

    def create_area(self):
        self.mainframe = ttk.Frame(master=self.root)
        #self.mainframe.pack(side='top', fill='both', expand=1, anchor='w')

        self.mainframe.grid(row=1, column=0, sticky='ns')

        # Frame Top - Configurations
        self.frm_top = tk.LabelFrame(self.mainframe, text="Configurações", bg='light grey')
        self.frm_top.grid(row=0, column=0, columnspan=3, stick='we', padx=5, pady=5)

        # Frame LEFT (Origin path)
        self.frm_left = tk.Frame(self.mainframe, borderwidth=1, relief="groove", bg='light grey')
        self.frm_left.grid(row=1, column=0, columnspan=2, padx=(5,11), sticky='ns')
        
        # Frame RIGHT (Destiny path)
        self.frm_right = tk.Frame(self.mainframe, borderwidth=1, relief="groove", bg='light grey')
        self.frm_right.grid(row=1, column=2, columnspan=3, padx=(11,5), sticky='ns')

        # Frame BOTTOM
        self.frm_bottom = tk.Frame(self.mainframe, bg='light grey')
        self.frm_bottom.grid(row=2, column=0, columnspan=5, stick='we', padx=5, pady=(5,0))

        # Frame Top - Configurations >> Radios
        self.configuration_1 = tk.StringVar()
        self.configuration_1.set(None)
        self.configuration_2 = tk.StringVar()
        self.configuration_2.set(None)
        self.configuration_3 = tk.StringVar()
        self.configuration_3.set(None)
        self.configuration_4 = tk.StringVar()
        self.configuration_4.set(None)
        self.configuration_5 = tk.StringVar()
        self.configuration_5.set(None)
        
        self.chkbtn_1 = tk.Checkbutton(self.frm_top, bg='light grey', text="Create Folder",
                                       variable=self.configuration_1,
                                       onvalue="create_folder",
                                       offvalue='None',
                                       command=self.clicked_create_folder
                                       ).grid(row=0, column=0, columnspan=2, stick='w')
        self.chkbtn_5 = tk.Checkbutton(self.frm_top, bg='light grey', text="É Git Clone",
                                       variable=self.configuration_5,
                                       onvalue="is_git_clone",
                                       offvalue='None',
                                       #command=self.clicked_is_git_clone
                                       ).grid(row=0, column=2, columnspan=2, stick='w')
        self.lbl_copy = tk.Label(self.frm_top, bg='light grey', text="Copiar:",
                                 font=font.Font(size=10, weight='bold')
                                 ).grid(row=1, column=0)
        self.chkbtn_2 = tk.Checkbutton(self.frm_top, bg='light grey', text="migrations",
                                       variable=self.configuration_2,
                                       onvalue="migrations",
                                       offvalue='None',
                                       command=self.clicked_migrations
                                       ).grid(row=1, column=1)
        self.chkbtn_3 = tk.Checkbutton(self.frm_top, bg='light grey', text="migrations only init",
                                       variable=self.configuration_3,
                                       onvalue="migrations_only_init",
                                       offvalue='None',
                                       command=self.clicked_migrations_only_init
                                       ).grid(row=1, column=2)
        self.chkbtn_4 = tk.Checkbutton(self.frm_top, bg='light grey', text="static",
                                       variable=self.configuration_4,
                                       onvalue="static",
                                       offvalue='None',
                                       command=self.clicked_static
                                       ).grid(row=1, column=3)

        self.btn_other_items = tk.Button(self.mainframe, bg='light grey',
                                         text="Items para NÃO copiar",
                                         cursor='hand2',
                                         borderwidth=1,
                                         activebackground='grey',
                                         font=font.Font(size=10, weight='bold'),
                                         command=self.show_list_blocked_items)
        self.btn_other_items.grid(row=0, column=3, padx=5, pady=5, sticky='we')

        # Button COPY
        self.btn_copy = tk.Button(self.mainframe, bg='light grey',
                                  text="Copiar",
                                  cursor="hand2",
                                  borderwidth=2,
                                  activebackground='grey',
                                  font=font.Font(size=14, weight='bold'),
                                  command=self.copy)
        self.btn_copy.grid(row=0, column=4, padx=5, pady=5, sticky='we')

        # Frame LEFT >> Origem
        self.btn_orig_path = tk.Button(self.frm_left,
                                        text='Obter diretório do projeto Django',
                                        cursor='hand2',
                                        bg='light grey',
                                        borderwidth=0,
                                        activebackground='grey',
                                        font=font.Font(size=9, weight='bold', slant='italic'),
                                        command=self.get_origin_path)
        self.btn_orig_path.grid(row=0, column=0, columnspan=2, sticky='we', padx=5, pady=5)

        self.lbl_origin_path = tk.Label(self.frm_left, text='Diretório de origem:', font=font.Font(size=10, weight='bold'), bg='light grey')
        self.lbl_origin_path.grid(row=1, column=0, padx=5, pady=5)
        
        self.input_origin_path = tkst.ScrolledText(self.frm_left,
                                                   font=font.Font(size=10, weight='normal'),
                                                   width=50,
                                                   height=3,
                                                   wrap='word',
                                                   background='light grey',
                                                   #state='disabled'
                                                   )
        self.input_origin_path.grid(row=2, column=0, padx=5, pady=5)
        

        # Frame RIGHT >> Destino
        self.btn_destiny_path = tk.Button(self.frm_right,
                                        text='Obter diretório de destino do projeto Django',
                                        cursor='hand2',
                                        bg='light grey',
                                        borderwidth=0,
                                        activebackground='grey',
                                        font=font.Font(size=9, weight='bold', slant='italic'),
                                        command=self.get_destiny_path )
        self.btn_destiny_path.grid(row=0, column=0, columnspan=2, sticky='we', padx=5, pady=5)
        
        self.lbl_destiny_path = tk.Label(self.frm_right, text='Diretório de destino:', font=font.Font(size=10, weight='bold'), bg='light grey')
        self.lbl_destiny_path.grid(row=1, column=0, padx=5, pady=5)
        
        self.input_destiny_path = tkst.ScrolledText(self.frm_right,
                                                    font=font.Font(size=10, weight='normal'),
                                                    width=50,
                                                    height=3,
                                                    wrap='word',
                                                    background='light grey',
                                                    #state='disabled'
                                                    )
        self.input_destiny_path.grid(row=2, column=0, padx=5, pady=5)


        # Frame BOTTOM >> Footer
        lbl_footer_1 = tk.Label(self.frm_bottom, bg='black', fg='white',
                                text='Produzido por Cleber Almeida Pereira'
                                )
        #lbl_footer_1.grid(row=0, column=0, padx=5, pady=(5,0), sticky='we')
        lbl_footer_1.pack(fill='both', expand=True, padx=5, pady=(5,0))
        
        lbl_footer_2 = tk.Label(self.frm_bottom, bg='black', fg='white',
                                text='+55 (67) 9 9607-6081 WhatsApp'
                                )
        #lbl_footer_2.grid(row=1, column=0, padx=5, pady=(0,0), sticky='we')
        lbl_footer_2.pack(fill='both', expand=True, padx=5, pady=(0,0))

        lbl_footer_3 = tk.Label(self.frm_bottom, bg='black', fg='white',
                                text='cleber.almeidapereira@gmail.com'
                                )
        #lbl_footer_3.grid(row=1, column=2, padx=5, pady=(0,5), sticky='we')
        lbl_footer_3.pack(fill='both', expand=True, padx=5, pady=(0,5))

    def charge_config_dict(self):
        file = open('config.txt', 'r')
        lines = file.readlines()
        file.close()

        for line in lines:
            record = line.strip().split(':::')
            # Verifica se é lista
            if record[1].find(',') > -1:
                self.config_dict[record[0]] = [item.strip() for item in record[1].split(',')]
            else:
                self.config_dict[record[0]] = record[1]
    
    def charge_configs(self):
        if 'origin_dir' in self.config_dict.keys():
            self.charge_input_origin_dir()
        if 'destiny_dir' in self.config_dict.keys():
            self.charge_input_destiny_dir()
        
    def charge_input_origin_dir(self):
        orig_path = self.config_dict['origin_dir']
        #self.input_origin_path['state'] = 'normal'
        self.input_origin_path.delete("0.0", "end")
        self.input_origin_path.insert("1.0", orig_path)
        #self.input_origin_path['state'] = 'disabled'
        
    def charge_input_destiny_dir(self):
        destiny_path = self.config_dict['destiny_dir']
        #self.input_destiny_path['state'] = 'normal'
        self.input_destiny_path.delete("0.0", "end")
        self.input_destiny_path.insert("1.0", destiny_path)
        #self.input_destiny_path['state'] = 'disabled'

    def create_list_blocked_items(self):
        self.LIST_BLOCKED_ITEMS = ['__pycache__']    # Lista de itens bloqueados para cópia. Inclui nome completo de pastas ou de arquivos

        if 'list_blocked_items' in self.config_dict.keys():
            self.LIST_BLOCKED_ITEMS = self.config_dict['list_blocked_items']

    def add_item_of_list_blocked_items(self, item):
        if not item in self.LIST_BLOCKED_ITEMS:
            self.LIST_BLOCKED_ITEMS.append(item)

    def remove_item_of_list_blocked_items(self, item):
        if item in self.LIST_BLOCKED_ITEMS:
            self.LIST_BLOCKED_ITEMS.remove(item)

    def clicked_create_folder(self):
        destiny_path = self.input_destiny_path.get("1.0", "end").strip().split('\\')
        # verifica se o nome do projeto já consta no nome de destino
        project_name = self.input_origin_path.get("1.0", "end").strip().split('\\')[-1]
        if not project_name in destiny_path:
            new_destiny_path = os.path.join(self.input_destiny_path.get("1.0", "end").strip(), project_name)
            self.input_destiny_path.delete("0.0", "end")
            self.input_destiny_path.insert("1.0", new_destiny_path)

    def clicked_is_git_clone(self):
        if self.configuration_5.get() == 'is_git_clone':
            self.CONFIGURATIONS.append(self.configuration_5.get())
        else:
            if 'is_git_clone' in self.CONFIGURATIONS:
                self.CONFIGURATIONS.remove('is_git_clone')

    def clicked_migrations(self):
        if self.configuration_3.get() != None: # desabilita migration_only_init
            self.configuration_3.set(None)

        # itera na lista self.LIST_BLOCKED_ITEMS para adicionar ou remover item 'migrations'
        if self.configuration_2.get() == 'migrations' and self.configuration_3.get() == 'None':
            self.remove_item_of_list_blocked_items('migrations')
        elif self.configuration_2.get() == 'None' and self.configuration_3.get() == 'None':
            self.add_item_of_list_blocked_items('migrations')
        
    def clicked_migrations_only_init(self):
        if self.configuration_2.get() != None: # desabilita migration
            self.configuration_2.set(None)

        # itera na lista self.LIST_BLOCKED_ITEMS para adicionar ou remover item 'migrations'
        if self.configuration_3.get() == 'migrations_only_init' and self.configuration_2.get() == 'None':
            self.remove_item_of_list_blocked_items('migrations')
        elif self.configuration_2.get() == 'None' and self.configuration_3.get() == 'None':
            self.add_item_of_list_blocked_items('migrations')

    def clicked_static(self):
        # itera na lista self.LIST_BLOCKED_ITEMS para adicionar ou remover item 'static'
        if self.configuration_4.get() == 'static':
            self.remove_item_of_list_blocked_items('static')
        else:
            self.add_item_of_list_blocked_items('static')
        
    def set_configurations(self):
        self.CONFIGURATIONS = []

        if self.configuration_1.get() != 'None':
            self.CONFIGURATIONS.append(self.configuration_1.get())
        if self.configuration_2.get() != 'None':
            self.CONFIGURATIONS.append(self.configuration_2.get())
        if self.configuration_3.get() != 'None':
            self.CONFIGURATIONS.append(self.configuration_3.get())
        if self.configuration_4.get() != 'None':
            self.CONFIGURATIONS.append(self.configuration_4.get())
        if self.configuration_5.get() != 'None':
            self.CONFIGURATIONS.append(self.configuration_5.get())

    def check_list_blocked_items(self):
        # Verifica lista no carregamento da aplicação

        if self.configuration_2.get() == 'None' and self.configuration_3.get() == 'None':
            self.add_item_of_list_blocked_items('migrations')
            
        if self.configuration_4.get() == 'None':
            self.add_item_of_list_blocked_items('static')

    def get_origin_path(self):
        orig_path = fdlg.askdirectory()     # "Caminho Original"
        #self.input_origin_path['state'] = 'normal'
        self.input_origin_path.delete("0.0", "end")
        self.input_origin_path.insert("1.0", orig_path)
        #self.input_origin_path['state'] = 'disabled'

    def get_destiny_path(self):
        destiny_path = fdlg.askdirectory()  # "Caminho de Destino"
        #self.input_destiny_path['state'] = 'normal'
        self.input_destiny_path.delete("0.0", "end")
        self.input_destiny_path.insert("1.0", destiny_path)
        #self.input_destiny_path['state'] = 'disabled'


    def launch_jan_lbi(self):

        self.jan_lbi = tk.Toplevel()
        self.jan_lbi.wm_title("Lista de itens desconsiderados para cópia")
        self.jan_lbi.geometry('%dx%d+%d+%d'%(422,573,801,0))
        #self.jan_lbi.overrideredirect(True) # Esconde a toolbar mas possibilita o uso do comando [ALT + F4]
        self.jan_lbi.protocol("WM_DELETE_WINDOW", self.jan_lbi_disable_event)
        self.jan_lbi.iconbitmap("images\image001.ico")
        
        self.btn_close_jan_lbi = tk.Button(self.jan_lbi,
                                           text="Fechar",
                                           cursor='hand2',
                                           activebackground='red',
                                           font=font.Font(size=10, weight='bold'),
                                           command=self.jan_lbi_hide
                                           )
        self.btn_close_jan_lbi.grid(row=0, column=0, columnspan=4, padx=5, pady=(5,10), stick='we')

        """
        self.input_new_item = tk.Entry(self.jan_lbi)
        self.input_new_item.grid(row=1, column=0, columnspan=3, padx=(10,0), pady=5, stick='we')

        self.btn_add_new_item = tk.Button(self.jan_lbi,
                                          text='',
                                          cursor='hand2',
                                          image=self.add_text,
                                          compound='top',
                                          font=font.Font(size=11, weight='bold'),
                                          command=self.add_item_lbi
                                          )
        self.btn_add_new_item.grid(row=1, column=3, padx=5, pady=5)
        """
        
        # Frame Read Files >> Tabela para Ordenar itens (entidades/tabelas), remover desnecessários e restaurar lista original
        self.table = SimpleTable(self.jan_lbi,
                                 self.LIST_BLOCKED_ITEMS,
                                 grid_on={'row':3, 'column':0, 'columnspan':4, 'padx':5, 'pady':0},
                                 max_rows=18,
                                 stripped=[True],
                                 select_mode="extended",
                                 column_name="Entidades/Tabelas",
                                 inplace_list=True
                                 )

        self.TableInputField = SimpleTableInputField(self.jan_lbi,
                                                     self.table,
                                                     grid_on={'row':1, 'column':0, 'columnspan':4, 'padx':5, 'pady':5}
                                                     )                                                       

        # Frame Read Files >> Barra de Navegação da Tabela
        self.TableNavToolbar = SimpleTableNavigationToolbar(self.jan_lbi,
                                                            self.table,
                                                            grid_on={'row':2, 'column':0, 'columnspan':4, 'padx':5, 'pady':5}
                                                            )

        # Teste de verificação de tamanho da janela
        #print('width:', self.jan_lbi.winfo_screenwidth())
        #print('height:', self.jan_lbi.winfo_screenheight())
        #print('Toplevel:', self.jan_lbi.winfo_toplevel())
        #self.jan_lbi.update()
        #print('width:', self.jan_lbi.winfo_width())
        #print('height:', self.jan_lbi.winfo_height())
        
        self.jan_lbi.withdraw() # hide the window

    def jan_lbi_disable_event(self):
        # Evento para desabilitar a função Exit for [X] e usar outra opção para fechar (ex: button)
        pass

    def jan_lbi_hide(self):
        self.jan_lbi.withdraw()

    def show_list_blocked_items(self):
        self.jan_lbi.deiconify()    # show the window

    def add_item_lbi(self):
        new_item = self.input_new_item.get().strip()
        #print('len:', len(new_item))
        #print('texto:', new_item)
        #print(self.LIST_BLOCKED_ITEMS)

        if len(new_item) > 0:
            if not new_item in self.LIST_BLOCKED_ITEMS:
                self.LIST_BLOCKED_ITEMS.append(new_item)
                self.table.recharge_table(self.LIST_BLOCKED_ITEMS)
            else:
                tkmsg.showinfo('O item já está na lista')

            self.input_new_item.delete(0, 'end')

    def get_last_dir_on_path(self, path):
        return path.split("/")[-1]

    def regex_path(self, path):
        return re.sub(r'(\n|\t|\"|\')',lambda path:{'\n':'\\n','\t':'\\t','\'':'\\\'','\"':'\\\"'}[path.group()], path)

    def check_dir_exists(self, path):
        return os.path.exists(path)

    def check_and_create_dir(self, path):
        if not os.path.exists(path):
            os.mkdir(path)

    def delete_dir(self, path):
        #os.remove(path)
        try:
            shutil.rmtree(path)
            return True
        except Exception as err:
            if 'is_git_clone' in self.CONFIGURATIONS:
                for item in os.listdir(path):
                    if not item in self.config_dict['git_clone']:
                        if os.path.isdir(self.regex_path(os.path.join(path,item))):
                            shutil.rmtree(self.regex_path(os.path.join(path,item)))
                        else:
                            os.remove(self.regex_path(os.path.join(path,item)))
                return True
            else:
                tkmsg.showerror("ERRO", f"Não foi possível deletar pasta. \n\nErro: {err}")
                return False

    def check_dir_on_list_blocked(self, list_dirs):
        checked = True
        for dir_ in list_dirs:
            if dir_ in self.LIST_BLOCKED_ITEMS:
                #print(f"      {dir_}")
                checked = False
        return checked
                
    def copy(self):
        # 1. Verifica se os campos estão setados
        init_copy = True
        execute_copy = True
        origin_dir = self.input_origin_path.get("1.0", "end").strip()
        destiny_dir = self.input_destiny_path.get("1.0", "end").strip()

        
        if len(origin_dir) == 0 or len(destiny_dir) == 0:
            tkmsg.showwarning("Impossível!", "Não há diretório definido!\n\nVocê deve especificar ambos os diretórios de origem e de destino.")
            init_copy = False
        
        if init_copy:
            # 2. Setar configurações
            self.set_configurations()
            ##print("\nTestes")
            ##print(self.CONFIGURATIONS)
            ##print(self.config_dict)
            ##print("De:", origin_dir)
            ##print("Para:", destiny_dir)

            # 3. Verifica se precisa criar pasta no diretório de origem
            

            if not os.path.exists(destiny_dir):
                tkmsg.showinfo("Aviso",f"A pasta não existe no diretório informado! \n\nDir: {destiny_dir} \n\nPasta: {self.get_last_dir_on_path(origin_dir)}\n\nEntão será criada!")
                #destiny_dir = os.path.join(destiny_dir, self.get_last_dir_on_path(origin_dir))
                #os.mkdir(destiny_dir)
                self.check_and_create_dir(destiny_dir)
            else:
                execute_copy = False
                if tkmsg.askyesno("Não realizada!", f"A pasta já existe no diretório informado! \n\nDir: {destiny_dir} \n\nPasta: {self.get_last_dir_on_path(origin_dir)}\n\nA pasta atual será deletada e criada uma nova a fim de manter cópia igual à original.\n\nDeseja continuar?"):
                    execute_copy = True
                    if self.delete_dir(destiny_dir):
                        self.check_and_create_dir(destiny_dir)
                    else:
                        execute_copy = False
 

            if execute_copy:

                ##print("Dir de destino:", destiny_dir)

                ##print(f"\n{len(self.LIST_BLOCKED_ITEMS)} Arquivos NÃO copiar:", self.LIST_BLOCKED_ITEMS)

                # 4. Ler diretório de origem
                origin_dir_itens = os.listdir(origin_dir)

                # 5. Total de itens no diretório de origem
                total_items_on_origin_dir = len(origin_dir_itens)

                # 6. Itera no diretório de origem, cria as pastas se necessário, e cria a lista de diretórios (dicionário)
                dict_copy = {}
                for item in origin_dir_itens:
                    # Verifica se é diretório
                    if os.path.isdir(self.regex_path(os.path.join(origin_dir,item))):
                        ##print(item, 'é pasta')
                        if not item in self.LIST_BLOCKED_ITEMS:
                            for pastaA, subPastaA, arquivos in os.walk(os.path.join(origin_dir,item)):
                                list_itens = pastaA.split('\\')
                                ##print(f">> {item} em {list_itens}" )
                                if self.check_dir_on_list_blocked(list_itens):
                                    folder_name = pastaA.split(origin_dir)[-1].strip('\\')
                                    self.check_and_create_dir(os.path.join(destiny_dir,folder_name))
                                    ##print(f"p: {pastaA}\n    sub:{subPastaA}")
                                    ##print("        folder atual:", pastaA.split("\\")[-1])
                                    for arq in arquivos:
                                        ##print("        a:", arq)
                                        item_copy_origin = pastaA
                                        
                                        # Verifica se pasta é 'migrations' e 'migrations_only_init'
                                        check_if_copy_migrations = True
                                        if pastaA.split("\\")[-1] == 'migrations' and 'migrations_only_init' in self.CONFIGURATIONS:
                                            if arq.strip() == '__init__.py':
                                                item_copy_destiny = os.path.join(destiny_dir, folder_name)
                                                check_if_copy_migrations = True
                                            else:
                                                check_if_copy_migrations = None
                                        elif pastaA.split("\\")[-1] == 'migrations' and 'migrations_only_init' not in self.CONFIGURATIONS:
                                            item_copy_destiny = os.path.join(destiny_dir, folder_name)
                                        elif pastaA.split("\\")[-1] != 'migrations':
                                            item_copy_destiny = os.path.join(destiny_dir, folder_name)
                                            
                                        ##print("        >> Origem:", os.path.join(item_copy_origin, arq))
                                        ##print("        >>   Dest:", os.path.join(item_copy_destiny, arq))

                                        #os.popen(f'copy {item_copy_origin} {item_copy_destiny}')
                                        if check_if_copy_migrations:
                                            dict_copy[os.path.join(item_copy_origin, arq)] = os.path.join(item_copy_destiny, arq)
                                ##else:
                                ##         print("    BLOCKED")
                                        
                    else:
                        ##print(item, 'é arquivo')
                        if not item in self.LIST_BLOCKED_ITEMS:
                            ##print(" copiando...")
                            item_copy_origin = os.path.join(origin_dir,item)
                            item_copy_destiny = os.path.join(destiny_dir, item_copy_origin.split(origin_dir)[-1].strip('\\'))
                            ##print("        >>> Origem:", item_copy_origin)
                            ##print("        >>>   Dest:", item_copy_destiny)
                            #os.popen(f'copy {item_copy_origin} {item_copy_destiny}')
                            dict_copy[item_copy_origin] = item_copy_destiny
                            
                self.copy_execute(dict_copy)
                tkmsg.showinfo("FIM", "Processo finalizado")
            else:
                tkmsg.showinfo('Cancelado','O processo de cópia foi cancelado pelo usuário.')
                

    def copy_execute(self, dict_copy):
        for dir_orig, dir_dest in dict_copy.items():
            os.system(f'copy {dir_orig} {dir_dest}')
                    

    # Function to do 'stuff' and place object in queue for later #
    def foo(self):
        # sleep to demonstrate thread doing work #
        time.sleep(5)
        obj = [x for x in range(0,600)]
        self.queue.put(obj)
        #while self.thread1.is_alive():
        #    obj = [x for x in range(0,600)]
        #    self.queue.put(obj)
        #    obj = [x for x in range(600,0)]
        #    self.queue.put(obj)

    def progress(self, thread, queue):
        # starts thread #
        thread.start()
        
        # defines indeterminate progress bar (used while thread is alive)
        self.prog_bar = ttk.Progressbar(self.frm_bottom, orient='horizontal', length=600, mode='indeterminate')
        self.prog_bar.grid(row=0, column=1, sticky='we', padx=5, pady=(5,0))

        self.prog_bar.start()

        # checks whether thread is alive #
        while thread.is_alive():
            self.frm_bottom.update()
            pass

        # retrieves object from queue #
        work = queue.get()
        return work

    def start_progress_bar(self):
        self.queue = Queue()
        # Create thread object, targeting function to do 'stuff' #
        self.thread1 = threading.Thread(target=self.foo, args=())
        work = self.progress(self.thread1, self.queue)
        

def main(args):
    app_proc = my_App()
    app_proc.execute()
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
