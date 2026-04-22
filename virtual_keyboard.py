import tkinter as tk
import random

def get_password_via_vk(title="Nhập Mật Khẩu (Bàn phím ảo)"):
    """
    Displays a virtual QWERTY keyboard using Tkinter to input a password.
    Returns the entered password as a string.
    """
    password_result = ""
    
    # QWERTY layouts
    lower_layout = [
        ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '-', '='],
        ['q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', '[', ']'],
        ['a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', ';', "'", '\\'],
        ['z', 'x', 'c', 'v', 'b', 'n', 'm', ',', '.', '/']
    ]
    
    shift_layout = [
        ['!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '_', '+'],
        ['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P', '{', '}'],
        ['A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L', ':', '"', '|'],
        ['Z', 'X', 'C', 'V', 'B', 'N', 'M', '<', '>', '?']
    ]
    
    root = tk.Tk()
    root.title(title)
    root.geometry("750x450")
    root.resizable(False, False)
    root.attributes('-topmost', True) # Keep on top

    pwd_var = tk.StringVar()
    is_shifted = False
    is_shuffled = False
    
    # Frame for display
    display_frame = tk.Frame(root, pady=10)
    display_frame.pack(fill=tk.X)
    
    entry = tk.Entry(display_frame, textvariable=pwd_var, show="*", font=("Arial", 20), state='readonly', justify='center')
    entry.pack(fill=tk.X, padx=20)
    
    # Frame for keyboard
    kb_frame = tk.Frame(root)
    kb_frame.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)
    
    def on_key_press(char):
        pwd_var.set(pwd_var.get() + char)
        
    def on_backspace():
        current = pwd_var.get()
        if current:
            pwd_var.set(current[:-1])
            
    def on_clear():
        pwd_var.set("")
        
    def on_submit():
        nonlocal password_result
        password_result = pwd_var.get()
        root.destroy()
        
    def toggle_shift():
        nonlocal is_shifted
        is_shifted = not is_shifted
        render_keys()

    def toggle_shuffle():
        nonlocal is_shuffled
        is_shuffled = not is_shuffled
        render_keys()
        
    def render_keys():
        # Clear existing buttons
        for widget in kb_frame.winfo_children():
            widget.destroy()
            
        current_layout = shift_layout if is_shifted else lower_layout
        
        # Flatten layout for easier shuffling if needed
        flat_keys = []
        for row in current_layout:
            for key in row:
                flat_keys.append(key)
                
        if is_shuffled:
            random.shuffle(flat_keys)
            
        # Re-construct rows
        render_layout = []
        idx = 0
        for row in current_layout:
            new_row = []
            for _ in row:
                new_row.append(flat_keys[idx])
                idx += 1
            render_layout.append(new_row)
            
        for r_idx, row in enumerate(render_layout):
            row_frame = tk.Frame(kb_frame)
            row_frame.pack(pady=2)
            for c_idx, char in enumerate(row):
                btn = tk.Button(row_frame, text=char, width=4, height=2, font=("Arial", 12),
                                command=lambda c=char: on_key_press(c))
                btn.pack(side=tk.LEFT, padx=2)
                
        # Control buttons row
        control_frame = tk.Frame(kb_frame)
        control_frame.pack(pady=10)
        
        shift_text = "▼ Thường" if is_shifted else "▲ Shift"
        tk.Button(control_frame, text=shift_text, width=8, height=2, bg="lightgrey", font=("Arial", 10, "bold"),
                  command=toggle_shift).pack(side=tk.LEFT, padx=5)
                  
        tk.Button(control_frame, text="Xóa lùi", width=8, height=2, bg="orange", font=("Arial", 10, "bold"),
                  command=on_backspace).pack(side=tk.LEFT, padx=5)
        
        tk.Button(control_frame, text="Xóa hết", width=8, height=2, bg="red", fg="white", font=("Arial", 10, "bold"),
                  command=on_clear).pack(side=tk.LEFT, padx=5)
                  
        shuffle_text = "Sắp xếp: Trộn" if is_shuffled else "Sắp xếp: QWERTY"
        tk.Button(control_frame, text=shuffle_text, width=15, height=2, bg="lightblue", font=("Arial", 10, "bold"),
                  command=toggle_shuffle).pack(side=tk.LEFT, padx=5)
                  
        tk.Button(control_frame, text="Xác nhận", width=8, height=2, bg="green", fg="white", font=("Arial", 10, "bold"),
                  command=on_submit).pack(side=tk.LEFT, padx=5)

    render_keys() # Initial render
    
    root.mainloop()
    return password_result

if __name__ == "__main__":
    # Test the virtual keyboard
    pw = get_password_via_vk("Test")
    print("Entered:", pw)
