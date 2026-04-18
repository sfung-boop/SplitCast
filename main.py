from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.responses import StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import io
import zipfile
import traceback

app = FastAPI(title="SplitBoom Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/api/split")
async def split_data(
    file: UploadFile = File(...),
    group_col: str = Form("Tienda"),
    sku_col: str = Form("SKU"),
    qty_col: str = Form("Cantidad")
):
    if not file.filename.endswith(('.xlsx', '.xls')):
        raise HTTPException(status_code=400, detail="El archivo debe ser un Excel (.xlsx, .xls)")

    try:
        contents = await file.read()
        df = pd.read_excel(io.BytesIO(contents), engine='openpyxl')
    except Exception as e:
        print(f"Error al leer excel: {traceback.format_exc()}")
        raise HTTPException(status_code=400, detail=f"Error leyendo archivo: {str(e)}")

    cols_req = [group_col, sku_col, qty_col]
    cols_faltantes = [c for c in cols_req if c not in df.columns]
    
    if cols_faltantes:
        raise HTTPException(
            status_code=400, 
            detail=f"No se encontraron estas columnas en tu Excel: {', '.join(cols_faltantes)}. Verifica las cabeceras."
        )

    df_clean = df.dropna(subset=[group_col, sku_col, qty_col]).copy()
    
    zip_buffer = io.BytesIO()
    sep_real = "\t"

    with zipfile.ZipFile(zip_buffer, "a", zipfile.ZIP_DEFLATED, False) as zip_file:
        for group_val, grupo in df_clean.groupby(group_col):
            nombre_limpio = str(group_val).replace('/', '-').replace('\\', '-').strip()
            
            def clean_qty(val):
                sval = str(val)
                if sval.replace('.','',1).isdigit():
                    try:
                       return str(int(float(sval)))
                    except ValueError:
                       return sval
                return sval

            lineas = grupo.apply(lambda row: f"{row[sku_col]}{sep_real}{clean_qty(row[qty_col])}", axis=1)
            contenido_txt = "\n".join(lineas.astype(str).tolist())
            zip_file.writestr(f"{nombre_limpio}.txt", contenido_txt.encode('utf-8'))

    zip_buffer.seek(0)
    
    original_name = file.filename.rsplit('.', 1)[0]
    headers = {
        'Content-Disposition': f'attachment; filename="Export_{original_name}.zip"'
    }

    return StreamingResponse(zip_buffer, media_type="application/zip", headers=headers)

# Montaje de la carpeta estática para suplir root (index.html)
app.mount("/", StaticFiles(directory="static", html=True), name="static")
