# SOC-linguo

**SOC-linguo** es una aplicación web local para practicar inglés aplicado a ciberseguridad, operaciones SOC y comunicación profesional con clientes.

La aplicación funciona en un único archivo HTML, sin servidor y sin enviar preguntas, respuestas, estadísticas ni progreso fuera del navegador.

## Contenido

- 1.910 preguntas disponibles tras cargar la colección completa.
- 33 baterías en total:
  - 1 batería integrada de fundamentos, con 100 preguntas.
  - 24 baterías de gramática y fundamentos, con 1.010 preguntas.
  - 8 baterías de Natural English, con 800 preguntas.
- Sesiones de 10, 20, 50, 100 preguntas o colección completa.
- Filtros por batería y tema.
- Orden aleatorio.
- Corrección inmediata, explicaciones y traducciones al español.
- Estadísticas por tema y repetición de errores.
- Importación múltiple de baterías JSON o CSV.
- Persistencia local mediante el almacenamiento del navegador.

## Uso rápido

### Opción 1: abrir en local

1. Descarga o clona el repositorio.
2. Abre `index.html` con Microsoft Edge, Google Chrome o Mozilla Firefox.
3. Pulsa **Importar batería**.
4. Selecciona los archivos JSON disponibles en `batteries/normal` y `batteries/natural-english`.
5. Para cargar la colección completa, selecciona todos los JSON y marca **Sustituir las baterías importadas actuales**.

### Opción 2: GitHub Pages

1. Abre el repositorio en GitHub.
2. Entra en **Settings > Pages**.
3. En **Build and deployment**, selecciona **Deploy from a branch**.
4. Selecciona la rama `main` y la carpeta `/ (root)`.
5. Guarda los cambios.

GitHub Pages publicará `index.html` como página principal. Las baterías se importan manualmente y permanecen en el almacenamiento local de cada navegador.

## Estructura del repositorio

```text
SOC-linguo/
├── index.html
├── README.md
├── LICENSE
├── .gitignore
├── batteries/
│   ├── normal/
│   └── natural-english/
└── tools/
    ├── normalize_english_soc_lab.py
    └── prepare-github.ps1
```

## Categorías

### Gramática y fundamentos

Incluye formas verbales, tiempos verbales, modales, condicionales, artículos, sustantivos contables e incontables, preposiciones, relativas, voz pasiva, estilo indirecto, colocaciones SOC y preguntas.

### Natural English

Incluye presentaciones de incidentes, evidencia e incertidumbre, recomendaciones y riesgo, métricas y tendencias, preguntas y desacuerdos, explicación de detecciones y procesos SOC, conectores discursivos y próximos pasos.

## Formato básico de una batería

```json
{
  "name": "21 · Modal verbs · Normal",
  "category": "normal",
  "version": 1,
  "questions": [
    {
      "id": "21-001",
      "topic": "Modal verbs",
      "question": "We ___ review the logs before drawing a conclusion.",
      "options": ["should", "should to", "are should", "must to"],
      "correct": 0,
      "explanation": "Después de un modal se usa la forma base del verbo.",
      "translation": "Deberíamos revisar los logs antes de sacar una conclusión."
    }
  ]
}
```

Valores permitidos para `category`:

- `normal`
- `natural`

## Privacidad

SOC-linguo no requiere cuenta, backend, base de datos ni analítica. El progreso se guarda en el almacenamiento local del navegador. Cambiar de navegador, dispositivo o borrar los datos del sitio puede eliminar el progreso.

## Compatibilidad

Probado para navegadores modernos basados en Chromium, como Microsoft Edge y Google Chrome. También debería funcionar en versiones recientes de Mozilla Firefox.

## Licencia

Este proyecto se distribuye bajo la licencia MIT. Consulta `LICENSE`.
