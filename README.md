# Proyecto Biblioteca - Git, GitHub, Testing y Refactorizacion

Este proyecto es una practica por fases para trabajar con Git, GitHub, `unittest`,
refactorizacion, documentacion y resolucion de conflictos.

El objetivo no es entregar un sistema perfecto desde el principio. El objetivo es
mejorar un codigo inicial con problemas reales, usando un proceso de trabajo
ordenado y dejando evidencias de cada paso.

## Objetivos

- Usar Git y GitHub con ramas, commits frecuentes y merges.
- Escribir tests con `unittest` antes de modificar codigo.
- Refactorizar codigo existente sin cambiar su comportamiento.
- Documentar el proyecto y el codigo con docstrings y pdoc.
- Trabajar en paralelo con un companero y resolver conflictos reales.
- Practicar rollback con `git revert` y `git reset`.

## Normas principales

No se debe trabajar directamente en `main`.

Cada fase debe hacerse en una rama propia:

```bash
git checkout -b feature/nombre-fase
```

Antes de empezar a trabajar:

```bash
git pull
```

Durante el trabajo:

```bash
git add .
git commit -m "mensaje claro y concreto"
git push
```

Antes de integrar una rama:

```bash
git checkout main
git pull
git merge feature/nombre-fase
```

## Estructura inicial del proyecto

```text
Biblioteca_base/
├── bd/
│   ├── biblioteca.db
│   └── biblioteca.sql
├── tests/
│   ├── test_base_datos.py
│   └── test_biblioteca.py
├── AGENTS.md
├── biblioteca.py
├── .gitignore
└── README.md
```

La carpeta `bd/` contiene una base SQLite inicial para preparar la ultima fase
del proyecto. En esta fase no se debe usar todavia como capa de persistencia.

## Como ejecutar los tests

Desde la raiz del proyecto:

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests
```

Si Python esta configurado globalmente en el equipo, tambien puede ejecutarse:

```bash
python -m unittest discover -s tests
```

## Fase 1 - Setup y analisis

Objetivo: preparar el entorno y entender el codigo base.

Tareas:

- Clonar el repositorio.
- Abrir el proyecto en PyCharm.
- Ejecutar los tests iniciales.
- Leer `biblioteca.py`.
- Anotar en este README:
  - que hace el proyecto,
  - problemas detectados,
  - partes confusas,
  - funciones mal disenadas.
- Revisar la base inicial `bd/biblioteca.db`.

Rama sugerida:

```bash
git checkout -b feature/setup
```

Commit sugerido:

```bash
git commit -m "F1: setup, analisis y revision inicial"
```

## Fase 2 - Testing obligatorio

Objetivo: crear tests antes de modificar codigo.

Regla principal:

```text
No se modifica codigo si antes no existe un test que falle.
```

Tareas:

- Crear o completar tests en `tests/`.
- Usar nombres claros.
- Probar una sola funcionalidad por test.
- Incluir casos correctos y casos de error.
- Ejecutar los tests despues de cada cambio.

Rama sugerida:

```bash
git checkout -b feature/testing
```

## Fase 3 - Refactorizacion inicial

Objetivo: mejorar el codigo sin anadir funcionalidad.

Tareas:

- Renombrar variables poco claras como `x`, `data`, `tmp` o similares.
- Dividir funciones largas.
- Eliminar duplicacion.
- Simplificar condicionales.
- Mantener el comportamiento existente.
- Ejecutar tests despues de cada refactorizacion pequena.
- Anadir docstrings en las funciones modificadas.

Ejemplo de commit:

```bash
git commit -m "Refactor: renombra variables de busqueda de libros"
```

## Fase 4 - Libros

Objetivo: implementar la gestion de libros.

Requisitos orientativos:

- Crear una clase `Libro`.
- Gestionar campos como `id`, `titulo`, `autor`, `disponible` e `ISBN`.
- Implementar operaciones CRUD.
- Anadir al menos tres busquedas:
  - por titulo,
  - por autor,
  - por disponibilidad,
  - por coincidencia parcial,
  - por id.

Cada operacion debe tener tests.

Rama sugerida:

```bash
git checkout -b feature/libros
```

## Fase 5 - Usuarios

Objetivo: implementar la gestion de usuarios en paralelo a la fase de libros.

Requisitos orientativos:

- Crear una clase `Usuario`.
- Gestionar campos como `id`, `nombre`, `apellidos`, `email` y `habilitado`.
- Implementar operaciones CRUD.
- Implementar `habilita_usuario(id)` y `deshabilita_usuario(id)`.
- Crear al menos tres busquedas.

Rama sugerida:

```bash
git checkout -b feature/usuarios
```

Esta fase debe generar conflictos al integrarse con la fase de libros.

## Fase 6 - Prestamos

Objetivo: relacionar libros y usuarios.

Funciones esperadas:

```python
prestar_libro(libro_id, usuario_id)
devolver_libro(libro_id, usuario_id)
```

Trabajo recomendado:

- Alumno A: `prestar_libro`.
- Alumno B: `devolver_libro`.

Se espera que aparezcan conflictos porque ambos alumnos tocaran zonas cercanas
del codigo.

## Fase 7 - Logs

Objetivo: registrar acciones importantes del sistema.

Ejemplo:

```text
Usuario X ha prestado Libro Y
```

Debe haber tests que comprueben que las acciones quedan registradas.

## Fase 8 - Integracion total

Objetivo: unificar operaciones mediante una funcion general.

Ejemplo:

```python
operar(accion, datos)
```

Esta fase debe servir para integrar lo anterior y resolver conflictos finales.

## Rollback obligatorio

El proyecto debe demostrar dos tipos de vuelta atras:

```bash
git revert <commit>
```

```bash
git reset --hard <commit>
```

Hay que guardar capturas o evidencias de ambos casos.

## Entregables

Al finalizar el proyecto se debe entregar:

- Codigo funcional.
- Tests ejecutables.
- Documentacion del codigo.
- README actualizado.
- PDF de documentacion del proceso.
- Evidencias de:
  - `git log`,
  - commits,
  - ramas,
  - merges,
  - conflictos,
  - resolucion de conflictos,
  - rollback.

## Evaluacion

Se evaluara especialmente:

- Uso correcto de Git y GitHub.
- Calidad y orden de los commits.
- Uso de ramas por fase.
- Tests antes de modificar codigo.
- Refactorizaciones pequenas y justificadas.
- Documentacion clara.
- Evidencias del trabajo.
- Defensa del proyecto.
- Colaboracion y resolucion de conflictos.

## Estado inicial del codigo

El codigo inicial esta pensado para ser mejorado. Contiene problemas de diseno
de forma intencionada:

- variables poco descriptivas,
- datos globales,
- mezcla de logica y salida por pantalla,
- condicionales redundantes,
- duplicacion,
- estructura dificil de seguir.

No se debe reescribir todo desde cero. La mejora debe hacerse poco a poco,
siempre con tests previos.
