@echo off
cd D:\pdf_status
python count_pdfs.py
git add pdf_status.json
git commit -m "Update PDF count"
git push origin main