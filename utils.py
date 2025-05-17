import pymupdf  # PyMuPDF
from PIL import Image
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import os


class PDF_Converter:

    pdf_size = 0
    png_size = 0
    target = ''

    def __init__(self, target):
        self.target = target

    def resize_image_with_aspect_ratio(self, img, max_width, max_height):
        width, height = img.size
        
        scale_width = max_width / width
        scale_height = max_height / height
        scale = min(scale_width, scale_height)
        
        new_width = int(width * scale)
        new_height = int(height * scale)
        
        return img.resize((new_width, new_height))

    def extract_images_from_pdf(self, pdf_path_list):
        png_files = []
        for pdf_path in pdf_path_list:
            doc = pymupdf.open(pdf_path)

            for page_num in range(doc.page_count):
                page = doc.load_page(page_num)
                #page.set_rotation(270)
                pixmap = page.get_pixmap(matrix=pymupdf.Matrix(4,4))

                file_name = os.path.basename(pdf_path)
                name, ext = os.path.splitext(file_name)
                file_path = os.path.dirname(pdf_path)
                temp_img_path = os.path.join(file_path, self.target, "png", f"{name}_{page_num}_convert.png")
                os.makedirs(os.path.dirname(temp_img_path), exist_ok=True)
                pixmap.save(temp_img_path)
                png_files.append(temp_img_path)
        self.pdf_size = len(pdf_path_list)
        return png_files


    def merge_images_to_pdf(self, png_files):
        self.png_size = len(png_files)

        if png_files and len(png_files) > 0:
            page_width, page_height = A4

            dir = os.path.dirname(os.path.dirname(png_files[0]))
            report_path = os.path.join(dir, "converted")
            output_pdf_path = os.path.join(report_path, "双页合并.pdf")
            os.makedirs(os.path.dirname(output_pdf_path), exist_ok=True)
            c = canvas.Canvas(output_pdf_path, pagesize=A4)
            
            x_offset = 0
            y_offset = page_height / 2

            flag = 0
            for i, png_file in enumerate(png_files):
                if flag % 2 == 0:
                    x_offset = 0
                    y_offset = page_height / 2
                else:
                    x_offset = 0
                    y_offset = 0
                png_folder = os.path.dirname(os.path.realpath(png_file))
                img_path = os.path.join(png_folder, png_file)
                img = Image.open(img_path)

                if img.size[0] < img.size[1]:
                    img = self.resize_image_with_aspect_ratio(img, page_width, page_height)
                    if y_offset == 0:
                        c.showPage()
                    c.drawImage(img_path, 0, 0, width=img.size[0], height=img.size[1])
                    c.showPage()
                    flag = 0
                else:
                    img = self.resize_image_with_aspect_ratio(img, page_width, page_height/2)
                    c.drawImage(img_path, x_offset, y_offset, width=img.size[0], height=img.size[1])
                    if (flag + 1) % 2 == 0:
                        c.showPage()
                    flag += 1
            c.save()

        output_pdf_path = os.path.join(report_path, "单页合并.pdf")
        os.makedirs(os.path.dirname(output_pdf_path), exist_ok=True)
        c = canvas.Canvas(output_pdf_path, pagesize=A4)

        for i, png_file in enumerate(png_files):            
            png_folder = os.path.dirname(os.path.realpath(png_file))
            img_path = os.path.join(png_folder, png_file)
            img = Image.open(img_path)

            img = self.resize_image_with_aspect_ratio(img, page_width, page_height)
            y_offset = page_height - img.size[1]
            c.drawImage(img_path, 0, y_offset, width=img.size[0], height=img.size[1])
            c.showPage()
        c.save()
        return f"已加载PDF{self.pdf_size}个\n已提取PNG{self.png_size}个\n结果文档路径:{report_path}"