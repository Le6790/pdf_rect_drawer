import io
import sys
import tkinter as tk
from os import wait

import fitz  # PyMuPDF
from PIL import Image, ImageTk

if sys.argv[1]:
    PDF_PATH = sys.argv[1]
else:
    PDF_PATH = "Formal_Business_Letter_Template30239.pdf"

TARGET_WIDTH = 800  # Resize width for display


def render_pdf_first_page(path, dpi=150):
    doc = fitz.open(path)
    page = doc.load_page(0)
    pix = page.get_pixmap(dpi=dpi)
    image = Image.open(io.BytesIO(pix.tobytes("png")))
    return image


def scale_image(image, target_width):
    w_percent = target_width / float(image.size[0])
    h_size = int(float(image.size[1]) * w_percent)
    return image.resize((target_width, h_size), Image.Resampling.LANCZOS), w_percent


class PDFRectangleDrawer:
    def __init__(self, root, image, scale_factor):
        self.root = root
        self.scale = scale_factor
        self.img = ImageTk.PhotoImage(image)

        self.canvas = tk.Canvas(root, width=self.img.width(), height=self.img.height())
        self.canvas.pack()
        self.canvas.create_image(0, 0, anchor="nw", image=self.img)

        self.start_x = None
        self.start_y = None
        self.rect = None
        self.rectangles = []  # List of (canvas_id, coords_scaled)

        self.drag_data = {"item": None, "offset_x": 0, "offset_y": 0}

        self.canvas.bind("<ButtonPress-1>", self.on_button_press)
        self.canvas.bind("<B1-Motion>", self.on_move_press)
        self.canvas.bind("<ButtonRelease-1>", self.on_button_release)

        self.mode = None  # 'draw' or 'move'

    def on_button_press(self, event):
        x = self.canvas.canvasx(event.x)
        y = self.canvas.canvasy(event.y)

        # Check manually if click is inside any known rectangle
        for canvas_id, coords in self.rectangles:
            x1, y1, x2, y2 = [coord * self.scale for coord in coords]
            if x1 <= x <= x2 and y1 <= y <= y2:
                self.drag_data["item"] = canvas_id
                self.drag_data["offset_x"] = x - x1
                self.drag_data["offset_y"] = y - y1
                self.mode = "move"
                return

        # Not on any existing rect — begin new
        self.start_x = x
        self.start_y = y
        self.rect = self.canvas.create_rectangle(x, y, x, y, outline="red")
        self.mode = "draw"

    def on_move_press(self, event):
        x = self.canvas.canvasx(event.x)
        y = self.canvas.canvasy(event.y)

        if self.mode == "move" and self.drag_data["item"]:
            item = self.drag_data["item"]
            coords = self.canvas.coords(item)
            width = coords[2] - coords[0]
            height = coords[3] - coords[1]
            new_x1 = x - self.drag_data["offset_x"]
            new_y1 = y - self.drag_data["offset_y"]
            self.canvas.coords(item, new_x1, new_y1, new_x1 + width, new_y1 + height)
        elif self.mode == "draw" and self.rect:
            self.canvas.coords(self.rect, self.start_x, self.start_y, x, y)

    def on_button_release(self, event):
        if self.mode == "move" and self.drag_data["item"]:
            item = self.drag_data["item"]
            coords = self.canvas.coords(item)
            scaled_coords = tuple(round(c / self.scale) for c in coords)
            print(f"Moved Rectangle (PDF coords): {scaled_coords}")
            # Update saved coords for this rectangle
            for i, (canvas_id, _) in enumerate(self.rectangles):
                if canvas_id == item:
                    self.rectangles[i] = (canvas_id, scaled_coords)
                    break
            self.drag_data["item"] = None
        elif self.mode == "draw" and self.rect:
            coords = self.canvas.coords(self.rect)
            scaled_coords = tuple(round(c / self.scale) for c in coords)
            print(f"New Rectangle (PDF coords): {scaled_coords}")
            self.rectangles.append((self.rect, scaled_coords))
            self.rect = None

        self.mode = None


if __name__ == "__main__":
    img_orig = render_pdf_first_page(PDF_PATH)
    img_scaled, scale_factor = scale_image(img_orig, TARGET_WIDTH)

    root = tk.Tk()
    root.title("Draw and Move Rectangles on PDF Page")
    app = PDFRectangleDrawer(root, img_scaled, scale_factor)
    root.mainloop()
