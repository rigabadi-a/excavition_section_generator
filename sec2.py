import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import openpyxl
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pathlib import Path


def draw_inverted_trapezoid_subplot(ax, B1, B2, h, GL_height, FL_height, title):
    """
    Draw an inverted trapezoid with dynamic geometry so the plotted shape
    reflects the real proportions of width and height.
    """
    # Trapezoid geometry
    top_left = (B2 - B1) / 2
    top_right = B2 - top_left
    x = [top_left, top_right, B2, 0]
    y = [h, h, 0, 0]

    ax.fill(x, y, color='lightgreen', edgecolor='black', linewidth=1.2)

    # Dynamic offsets based on actual geometry
    base_dim = max(B2, h)
    offset = base_dim * 0.08
    text_offset = base_dim * 0.04

    # Bottom width dimension
    ax.annotate(
        '',
        xy=(0, -offset),
        xytext=(B2, -offset),
        arrowprops=dict(arrowstyle='<->', color='blue', lw=1),
        annotation_clip=False
    )
    ax.text(
        B2 / 2,
        -offset - text_offset,
        f'Bottom Width = {B2:.2f}',
        ha='center',
        va='top',
        color='blue',
        fontsize=9
    )

    # Top width dimension
    ax.annotate(
        '',
        xy=(top_left, h),
        xytext=(top_right, h),
        arrowprops=dict(arrowstyle='<->', color='red', lw=1),
        annotation_clip=False
    )
    ax.text(
        B2 / 2,
        h + text_offset,
        f'Top Width = {B1:.2f}',
        ha='center',
        va='bottom',
        color='red',
        fontsize=9
    )

    # Green height arrow aligned with top-left corner
    green_gap = base_dim * 0.12
    green_text_gap = base_dim * 0.04
    green_arrow_x = top_left - green_gap
    green_text_x = green_arrow_x - green_text_gap

    ax.annotate(
        '',
        xy=(green_arrow_x, 0),
        xytext=(green_arrow_x, h),
        arrowprops=dict(arrowstyle='<->', color='green', lw=1.2),
        annotation_clip=False
    )
    ax.text(
        green_text_x,
        h / 2,
        f'Height = {h:.2f}',
        ha='right',
        va='center',
        rotation=90,
        color='green',
        fontsize=9
    )

    # Defaults for dynamic limits
    right_x = B2
    orange_arrow_x = B2 + offset
    left_x = top_left
    y_pos = h

    # Width at 2m from top
    if h > 2:
        distance_from_top = 2
        width_at_2m = B1 + (B2 - B1) * (distance_from_top / h)
        y_pos = h - distance_from_top

        left_x = (B2 - width_at_2m) / 2
        right_x = B2 - left_x

        ax.annotate(
            '',
            xy=(left_x, y_pos),
            xytext=(right_x, y_pos),
            arrowprops=dict(arrowstyle='<->', color='purple', lw=1),
            annotation_clip=False
        )
        ax.text(
            B2 / 2,
            y_pos + text_offset,
            f'Width at 2m = {width_at_2m:.2f}',
            ha='center',
            va='bottom',
            color='purple',
            fontsize=9
        )

        height_from_bottom_to_2m = h - distance_from_top
        orange_arrow_x = right_x + offset

        ax.annotate(
            '',
            xy=(orange_arrow_x, 0),
            xytext=(orange_arrow_x, y_pos),
            arrowprops=dict(arrowstyle='<->', color='orange', lw=1),
            annotation_clip=False
        )
        ax.text(
            orange_arrow_x + text_offset,
            y_pos / 2,
            f'Height = {height_from_bottom_to_2m:.2f}',
            ha='left',
            va='center',
            rotation=90,
            color='orange',
            fontsize=9
        )

    # GL label on the RIGHT side
    gl_line_x0 = top_right
    gl_line_x1 = top_right + 0.9 * offset
    ax.plot([gl_line_x0, gl_line_x1], [h, h], color='black', lw=1)
    ax.text(
        gl_line_x1 + 0.15 * offset,
        h,
        f'GL = {float(GL_height):.2f}',
        ha='left',
        va='center',
        color='black',
        fontsize=9
    )

    # FL label on the LEFT side
    fl_y_offset = text_offset * 0.8
    fl_line_x1 = 0
    fl_line_x0 = -0.9 * offset
    ax.plot([fl_line_x0, fl_line_x1], [fl_y_offset, fl_y_offset], color='black', lw=1)
    ax.text(
        fl_line_x0 - 0.15 * offset,
        fl_y_offset,
        f'FL = {float(FL_height):.2f}',
        ha='right',
        va='center',
        color='black',
        fontsize=9
    )

    # Title
    ax.set_title(str(title), y=1.06, fontsize=11)

    # Keep true geometric proportions
    ax.set_aspect('equal', adjustable='box')

    # Dynamic margins from geometry and annotation anchor points
    x_points = [
        0, B2, top_left, top_right,
        green_arrow_x, green_text_x,
        left_x, right_x,
        orange_arrow_x, orange_arrow_x + text_offset,
        gl_line_x0, gl_line_x1,
        fl_line_x0, fl_line_x1
    ]
    y_points = [
        0, h, -offset,
        h + text_offset,
        fl_y_offset,
        y_pos, y_pos + text_offset
    ]

    x_min = min(x_points)
    x_max = max(x_points)
    y_min = min(y_points)
    y_max = max(y_points)

    x_span = x_max - x_min
    y_span = y_max - y_min

    x_margin = max(0.30, 0.10 * x_span)
    y_margin = max(0.30, 0.12 * y_span)

    ax.set_xlim(x_min - x_margin, x_max + x_margin)
    ax.set_ylim(y_min - y_margin, y_max + y_margin)

    ax.axis('off')


def draw_inverted_trapezoid_grid(df, pdf_filename):
    required_cols = ['B1', 'B2', 'h', 'Title', 'GL', 'FL']
    missing = [col for col in required_cols if col not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    total_graphs = len(df)
    graphs_per_page = 9
    num_pages = (total_graphs + graphs_per_page - 1) // graphs_per_page

    with PdfPages(pdf_filename) as pdf:
        for page in range(num_pages):
            fig, axs = plt.subplots(3, 3, figsize=(11.69, 8.27))
            axs = axs.flatten()

            start_index = page * graphs_per_page
            end_index = min(start_index + graphs_per_page, total_graphs)
            df_subset = df.iloc[start_index:end_index]

            for ax, (_, row) in zip(axs, df_subset.iterrows()):
                try:
                    B1 = float(row['B2'])
                    B2 = float(row['B1'])
                    h = float(row['h'])
                    title = str(row['Title'])
                    GL_height = row['GL']
                    FL_height = row['FL']

                    if B1 <= 0 or B2 <= 0 or h <= 0:
                        ax.text(0.5, 0.5, 'Invalid dimensions', ha='center', va='center')
                        ax.axis('off')
                        continue

                    draw_inverted_trapezoid_subplot(ax, B1, B2, h, GL_height, FL_height, title)

                except Exception as e:
                    ax.text(0.5, 0.5, f'Row error:\n{e}', ha='center', va='center', fontsize=9)
                    ax.axis('off')

            for ax in axs[len(df_subset):]:
                ax.axis('off')

            plt.tight_layout(rect=[0, 0.04, 1, 0.97])

            fig.text(
                0.98,
                0.02,
                f'Page {page + 1} of {num_pages}',
                ha='right',
                va='bottom',
                fontsize=10
            )

            pdf.savefig(fig)
            plt.close(fig)


class TrapezoidApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Trapezoid PDF Generator")
        self.root.geometry("600x250")
        self.root.resizable(False, False)

        # Variables to store file paths
        self.input_file_var = tk.StringVar()
        self.output_file_var = tk.StringVar()

        self.create_widgets()

    def create_widgets(self):
        # Create a main frame for padding
        main_frame = ttk.Frame(self.root, padding="20 20 20 20")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # --- Input File Section ---
        ttk.Label(main_frame, text="Select Excel File:", font=("Segoe UI", 10, "bold")).grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        
        self.input_entry = ttk.Entry(main_frame, textvariable=self.input_file_var, width=50, state="readonly")
        self.input_entry.grid(row=1, column=0, sticky=tk.W, padx=(0, 10))
        
        ttk.Button(main_frame, text="Browse...", command=self.browse_input).grid(row=1, column=1)

        # --- Output File Section ---
        ttk.Label(main_frame, text="Save PDF As:", font=("Segoe UI", 10, "bold")).grid(row=2, column=0, sticky=tk.W, pady=(15, 5))
        
        self.output_entry = ttk.Entry(main_frame, textvariable=self.output_file_var, width=50, state="readonly")
        self.output_entry.grid(row=3, column=0, sticky=tk.W, padx=(0, 10))
        
        ttk.Button(main_frame, text="Browse...", command=self.browse_output).grid(row=3, column=1)

        # --- Action Buttons ---
        self.generate_btn = ttk.Button(main_frame, text="Generate PDF", command=self.process_files, style="Accent.TButton")
        self.generate_btn.grid(row=4, column=0, columnspan=2, pady=(25, 0), ipadx=20, ipady=5)

        # Style tweaking for the generate button to make it pop
        style = ttk.Style()
        style.configure("Accent.TButton", font=("Segoe UI", 10, "bold"))

    def browse_input(self):
        filename = filedialog.askopenfilename(
            title="Select Excel file",
            filetypes=[("Excel files", "*.xlsx *.xls"), ("All files", "*.*")]
        )
        if filename:
            self.input_file_var.set(filename)
            
            # Automatically suggest an output file name to save the user time
            input_path = Path(filename)
            suggested_output = input_path.parent / f"{input_path.stem}_trapezoids.pdf"
            self.output_file_var.set(str(suggested_output))

    def browse_output(self):
        # Default to the current output file path if one exists
        initial_file = ""
        initial_dir = ""
        if self.output_file_var.get():
            current_path = Path(self.output_file_var.get())
            initial_file = current_path.name
            initial_dir = current_path.parent

        filename = filedialog.asksaveasfilename(
            title="Save PDF as",
            defaultextension=".pdf",
            initialdir=initial_dir,
            initialfile=initial_file,
            filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")]
        )
        if filename:
            self.output_file_var.set(filename)

    def process_files(self):
        input_file = self.input_file_var.get()
        output_file = self.output_file_var.get()

        # Validation
        if not input_file:
            messagebox.showwarning("Missing Information", "Please select an input Excel file.")
            return
        if not output_file:
            messagebox.showwarning("Missing Information", "Please choose a save location for the PDF.")
            return

        input_path = Path(input_file)
        output_path = Path(output_file)

        # Create parent directories if they don't exist
        output_path.parent.mkdir(parents=True, exist_ok=True)

        # Change button state to indicate processing
        self.generate_btn.config(text="Processing...", state=tk.DISABLED)
        self.root.update() # Force UI update before heavy processing

        try:
            df = pd.read_excel(input_path, engine="openpyxl")
            draw_inverted_trapezoid_grid(df, output_path)
            messagebox.showinfo("Success", f"PDF generated successfully!\n\nSaved to: {output_path}")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while generating the PDF:\n\n{str(e)}")
        finally:
            # Re-enable the button
            self.generate_btn.config(text="Generate PDF", state=tk.NORMAL)


if __name__ == "__main__":
    root = tk.Tk()
    
    # Optional: If you want slightly sharper fonts on Windows
    try:
        from ctypes import windll
        windll.shcore.SetProcessDpiAwareness(1)
    except:
        pass
    
    app = TrapezoidApp(root)
    root.mainloop()