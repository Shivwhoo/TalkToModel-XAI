"""Render all pages of the BEST PDF to preview PNGs."""
import os
import pypdfium2 as pdfium

os.chdir(r'C:\Users\Sachin\Desktop\talktomodel-replication')
os.makedirs('visualizations/best_pdf_preview', exist_ok=True)

pdf = pdfium.PdfDocument('Experimental_Results_and_Comparison_BEST.pdf')
n = len(pdf)
print(f"Total pages: {n}")

for i in range(n):
    page = pdf[i]
    bitmap = page.render(scale=2.0, rotation=0)
    pil_img = bitmap.to_pil()
    out_path = f'visualizations/best_pdf_preview/page_{i+1}.png'
    pil_img.save(out_path)
    print(f"  Saved: {out_path}")

pdf.close()
print("Done!")

