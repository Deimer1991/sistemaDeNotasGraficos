import pandas as pd
import re


def validar_email(email):
    """Valida formato de email."""
    if pd.isna(email) or email == "NULL":
        return False
    patron = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(patron, str(email)))


def validar_celular(celular):
    """Valida que el celular sea numérico y tenga longitud adecuada."""
    if pd.isna(celular) or celular == "NULL":
        return False
    celular_str = str(celular).strip()
    return celular_str.isdigit() and len(celular_str) >= 10


def reporte_calidad_estudiantes(df_estudiantes):
    """Genera reporte de calidad para estudiantes."""
    print("\n" + "="*70)
    print("ANÁLISIS DE CALIDAD - ESTUDIANTES")
    print("="*70)
    
    total = len(df_estudiantes)
    
    # Valores faltantes
    faltantes = df_estudiantes.isnull().sum()
    print(f"\n VALORES FALTANTES:")
    for col in faltantes[faltantes > 0].index:
        print(f"  - {col}: {faltantes[col]} ({faltantes[col]/total*100:.1f}%)")
    
    # Emails inválidos
    emails_invalidos = df_estudiantes[~df_estudiantes['correo'].apply(validar_email)]
    print(f"\n EMAILS INVÁLIDOS: {len(emails_invalidos)}")
    if len(emails_invalidos) > 0:
        print(f"   Ejemplos: {emails_invalidos['correo'].head(3).tolist()}")
    
    # Estados no ACTIVO
    estados_no_activos = df_estudiantes[df_estudiantes['estado'] != 'ACTIVO']
    print(f"\n  ESTUDIANTES NO ACTIVOS: {len(estados_no_activos)}")
    
    print(f"\n TOTAL ESTUDIANTES: {total}")


def reporte_calidad_profesores(df_profesores):
    """Genera reporte de calidad para profesores."""
    print("\n" + "="*70)
    print("ANÁLISIS DE CALIDAD - PROFESORES")
    print("="*70)
    
    total = len(df_profesores)
    
    # Valores faltantes
    faltantes = df_profesores.isnull().sum()
    print(f"\n VALORES FALTANTES:")
    for col in faltantes[faltantes > 0].index:
        print(f"  - {col}: {faltantes[col]} ({faltantes[col]/total*100:.1f}%)")
    
    # Profesores sin email
    sin_email = df_profesores[~df_profesores['correo'].apply(validar_email)]
    print(f"\n PROFESORES SIN EMAIL VÁLIDO: {len(sin_email)}")
    if len(sin_email) > 0:
        print(f"   Nombres: {sin_email['nombres'].tolist()}")
    
    # Profesores sin celular válido
    sin_celular = df_profesores[~df_profesores['numero_celular'].apply(validar_celular)]
    print(f"\n📱 PROFESORES SIN CELULAR VÁLIDO: {len(sin_celular)}")
    if len(sin_celular) > 0:
        print(f"   Nombres: {sin_celular['nombres'].tolist()}")
    
    # Estados inactivos
    inactivos = df_profesores[df_profesores['estado'] == 'INACTIVO']
    print(f"\n  PROFESORES INACTIVOS: {len(inactivos)}")
    if len(inactivos) > 0:
        print(f"   Nombres: {inactivos['nombres'].tolist()}")
    
    print(f"\n TOTAL PROFESORES: {total}")


def reporte_calidad_grupos(df_grupos, df_materias, df_profesores):
    """Genera reporte de calidad para grupos."""
    print("\n" + "="*70)
    print("ANÁLISIS DE CALIDAD - GRUPOS")
    print("="*70)
    
    total = len(df_grupos)
    
    # Verificar referencias válidas
    materias_ids = set(df_materias['id'].values)
    profesores_ids = set(df_profesores['id'].values)
    
    grupos_sin_materia = df_grupos[~df_grupos['materia_id'].isin(materias_ids)]
    print(f"\n  GRUPOS CON MATERIA INVÁLIDA: {len(grupos_sin_materia)}")
    
    grupos_sin_profesor = df_grupos[~df_grupos['profesor_id'].isin(profesores_ids)]
    print(f"\n  GRUPOS CON PROFESOR INVÁLIDO: {len(grupos_sin_profesor)}")
    
    print(f"\n TOTAL GRUPOS: {total}")


def reporte_calidad_matriculas(df_matriculas, df_grupos, df_estudiantes):
    """Genera reporte de calidad para matrículas."""
    print("\n" + "="*70)
    print("ANÁLISIS DE CALIDAD - MATRÍCULAS")
    print("="*70)
    
    total = len(df_matriculas)
    
    # Verificar referencias válidas
    grupos_ids = set(df_grupos['id'].values)
    estudiantes_ids = set(df_estudiantes['id'].values)
    
    matriculas_sin_grupo = df_matriculas[~df_matriculas['grupo_id'].isin(grupos_ids)]
    print(f"\n  MATRÍCULAS CON GRUPO INVÁLIDO: {len(matriculas_sin_grupo)}")
    
    matriculas_sin_estudiante = df_matriculas[~df_matriculas['estudiante_id'].isin(estudiantes_ids)]
    print(f"\n  MATRÍCULAS CON ESTUDIANTE INVÁLIDO: {len(matriculas_sin_estudiante)}")
    
    print(f"\n TOTAL MATRÍCULAS: {total}")


def reporte_calidad_calificaciones(df_calificaciones, df_matriculas):
    """Genera reporte de calidad para calificaciones."""
    print("\n" + "="*70)
    print("ANÁLISIS DE CALIDAD - CALIFICACIONES")
    print("="*70)
    
    total = len(df_calificaciones)
    
    # Verificar referencias válidas
    matriculas_ids = set(df_matriculas['id'].values)
    
    calificaciones_sin_matricula = df_calificaciones[~df_calificaciones['matricula_id'].isin(matriculas_ids)]
    print(f"\n  CALIFICACIONES CON MATRÍCULA INVÁLIDA: {len(calificaciones_sin_matricula)}")
    
    # Notas fuera de rango (0-5)
    notas_fuera_rango = df_calificaciones[(df_calificaciones['nota'] < 0) | (df_calificaciones['nota'] > 5)]
    print(f"\n NOTAS FUERA DE RANGO (0-5): {len(notas_fuera_rango)}")
    
    print(f"\n TOTAL CALIFICACIONES: {total}")


def generar_reporte_completo_calidad(datos):
    """Genera un reporte completo de calidad de todos los datos."""
    print("\n" + " "*20)
    print("REPORTE GENERAL DE CALIDAD DE DATOS")
    print(" "*20)
    
    reporte_calidad_estudiantes(datos['estudiantes'])
    reporte_calidad_profesores(datos['profesores'])
    reporte_calidad_grupos(datos['grupos'], datos['materias'], datos['profesores'])
    reporte_calidad_matriculas(datos['matriculas'], datos['grupos'], datos['estudiantes'])
    reporte_calidad_calificaciones(datos['calificaciones'], datos['matriculas'])
    
    print("\n" + "="*70)
    print("FIN DEL REPORTE")
    print("="*70 + "\n")