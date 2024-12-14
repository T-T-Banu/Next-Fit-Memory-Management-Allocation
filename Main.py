import tkinter as tk
from tkinter import messagebox

class MemoryAllocator:
    def __init__(self, master):
        self.master = master
        master.title("Next Fit Memory Allocation")

        
        self.memory_blocks = [50, 200, 150, 100, 300]
        self.initial_memory_blocks = self.memory_blocks.copy()
        self.last_allocated = -1  

       
        self.label = tk.Label(master, text="Next Fit Memory Allocation", font=("Arial", 16))
        self.label.pack(pady=10)

        self.memory_display = tk.Text(master, width=40, height=10, state="disabled", font=("Courier", 12))
        self.memory_display.pack(pady=10)

        self.process_input_label = tk.Label(master, text="Enter Process Size:")
        self.process_input_label.pack()

        self.process_input = tk.Entry(master)
        self.process_input.pack()

        self.add_process_button = tk.Button(master, text="Add Process", command=self.add_process)
        self.add_process_button.pack(pady=5)

        self.block_input_label = tk.Label(master, text="Enter Block Number to Deallocate:")
        self.block_input_label.pack()

        self.block_input = tk.Entry(master)
        self.block_input.pack()

        self.deallocate_button = tk.Button(master, text="Deallocate Memory", command=self.deallocate_memory)
        self.deallocate_button.pack(pady=5)

        self.reset_button = tk.Button(master, text="Reset", command=self.reset)
        self.reset_button.pack(pady=10)

      
        self.update_memory_display()

    def update_memory_display(self):
        """Updates the memory blocks display."""
        self.memory_display.config(state="normal")
        self.memory_display.delete("1.0", tk.END)
        for i, size in enumerate(self.memory_blocks):
            status = "Free" if size == self.initial_memory_blocks[i] else "Allocated"
            self.memory_display.insert(tk.END, f"Block {i}: {size} MB ({status})\n")
        self.memory_display.config(state="disabled")

    def add_process(self):
        """Allocates memory to a process using the Next Fit algorithm."""
        try:
            process_size = int(self.process_input.get())
            if process_size <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid positive process size.")
            return

        
        for i in range(len(self.memory_blocks)):
            index = (self.last_allocated + 1 + i) % len(self.memory_blocks)
            if self.memory_blocks[index] >= process_size:
                self.memory_blocks[index] -= process_size
                self.last_allocated = index
                messagebox.showinfo("Success", f"Process of {process_size} MB allocated to Block {index}.")
                self.update_memory_display()
                return

        
        messagebox.showerror("Error", f"Process of {process_size} MB could not be allocated.")
        self.update_memory_display()

    def deallocate_memory(self):
        """Deallocates memory for a specific block."""
        try:
            block_index = int(self.block_input.get())
            if block_index < 0 or block_index >= len(self.memory_blocks):
                raise IndexError
        except (ValueError, IndexError):
            messagebox.showerror("Error", "Please enter a valid block number.")
            return

        if self.memory_blocks[block_index] == self.initial_memory_blocks[block_index]:
            messagebox.showinfo("Info", f"Memory Block {block_index} is already free.")
        else:
            self.memory_blocks[block_index] = self.initial_memory_blocks[block_index]
            messagebox.showinfo("Success", f"Memory Block {block_index} has been deallocated.")

        self.update_memory_display()

    def reset(self):
        """Resets the memory allocation simulation."""
        self.memory_blocks = self.initial_memory_blocks.copy()
        self.last_allocated = -1
        self.update_memory_display()
        self.process_input.delete(0, tk.END)
        self.block_input.delete(0, tk.END)
        messagebox.showinfo("Success", "Memory allocation simulation has been reset.")

if __name__ == "__main__":
    root = tk.Tk()
    app = MemoryAllocator(root)
    root.mainloop()
