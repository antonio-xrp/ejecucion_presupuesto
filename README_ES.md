# PRESUPUESTO Y EJECUCIÓN - GOBIERNOS LOCALES - MUNICIPALIDADES Perú 2026 📊

![Static Badge](https://img.shields.io/badge/Python-data_analysis-blue?logo=Python&logoColor=yellow&color=blue)
![Static Badge](https://img.shields.io/badge/Streamlit-dashboard-blue?logo=Streamlit&logoColor=red&color=blue)
![Static Badge](https://img.shields.io/badge/pandas-Data_manipulation-blue?logo=pandas&logoColor=red&color=blue)
![Static Badge](https://img.shields.io/badge/Matplotlib-Data_visualization-green?logo=Matplotlib&logoColor=red&color=green)
![Static Badge](https://img.shields.io/badge/Seaborn-Data_visualization-green?logo=Seaborn&logoColor=red&color=purple)
![Static Badge](https://img.shields.io/badge/status-in_development-blue?logoColor=red&color=red)


Estado:  🚧 En progreso (Hombres Trabajando!!!)

## Contexto

Aunque la información presupuestal es pública y se puede encontrar en plataformas como [Transparencia economica Perú](https://apps5.mineco.gob.pe/transparencia/Mensual/default.aspx?y=2026&ap=Proyecto). Sin embargo, la consulta y exploración puede resultar engorroso a la hora de obtener datos de los gobiernos locales pues esta no esta no esta optimizada para el usuario final. 

<!-- La solución consiste en obtener y transformar los datos financieros públicos en un dashboard analítico interactivo y optimizado para el usuario final desarrollado con Python y Streamlit, permitiendo explorar los principales indicadores presupuestales, mediante filtros geográficos y temporales.  -->

## Resumen del proyecto

El proyecto busca convertir datos públicos de presupuesto y ejecución en información que pueda ser explorada de forma más sencilla, enfocado en el usuario común y corriente. 

El análisis se centra principalmente en:

- Análisis exploratorio de datos (EDA) para comprender la estructura, distribución y comportamiento de la información presupuestal.
- Presupuesto Institucional de Apertura (PIA)
- Presupuesto Institucional Modificado (PIM)
- Gasto devengado
- Porcentaje de ejecución presupuestal
- Saldo pendiente de ejecución
- Evolución mensual del gasto
- Ejecución acumulada
- Comparación entre gobiernos locales (En Revisión)

## 🎯  Preguntas Claves

El análisis fue diseñado para responder a las siguientes preguntas:

- ¿Cuánto es el presupuesto asignado de una provincia y distrito (PIA) en soles (S/)? 
- ¿Cuánto es el presupuesto modificado de una provincia y distrito (PIM) en soles (S/)? 
- ¿Cuánto es el devengando (gasto ejecutado) de una provincia y distrito? 
- ¿Cuánto es el porcentaje de ejecución respecto al presupuesto modificado (PIM) durante el año? 
- ¿Cuánto es el saldo pendiente de ejecución respecto al presupuesto modificado (PIM)?
- ¿Cómo evoluciona el gasto durante el año?
- ¿Cúales son las 10 provincias y distritos que han ejecutado mejor el presupuesto modificado (PIM)?
- ¿En qué áreas se ha ejecutado más presupuesto en proyectos?

## 💡 Hallazgos claves

El siguiente análisis será respecto a la provincia de Huancayo y al distrito del Tambo respecto al mes de agosto del año 2026. 

- El distrito del Tambo, uno de los distritos más importantes de la pronvicia de Huancayo, ha ejecutado cerca del 45% del Presupuesto Modificado (PIM). 

- El distrito del Tambo ocupa el puesto 8 de 28 distritos respecto al porcentaje de ejecución respecto al Presupuesto Modificado (PIM)

- El distrito del Tambo cuenta cerca de S/. 16.7 M para invertir en proyectos en lo que queda año.

- El distrito del Tambo ha invertido más dinero *Saneamiento* con S/ 5.7 M, 

> **Conclusión:** Al mes de agosto, El Tambo registra una ejecución presupuestal de 44.7% del PIM, manteniendo el 55.3% pendiente de ejecución. Este resultado requiere revisar el avance de los proyectos y los factores que pueden estar limitando la ejecución del presupuesto.

## 📈 Dashboard

El dashoard puedes encontrarlo en la siguiente página: 🔗 [ejecucionpresupuesto](https://ejecucionpresupuesto.streamlit.app/)

![alt text](image-1.png)

## 📁 Estructura del projecto



```text
.
├── environment.yml
├── figures
│   └── dashboard.png
├── projects
│   └── 0.1_ejecucion_presupuesto
│       ├── app
│       │   ├── charts
│       │   │   ├── bar.py
│       │   │   └── line.py
│       │   ├── components
│       │   │   ├── __init__.py
│       │   │   └── kpi.py
│       │   ├── __init__.py
│       │   ├── main.py
│       │   ├── services
│       │   │   ├── __init__.py
│       │   │   └── presupuesto.py
│       │   ├── styles
│       │   │   └── kpi.css
│       │   └── utils
│       │       ├── data.py
│       │       ├── format.py
│       │       ├── __init__.py
│       │       └── styles.py
│       ├── data
│       │   ├── interim
│       │   ├── processed
│       │   │   ├── ejecucion_mensual.parquet
│       │   │   └── presupuesto.parquet
│       │   └── raw
│       │       └── 2026-Gasto-Mensual.csv
│       ├── models
│       └── notebooks
│           ├── 0.1_presupuesto_ejecuciongasto.ipynb
│           ├── hyo_provincia.csv
│           ├── mef_2026_clean.parquet
│           ├── mef_2026.parquet
│           ├── ranking_gobiernos_regionales.png
│           ├── regional_ejecucion.csv
│           └── tipo_gastos_junin.csv
├── README_ES.md
├── README.md
├── environment.yml
└── shared
    ├── data
    │   └── __init__.py
    ├── __init__.py
    ├── utils
    │   └── __init__.py
    └── visualization
        └── __init__.py

```

## 👉 ¿Cómo ejecutar el proyecto?

Clona el repositorio:

```bash
git clone https://github.com/antonio-xrp/ejecucion_presupuesto.git
```

Ingresa al directorio del proyecto:

```bash
cd ejecucion_presupuesto
```

Crea el entorno de Conda a partir del archivo `environment.yml`:

```bash
conda env create -f environment.yml
```

Activa el entorno:

```bash
conda activate data_analysis
```

Ejecuta el dashboard de Streamlit:

```bash
streamlit run projects/0.1_ejecucion_presupuesto/app/main.py
```

La aplicación se abrirá automáticamente en el navegador.

Si no se abre automáticamente, accede a:

```text
http://localhost:8501
```

## 👨‍💻 Author

**Antonio Palacios**

**Ingenierio Industrial | Analista de datos | Científico de datos**

- GitHub: [Antonio Palacios](https://github.com/antonio-xrp)
- LinkedIn: [Antonio Palacios](https://www.linkedin.com/in/antonio-palacios-orihuela-xrp/)
- correo: palaciosorihuelaantonio@gmail.com
