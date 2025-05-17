from tkinter import filedialog
from utils import PDF_Converter as PdfConverter
import datetime
import time

class Controller:
    ui: object
    def __init__(self):
        pass
    def init(self, ui):
        self.ui = ui

    def open_file_dialog(self):
        file_paths = filedialog.askopenfilenames(
            title="选择PDF文件",
            filetypes=[("PDF Files", "*.pdf")]
        )
        
        if file_paths:
            self.ui.update_files("\n".join(file_paths))
            timestamp = time.time()
            datetime_object = datetime.datetime.fromtimestamp(timestamp)

            formatted_time = datetime_object.strftime("%Y-%m-%d_%H-%M-%S")
            pdf_converter = PdfConverter(formatted_time)
            png_files = pdf_converter.extract_images_from_pdf(file_paths)
            self.ui.update_results(pdf_converter.merge_images_to_pdf(png_files))

    def on_click(self,evt):
        self.open_file_dialog()
