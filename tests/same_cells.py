# Exits with an error if two Excel workbooks differ in any cell value (used by the GitHub Action).
import sys,openpyxl
v=lambda p:[[list(r) for r in ws.iter_rows(values_only=True)] for ws in openpyxl.load_workbook(p).worksheets]
sys.exit(0 if v(sys.argv[1])==v(sys.argv[2]) else f'cell values differ: {sys.argv[2]} (run update_all.py and commit)')
