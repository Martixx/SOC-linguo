# SOC-linguo

**SOC-linguo** es una aplicación web local y ampliable para practicar inglés aplicado a ciberseguridad, operaciones SOC y comunicación profesional con clientes.

El proyecto nace como una herramienta de aprendizaje continuo. La colección actual es solo el punto de partida: se pueden añadir nuevas baterías de preguntas, ampliar las existentes y crear nuevos bloques sin modificar el código principal.

La aplicación funciona en un único archivo HTML, sin servidor y sin enviar preguntas, respuestas, estadísticas ni progreso fuera del navegador.

## Qué puedes practicar

SOC-linguo combina dos líneas de aprendizaje:

### Gramática y fundamentos

Tiempos verbales, formas verbales, modales, condicionales, artículos, sustantivos contables e incontables, preposiciones, oraciones de relativo, voz pasiva, estilo indirecto, colocaciones habituales de SOC y formación de preguntas.

### Natural English

Inglés profesional para:

- presentar incidentes con claridad;
- explicar evidencias e incertidumbre;
- comunicar recomendaciones y riesgo;
- presentar métricas y tendencias;
- responder preguntas y gestionar desacuerdos;
- explicar detecciones y procesos SOC;
- utilizar conectores naturales en presentaciones;
- comunicar procesos, dependencias y próximos pasos.

## Colección actual

La versión inicial del repositorio incluye:

- **1.910 preguntas** al cargar la colección completa;
- **33 baterías** en total;
- **1 batería integrada** de fundamentos, con 100 preguntas;
- **24 baterías de gramática y fundamentos**, con 1.010 preguntas;
- **8 baterías de Natural English**, con 800 preguntas.

Estas cifras describen la versión inicial y aumentarán a medida que se incorporen nuevas baterías y revisiones.

## Funciones principales

- Sesiones de 10, 20, 50, 100 preguntas o colección completa.
- Selección por colección, batería individual y tema.
- Orden aleatorio.
- Corrección inmediata.
- Explicaciones gramaticales en español.
- Traducciones naturales al español.
- Estadísticas por tema.
- Repetición de preguntas falladas.
- Importación individual o múltiple de baterías JSON y CSV.
- Sustitución completa de la biblioteca importada sin borrar la batería integrada.
- Persistencia local mediante el almacenamiento del navegador.
- Funcionamiento sin backend, cuenta o base de datos.

## Uso rápido

### Abrir en local

1. Descarga o clona el repositorio.
2. Abre `index.html` con Microsoft Edge, Google Chrome o Mozilla Firefox.
3. Pulsa **Importar batería**.
4. Selecciona uno o varios archivos de `batteries/normal` y `batteries/natural-english`.
5. Para cargar la colección completa, selecciona los 32 JSON y marca **Sustituir las baterías importadas actuales**.

Las baterías y el progreso se guardan únicamente en el navegador utilizado.

### Publicar con GitHub Pages

1. Abre el repositorio en GitHub.
2. Entra en **Settings > Pages**.
3. En **Build and deployment**, selecciona **Deploy from a branch**.
4. Selecciona la rama `main` y la carpeta `/ (root)`.
5. Guarda los cambios.

GitHub Pages publicará `index.html` como página principal. Cada usuario podrá importar las baterías que quiera utilizar.

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

## Añadir nuevas baterías

SOC-linguo está diseñado para seguir creciendo. Una batería nueva puede importarse desde la propia aplicación sin modificar `index.html`.

### Formato JSON básico

```json
{
  "name": "33 · Nuevo tema · Normal",
  "category": "normal",
  "version": 1,
  "description": "Descripción breve de la batería.",
  "questions": [
    {
      "id": "33-001",
      "topic": "Nuevo tema",
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

- `normal`: gramática, vocabulario y fundamentos;
- `natural`: comunicación profesional y Natural English.

### Convención de nombres

```text
NN · Topic · Normal
NN · Topic · Natural English
```

Ejemplos:

```text
21 · Modal verbs · Normal
18 · Explaining detections and SOC processes · Natural English
```

El número de preguntas no se incluye en el nombre porque la interfaz lo calcula automáticamente.

### Recomendaciones de calidad

Antes de añadir una batería:

- usa identificadores únicos para todas las preguntas;
- incluye cuatro opciones plausibles;
- distribuye las respuestas correctas entre A, B, C y D;
- evita distractores absurdos o demasiado evidentes;
- añade una explicación centrada en el inglés;
- incluye una traducción natural al español;
- evita que la respuesta dependa de conocimientos técnicos discutibles;
- revisa repeticiones, ambigüedades y frases poco naturales;
- valida la importación en SOC-linguo antes de publicar.

## Preparar la colección para GitHub

El script `tools/prepare-github.ps1` valida la colección normalizada y distribuye las baterías según su categoría.

```powershell
Set-ExecutionPolicy -Scope Process Bypass
.\tools\prepare-github.ps1
```

La validación inicial espera:

- 24 baterías `normal`;
- 8 baterías `natural`;
- 32 JSON;
- 1.810 preguntas importables.

Si la colección crece, estos valores deberán actualizarse en el script o sustituirse por una validación dinámica.

## Próximas mejoras

Algunas líneas previstas para futuras versiones:

- nuevas baterías de gramática, vocabulario y Natural English;
- ejercicios específicos para reuniones, presentaciones e incident updates;
- exportación e importación del progreso;
- búsqueda y filtrado avanzado de baterías;
- catálogo de baterías disponible desde la propia interfaz;
- carga opcional de la colección publicada en GitHub;
- ejercicios adicionales de producción escrita y corrección;
- mejoras de accesibilidad y experiencia móvil.

## Privacidad

SOC-linguo no requiere cuenta, backend, base de datos ni analítica. El progreso se guarda en el almacenamiento local del navegador.

Cambiar de navegador, cambiar de dispositivo, abrir el HTML desde otra ubicación o borrar los datos del sitio puede hacer que la biblioteca y el progreso no aparezcan en la nueva sesión.

## Compatibilidad

La aplicación está diseñada para navegadores modernos como:

- Microsoft Edge;
- Google Chrome;
- Mozilla Firefox.

La apertura de archivos HTML locales y la persistencia del almacenamiento pueden variar en dispositivos móviles, especialmente en iOS.

## Contribuciones

Las propuestas de nuevas baterías, correcciones y mejoras son bienvenidas mediante issues o pull requests.

Al proponer contenido nuevo, indica:

- categoría;
- nivel o dificultad aproximada;
- objetivo lingüístico;
- número de preguntas;
- tipo de contexto SOC utilizado;
- validaciones realizadas.

## Licencia

Este proyecto se distribuye bajo la licencia MIT. Consulta `LICENSE`.
