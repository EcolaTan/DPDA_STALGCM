import tkinter as tk
import threading
import time
from os.path import abspath
from tkinter import filedialog
from model import PDA, State, Transition
import customtkinter as ctk

def open_txt_file():
    
    filename = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    global pda
    pda = PDA()

    if filename:
        reset_pda()
        entry.delete(0, tk.END)
        update_stack_display()
        
        with open(filename, 'r') as file:

            num_states = int(file.readline().strip())

            if num_states > 0:
                states = file.readline().strip().split()

            num_inputs = int(file.readline().strip())

            inputs = ""

            if num_inputs > 0:
                inputs = file.readline().strip().split()

            stack_symbol = file.readline().strip()

            num_transitions = int(file.readline().strip())
            
            transitions = []
        
            for _ in range(num_transitions):
                transition = file.readline().strip().split()
                transitions.append(transition)

            start_state = file.readline().strip()

            num_of_final = int(file.readline().strip())

            if num_of_final > 0:
                final_states = file.readline().strip().split()

        for i in range(num_states):
            pda.states.append(State(i+1,states[i]))
            
        for i in inputs:
            pda.alphabet.append(i)

        pda.stack_symbol = stack_symbol
        
        for i in transitions:
            from_state = None
            to_state = None

            push_char = '' if i[4] == "lambda" else i[4]
            pop_char = '' if i[3] == "lambda" else i[3]

            for state in pda.states:
                if state.name == i[0]:
                    from_state = state
                if state.name == i[1]:
                    to_state = state
            from_state.transitions.append(Transition(from_state, to_state, i[2], pop_char, push_char))

        for state in pda.states:
            if state.name == start_state:
                pda.start_state = state
                pda.current_state = state

        for i in final_states:
            for state in pda.states:
                if i == state.name:
                    state.is_final = True
        update_queue()
        
def update_info_display():
    global pda
    try:
        if pda is not None:
            current_state_entry.configure(text=pda.current_state.name if pda.current_state else "N/A")
            steps_made_entry.configure(text=pda.step)
    except NameError:
        pass

def update_queue():
    global pda
    try:
        queue_entry.configure(text = entry.get()[pda.idx::])
    except NameError:
        pass

def update_queue_amogus(idx):
    global pda
    try:
        queue_entry.configure(text = entry.get()[idx::])
    except NameError:
        pass

def update_stack_display():
    global pda
    stack_listbox.delete(0, tk.END)
    for item in reversed(pda.stack):
        width = 20 
        centered_item = item.center(width)
        stack_listbox.insert(tk.END, centered_item)


def step_machine():
    global pda
    try:
        if pda is not None:
            pda.step = pda.step + 1
            input_string = entry.get() + "#"
            entry.configure(state='disabled')
            file_button.configure(state='disabled')
            if(pda.idx < len(input_string) and pda.possible):
                temp = pda.move_next_transition(input_string[pda.idx])
                pda.possible = True if temp == 1 or temp == 2 else False
                if(temp == 2):
                    pda.idx = pda.idx + 1
                update_stack_display()
                update_info_display()
                update_queue()
            else:
                accepted_entry.configure(text="YES" if pda.string_accepted() else "NO")
                accepted_entry.configure(fg_color="green" if pda.string_accepted() else "transparent")
                complete_button.configure(state='disabled')
                run_button.configure(state='disabled')
                file_button.configure(state='normal')
    except NameError:
        pass

def reset_pda():
    global pda

    try:
        if pda is not None:
            pda.current_state = pda.start_state
            pda.possible = True
            pda.stack = ["Z"]
            pda.idx = 0
            pda.step = 0
            update_stack_display()
            update_info_display()
            update_queue()
            entry.configure(state='normal')
            file_button.configure(state='normal')
            run_button.configure(state='normal')
            complete_button.configure(state='normal')
            accepted_entry.configure(text="NO")
            accepted_entry.configure(fg_color="transparent")
    except NameError:
        pass

def complete_steps():
    global pda
    try:
        if pda is not None:
            complete_button.configure(state='disabled')
            entry.configure(state='disabled')
            file_button.configure(state='disabled')
            run_button.configure(state='disabled')
            reset_button.configure(state='disabled')
            thread = threading.Thread(target=run_steps_thread)
            thread.start()
    except NameError:
        pass

def run_steps_thread():
    input_string = entry.get() + "#"
    run_step(input_string, pda.idx)

def run_step(input_string, idx):
    global pda
    
    while idx < len(entry.get() + "#") and pda.possible and pda.stack:
        step_machine()
        time.sleep(0.5)
    
    accepted_entry.configure(text="YES" if pda.string_accepted() else "NO")
    accepted_entry.configure(fg_color="green" if pda.string_accepted() else "transparent")
    file_button.configure(state='normal')
    reset_button.configure(state='normal')

root = ctk.CTk()
ctk.set_appearance_mode("dark")
root.title("One Way One Stack PDA")
root.geometry("600x700")
root.resizable(False, False) 

main_frame = ctk.CTkFrame(root, fg_color='transparent')
main_frame.pack(padx=20, pady=20)

stack_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
stack_frame.grid(row=0, column=0, padx=10)
stack_label = ctk.CTkLabel(stack_frame, text="Stack:", font=("Segoe UI", 14))
stack_label.pack(pady=5)

stack_listbox = tk.Listbox(stack_frame, width=20, height=20, font=("Courier New", 14), bd=0, bg="#343638", fg='white', highlightthickness=0)
stack_listbox.pack(pady=10)

info_frame = ctk.CTkFrame(main_frame, fg_color='transparent')
info_frame.grid(row=1, column=0, columnspan=2, pady=10)

right_frame = ctk.CTkFrame(main_frame, fg_color='transparent')
right_frame.grid(row=0, column=1, padx=10)

entry = ctk.CTkEntry(right_frame, placeholder_text="Input Text")
entry.grid(row=1, column=0, pady=10, padx=10)

file_button = ctk.CTkButton(right_frame, text="Open Text File", command=open_txt_file)
file_button.grid(row=2, column=0, pady=10, padx=10, sticky='ew')

run_button = ctk.CTkButton(right_frame, text="Go to Next Step", command=step_machine)
run_button.grid(row=3, column=0, pady=10, padx=10, sticky='ew')

complete_button = ctk.CTkButton(right_frame, text="Run the steps", command=complete_steps)
complete_button.grid(row=4, column=0, pady=10, padx=10, sticky='ew')

reset_button = ctk.CTkButton(right_frame, text="Reset string input", command=reset_pda)
reset_button.grid(row=5, column=0, pady=10, padx=10, sticky='ew')

current_state_label = ctk.CTkLabel(info_frame, text="Current State:", font=("Segoe UI", 14))
current_state_label.grid(row=1, column=0, pady=5, padx=5)

steps_made_label = ctk.CTkLabel(info_frame, text="Steps Made:", font=("Segoe UI", 14))
steps_made_label.grid(row=2, column=0, pady=5, padx=5)

accepted_label = ctk.CTkLabel(info_frame, text="Accepted:", font=("Segoe UI", 14))
accepted_label.grid(row=3, column=0, pady=5, padx=5)

queue_label = ctk.CTkLabel(info_frame, text="Queue:", font=("Segoe UI", 14))
queue_label.grid(row=0, column=0, pady=5, padx=5)

current_state_entry = ctk.CTkLabel(info_frame, text="", width=120, font=("Courier New", 14))
current_state_entry.grid(row=1, column=1, pady=5, padx=5)

steps_made_entry = ctk.CTkLabel(info_frame, text="", width=120, font=("Courier New", 14))
steps_made_entry.grid(row=2, column=1, pady=5, padx=5)

accepted_entry = ctk.CTkLabel(info_frame, text="", width=120, font=("Courier New", 14))
accepted_entry.grid(row=3, column=1, pady=5, padx=5)

queue_entry = ctk.CTkLabel(info_frame, text="", width=120, font=("Courier New", 14))
queue_entry.grid(row=0, column=1, pady=5, padx=5)

right_frame.columnconfigure(0, weight=1)

main_frame.columnconfigure(0, weight=1)

root.mainloop()