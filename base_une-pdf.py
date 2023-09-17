import PyPDF2

archivos = ["test1.pdf",
            "test2.pdf",
            "test3.pdf"]

nombre_salida = "pdf_unido.pdf"

pdf_final = PyPDF2.PdfMerger()

for nombre_archivo in archivos:
    pdf_final.append(nombre_archivo)

pdf_final.write(nombre_salida)
pdf_final.close()
