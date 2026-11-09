#!/usr/bin/env python3
import sys
import csv
from collections import defaultdict

def procesar_secuencial(filepath):
    totales = defaultdict(float)
    with open(filepath, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        header = next(reader, None)
        for row in reader:
            if len(row) < 8:
                continue
            try:
                mes = row[1].split(" ")[0][:7]
                cat = row[3]
                ingreso = float(row[5]) * float(row[6])
                totales[f"{cat}\t{mes}"] += ingreso
            except ValueError:
                continue
    return totales

if __name__ == "__main__":
    if len(sys.argv) > 1:
        resultado = procesar_secuencial(sys.argv[1])
        print(f"Procesados {len(resultado)} registros agregados con script secuencial.")