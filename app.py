import customtkinter as ctk 
import sqlite3

# Inicializando banco de dados
#ps criar pasta db se não existir na pasta raiz do projeto.

conn = sqlite3.connect("db/pessoas.db")
cur = conn.cursor()
cur.execute("""
    CREATE TABLE IF NOT EXISTS pessoas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR(255) NOT NULL
            )
 """)

conn.commit()


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Cadastro de Pessoas")
        self.geometry("800x600")

        #Widgets
        self.entry_name = ctk.CTkEntry(self, placeholder_text="Digite o nome")
        self.entry_name.pack(pady=10)

        self.button_add = ctk.CTkButton(self,text="&Adicionar",command=self.add_person)
        self.button_add.pack(pady=5)


        self.search_entry = ctk.CTkEntry(self,placeholder_text="Pesquisar")
        self.search_entry.pack(pady=10)
        self.search_entry.bind("<keyRekease>",lambda event: self.update_list())

        self.listbox = ctk.CTkTextbox(self,height=200)
        self.listbox.pack(pady=10,fill="both", expand=True)


        self.button_edit = ctk.CTkButton(self,text="Editar selecionado",command=self.edit_person)
        self.button_edit.pack(pady=5)

        self.button_delete = ctk.CTkButton(self,text='Excluir Selecionado',command=self.delete_person)
        self.button_delete.pack(pady=5)

        self.update_list()


    def add_person(self):
        name = self.entry_name.get().strip()
        if name:
            cur.execute("INSERT INTO pessoas (name) (?)",(name,))
            conn.commit()
            self.entry_name.delete(0,'end')
            self.update_list()
    
    def edit_person(self):
        selected_text = self.listbox.get('self.first','sel.last').strip()
        if selected_text:
            new_name = self.entry_name.get().strip()
            if new_name:
                cur.execute('UPDATE pessoas SET name = ?  where  name = ?',(new_name,selected_text ))
                conn.commit()
                self.update_list()
    
    def delete_person(self):
        selected_text = self.listbox.get('self.first', 'sel.last').strip()
        if selected_text:
            cur.execute('DELETE FROM pessoas WHERE name = ?',(selected_text,))
            conn.commit()
            self.update_list()

    def update_list(self):
        self.listbox.delete('0.0','end')
        search = self.search_entry.get().lower()
        cur.execute('SELECT name FROM pessoas')
        for (name,) in cur.fetchall():
            if search in name.lower():
                self.listbox.insert("end", name+'\n')




if __name__ == "__main__":
    ctk.set_appearance_mode("Dark") # Dark / Light / System
    ctk.set_default_color_theme("blue")
    app = App()
    app.mainloop()
    









