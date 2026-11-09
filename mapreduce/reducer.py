#!/usr/bin/env python3
import sys
from collections import defaultdict

totales = defaultdict(float)

for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    
    try:
        parts = line.split('\t')
        if len(parts) == 3:
            categoria, mes, ingreso = parts[0], parts[1], float(parts[2])
            clave = f"{categoria}\t{mes}"
            totales[clave] += ingreso
    except Exception:
        continue

for clave, total in totales.items():
    print(f"{clave}\t{total:.2f}")