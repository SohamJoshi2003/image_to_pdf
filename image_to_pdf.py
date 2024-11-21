import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image
import os
import ttkbootstrap as ttk  # For enhanced styling

class ImageToPDFConverter:
    def __init__(self, root):
        self.root = root
        self.root.title("Image to PDF Converter")
        self.root.geometry("900x750")
        self.root.iconbitmap("")  # Add an icon file path here for branding
        self.style = ttk.Style("cosmo")  # Use a sleek theme
        
        # Store selected files as a list
        self.selected_files = []

        # Create UI components
        self.create_widgets()

    def create_widgets(self):
        # Title Label
        title_label = ttk.Label(
            self.root, 
            text="Image to PDF Converter", 
            font=("Helvetica", 18, "bold"),
            anchor="center"
        )
        title_label.pack(pady=10)

        # Button Frame for Selection Actions
        selection_frame = ttk.LabelFrame(self.root, text="File Selection", padding=10)
        selection_frame.pack(pady=10, fill=tk.X)

        # Select Images Button
        select_button = ttk.Button(
            selection_frame, 
            text="Select Images", 
            bootstyle="primary",
            command=self.select_images
        )
        select_button.pack(side=tk.LEFT, padx=10)

        # Select Folder Button
        select_folder_button = ttk.Button(
            selection_frame, 
            text="Select Folder", 
            bootstyle="primary",
            command=self.select_folder
        )
        select_folder_button.pack(side=tk.LEFT, padx=10)

        # Add More Photos Button
        add_photos_button = ttk.Button(
            selection_frame, 
            text="Add More Photos", 
            bootstyle="secondary",
            command=self.add_more_photos
        )
        add_photos_button.pack(side=tk.LEFT, padx=10)

        # Add More Folders Button
        add_folder_button = ttk.Button(
            selection_frame, 
            text="Add More Folders", 
            bootstyle="secondary",
            command=self.add_more_folders
        )
        add_folder_button.pack(side=tk.LEFT, padx=10)


        # Preview Area
        preview_frame = ttk.Frame(self.root, padding=10, bootstyle="secondary")
        preview_frame.pack(pady=15, expand=True, fill=tk.BOTH)

        preview_label = ttk.Label(preview_frame, text="Selected Files")
        preview_label.pack(anchor="w", pady=5)

        scrollbar = ttk.Scrollbar(preview_frame, orient=tk.VERTICAL)
        self.preview_listbox = tk.Listbox(
            preview_frame, 
            yscrollcommand=scrollbar.set, 
            width=60, 
            height=15, 
            selectmode=tk.SINGLE,
            highlightthickness=0,
            relief=tk.FLAT
        )
        scrollbar.config(command=self.preview_listbox.yview)
        self.preview_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Reordering Buttons Frame
        reorder_frame = ttk.LabelFrame(self.root, text="Reordering Operations", padding=10)
        reorder_frame.pack(pady=10, fill=tk.X)

        # Move Up Button
        move_up_button = ttk.Button(
            reorder_frame, 
            text="Move Up", 
            bootstyle="success",
            command=self.move_up
        )
        move_up_button.pack(side=tk.LEFT, padx=10)

        # Move Down Button
        move_down_button = ttk.Button(
            reorder_frame, 
            text="Move Down", 
            bootstyle="success",
            command=self.move_down
        )
        move_down_button.pack(side=tk.LEFT, padx=10)

        # Delete and Clear Selection Buttons Frame
        action_frame = ttk.LabelFrame(self.root, text="Action Buttons", padding=10)
        action_frame.pack(pady=10, fill=tk.X)

        # Delete Selected Photo Button
        delete_button = ttk.Button(
            action_frame, 
            text="Delete Selected Photo", 
            bootstyle="danger",
            command=self.delete_photo
        )
        delete_button.pack(side=tk.LEFT, padx=10)

        # Clear Selection Button
        clear_button = ttk.Button(
            action_frame, 
            text="Clear Selection", 
            bootstyle="danger",
            command=self.clear_selection
        )
        clear_button.pack(side=tk.LEFT, padx=10)

        # Convert to PDF Button
        convert_button = ttk.Button(
            self.root, 
            text="Convert to PDF", 
            bootstyle="primary-outline",
            command=self.convert_to_pdf
        )
        convert_button.pack(pady=20)


    def select_images(self):
        files = filedialog.askopenfilenames(
            filetypes=[
                ("Image Files", "*.png *.jpg *.jpeg *.bmp *.tiff *.gif"),
                ("All Files", "*.*")
            ],
            title="Select Images"
        )
        if files:
            self.add_files(files)

    def select_folder(self):
        folder = filedialog.askdirectory(title="Select Folder")
        if not folder:
            return
        valid_extensions = (".png", ".jpg", ".jpeg", ".bmp", ".tiff", ".gif")
        folder_images = [
            os.path.join(folder, file)
            for file in os.listdir(folder)
            if file.lower().endswith(valid_extensions)
        ]
        if not folder_images:
            messagebox.showwarning("No Images Found", "No valid image files were found in the selected folder.")
            return
        self.add_files(folder_images)

    def add_more_photos(self):
        self.select_images()

    def add_more_folders(self):
        self.select_folder()

    def add_files(self, files):
        for file in files:
            if file not in self.selected_files:
                self.selected_files.append(file)
        self.update_preview()

    def update_preview(self):
        self.preview_listbox.delete(0, tk.END)
        for file in self.selected_files:
            self.preview_listbox.insert(tk.END, os.path.basename(file))

    def move_up(self):
        selected_index = self.preview_listbox.curselection()
        if not selected_index or selected_index[0] == 0:
            return
        index = selected_index[0]
        self.selected_files[index], self.selected_files[index - 1] = (
            self.selected_files[index - 1], 
            self.selected_files[index]
        )
        self.update_preview()
        self.preview_listbox.select_set(index - 1)

    def move_down(self):
        selected_index = self.preview_listbox.curselection()
        if not selected_index or selected_index[0] == len(self.selected_files) - 1:
            return
        index = selected_index[0]
        self.selected_files[index], self.selected_files[index + 1] = (
            self.selected_files[index + 1], 
            self.selected_files[index]
        )
        self.update_preview()
        self.preview_listbox.select_set(index + 1)

    def delete_photo(self):
        selected_index = self.preview_listbox.curselection()
        if not selected_index:
            messagebox.showerror("Error", "No photo selected!")
            return
        index = selected_index[0]
        del self.selected_files[index]
        self.update_preview()

    def clear_selection(self):
        self.selected_files.clear()
        self.preview_listbox.delete(0, tk.END)

    def convert_to_pdf(self):
        if not self.selected_files:
            messagebox.showerror("Error", "No images selected!")
            return
        save_path = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF File", "*.pdf")],
            title="Save PDF As"
        )
        if not save_path:
            return
        try:
            images = [Image.open(file).convert("RGB") for file in self.selected_files]
            images[0].save(
                save_path, 
                save_all=True, 
                append_images=images[1:]
            )
            messagebox.showinfo("Success", f"PDF saved successfully to:\n{save_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to create PDF: {str(e)}")

# Main application launch
if __name__ == "__main__":
    root = ttk.Window(themename="cosmo")  # Use ttkbootstrap for better visuals
    app = ImageToPDFConverter(root)
    root.mainloop()

"""STANDARD_THEMES = {
    "cosmo": 
    "flatly": 
    "litera": 
    "minty": 
    "lumen": 
    "sandstone": 
    "yeti": 
    "pulse": 
    "united": 
    "journal": 
    "solar": 
    "simplex": 
    "cerculean": 
}
"""