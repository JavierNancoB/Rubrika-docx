# Rubrika-docx
Trabajo del ramo de taller de sistemas de información

# Objetivo de la App

Este proyecto tiene como objetivo desarrollar una aplicación en **Python** que permita la automatización de la generación de documentos legales para empresas. La aplicación se encargará de:

1. **Leer archivos .docx** utilizando la biblioteca `python-docx`.
2. **Identificar y reemplazar variables** en los documentos por claves o keys preestablecidas, según los datos específicos de cada empresa.
3. **Generar múltiples documentos legales** a partir de una plantilla base, integrando la información personalizada desde una base de datos.

### Tecnologías utilizadas:
- **Python**: Lenguaje principal de la aplicación.
- **Flask**: Framework web para la gestión y despliegue de la aplicación.
- **pytest**: Framework para pruebas unitarias, garantizando la calidad del código.
- **python-docx**: Biblioteca para la lectura y modificación de archivos Word (.docx).
- **Base de datos**: Para almacenar la información de las empresas que deseen generar documentos legales personalizados.

### Funcionalidades principales:
- Leer archivos `.docx` e identificar variables en el contenido del documento.
- Reemplazar las variables del documento por información predefinida almacenada en la base de datos.
- Generar automáticamente documentos legales personalizados para cada cliente.
  
## Archivos necesarios

Trabajaremos con Python, Flask como microframework y el framework pytest, ademas utilizaremos la libreria python-docx para la lectura de los archivos en formato .docx

# Instalación de Python, Flask y pytest

Instrucciones para configurar un entorno con Python, Flask y pytest.

## 1. Instalación de Python

### Windows:
1. Descarga el instalador desde: https://www.python.org/downloads/
2. Durante la instalación, selecciona la opción **"Add Python to PATH"**.
3. Verifica la instalación ejecutando en CMD:
   ```bash
   python --version
   ```

### macOS/Linux:
1. Instala Python (si no lo tienes ya):
   - macOS (Homebrew):
     ```bash
     brew install python
     ```
   - Debian/Ubuntu:
     ```bash
     sudo apt update && sudo apt install python3
     ```
   - Fedora:
     ```bash
     sudo dnf install python3
     ```
2. Verifica la instalación:
   ```bash
   python3 --version
   ```
### 1.1. Instalación de python-docx
    ```bash
   pip install python-docx
   ```
## 2. Entorno Virtual (Opcional)

1. Crea un entorno virtual (recomendado):
   ```bash
   python3 -m venv venv
   ```
2. Activa el entorno:
   - Windows:
     ```bash
     venv\Scripts\activate
     ```
   - macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

## 3. Instalación de Flask y pytest

Con el entorno virtual activado (o globalmente), instala Flask y pytest:

```bash
pip install Flask pytest
```

## 4. Verificación de las Instalaciones

Verifica que Flask y pytest se instalaron correctamente:

- Flask:
  ```bash
  python -c "import flask; print(flask.__version__)"
  ```
- pytest:
  ```bash
  pytest --version
  ```

---

