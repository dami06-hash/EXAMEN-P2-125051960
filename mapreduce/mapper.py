#!/usr/bin/env python3
import sys

for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    
    parts = line.split(',')
    if parts[0] == "id" or len(parts) < 8:
        continue
        
    try:
        fecha_hora = parts[1]
        categoria = parts[3]
        cantidad = float(parts[5])
        precio = float(parts[6])
        
        mes = fecha_hora.split(" ")[0][:7]
        ingreso = cantidad * precio
        
        print(f"{categoria}\t{mes}\t{ingreso:.2f}")
    except Exception:
        continue