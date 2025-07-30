# Guía Extensiva de Comandos VIM / IdeaVim

Esta guía combina los comandos del Vim Tutor con una recopilación de comandos adicionales para una referencia más completa.

## 📜 Modos de VIM

- **Modo Normal (`Normal Mode`):** El modo por defecto para navegación y manipulación. Se accede con `Esc` o `Ctrl+C`.
- **Modo Inserción (`Insert Mode`):** Para escribir texto. Se accede con `i`, `a`, `o`, etc.
- **Modo Visual (`Visual Mode`):** Para seleccionar texto. Se accede con `v`, `V`, `Ctrl+V`.
- **Modo Comando (`Command-Line Mode`):** Para ejecutar comandos complejos. Se accede con `:`.

---

## 🧭 MOVIMIENTO DEL CURSOR (Modo Normal)

#### Básico
- **h, j, k, l**: Izquierda, abajo, arriba, derecha.
- **w**: Inicio de la siguiente palabra.
- **b**: Inicio de la palabra anterior.
- **e**: Fin de la palabra actual.
- **0** o **^**: Inicio de la línea (el `^` va al primer carácter no blanco).
- **$**: Fin de la línea.
- **gg**: Ir al inicio del archivo.
- **G**: Ir al final del archivo.
- **{número}G**: Ir a la línea `{número}`.

#### Avanzado
- **H**: Ir a la parte superior de la pantalla (Head).
- **M**: Ir a la mitad de la pantalla (Middle).
- **L**: Ir a la parte inferior de la pantalla (Low).
- **%**: Saltar a paréntesis, corchete o llave emparejado.
- **Ctrl+f**: Avanzar una pantalla completa.
- **Ctrl+b**: Retroceder una pantalla completa.

---

## ✍️ EDICIÓN DE TEXTO

#### Inserción y Adición (`Insert Mode`)
- **i**: Insertar texto *antes* del cursor.
- **a**: Insertar texto *después* del cursor.
- **I**: Insertar al *principio* de la línea actual.
- **A**: Insertar al *final* de la línea actual.
- **o**: Abrir una nueva línea *debajo* de la actual y entrar en modo inserción.
- **O**: Abrir una nueva línea *encima* de la actual y entrar en modo inserción.

#### Eliminación (`Normal Mode`)
- **x**: Eliminar el carácter bajo el cursor.
- **X**: Eliminar el carácter *antes* del cursor.
- **d{movimiento}**: Eliminar texto según un movimiento.
  - **dw**: Eliminar desde el cursor hasta el inicio de la siguiente palabra.
  - **de**: Eliminar hasta el final de la palabra actual.
  - **d$** o **D**: Eliminar desde el cursor hasta el final de la línea.
  - **dd**: Eliminar la línea actual.
  - **d2w**: Eliminar las siguientes 2 palabras.

#### Reemplazo y Cambio (`Normal Mode`)
- **c{movimiento}**: Cambiar texto (elimina y entra en modo inserción).
  - **cw**: Cambiar palabra.
  - **c$** o **C**: Cambiar hasta el final de la línea.
  - **cc**: Cambiar la línea entera.
- **r{caracter}**: Reemplazar el carácter bajo el cursor por `{caracter}`.
- **R**: Entrar en modo Reemplazo para sobrescribir múltiples caracteres.

---

## 🔁 DESHACER Y REHACER

- **u**: Deshacer el último cambio.
- **Ctrl+r**: Rehacer el cambio deshecho.
- **.**: Repetir el último comando de modificación.

---

## 📋 COPIAR (YANK) Y PEGAR

- **y{movimiento}**: Copiar (yank) texto según un movimiento.
  - **yw**: Copiar una palabra.
  - **yy** o **Y**: Copiar la línea actual.
- **p**: Pegar *después* del cursor.
- **P**: Pegar *antes* del cursor.

---

## 🔎 BÚSQUEDA Y SUSTITUCIÓN

#### Búsqueda
- **/patrón**: Buscar `patrón` hacia adelante.
- **?patrón**: Buscar `patrón` hacia atrás.
- **n**: Ir a la siguiente coincidencia.
- **N**: Ir a la coincidencia anterior.

#### Sustitución
- **:s/viejo/nuevo/g**: Sustituir todas las ocurrencias de `viejo` por `nuevo` en la línea actual.
- **:%s/viejo/nuevo/g**: Sustituir en todo el archivo.
- **:%s/viejo/nuevo/gc**: Sustituir en todo el archivo con confirmación para cada caso.

---

## 👁️ MODO VISUAL

- **v**: Iniciar modo Visual (por carácter).
- **V**: Iniciar modo Visual por línea.
- **Ctrl+v**: Iniciar modo Visual por bloque.
- **aw**: Seleccionar una palabra (`a word`).
- Una vez en modo visual, puedes usar operadores como `d` (delete), `y` (yank), `c` (change).

---

## 🪟 VENTANAS Y PESTAÑAS

- **:sp {archivo}**: Dividir la ventana horizontalmente (split).
- **:vs {archivo}**: Dividir la ventana verticalmente (vertical split).
- **Ctrl+w + w**: Cambiar entre ventanas.
- **Ctrl+w + {h,j,k,l}**: Moverse a la ventana de la izquierda, abajo, arriba, derecha.
- **:tabnew** o **:tabe**: Abrir una nueva pestaña.
- **gt**: Ir a la siguiente pestaña.
- **gT**: Ir a la pestaña anterior.

---

## 📂 ARCHIVOS Y COMANDOS EXTERNOS

- **:w**: Guardar el archivo actual.
- **:wq** o **:x** o **ZZ**: Guardar y salir.
- **:q**: Salir (falla si hay cambios sin guardar).
- **:q!** o **ZQ**: Salir sin guardar cambios.
- **:e {archivo}**: Editar un archivo.
- **:ls** o **:buffers**: Listar todos los archivos abiertos (buffers).
- **:bn**: Ir al siguiente buffer.
- **:bp**: Ir al buffer anterior.
- **:bd**: Cerrar un buffer.
- **:!{comando}**: Ejecutar un comando de shell externo.

---

## ⚙️ CONFIGURACIÓN (`:set`)

- **:set ic**: Ignorar mayúsculas/minúsculas en búsquedas (`ignorecase`).
- **:set noic**: No ignorar mayúsculas/minúsculas.
- **:set hls**: Resaltar todas las coincidencias de búsqueda (`hlsearch`).
- **:set is**: Mostrar coincidencias parciales mientras se escribe la búsqueda (`incsearch`).
- **:nohlsearch** o **:noh**: Desactivar el resaltado de búsqueda temporalmente.

---

## 🛠️ PERSONALIZACIÓN (`.ideavimrc`)

- Crea el archivo `~/.ideavimrc` en tu directorio de usuario.
- Añade configuraciones y mapeos personalizados. Ejemplo:
  ```vim
  " Activa la búsqueda incremental y el resaltado
  set incsearch
  set hlsearch

  " Mapeo para salir del modo inserción más rápido
  inoremap jk <Esc>
  ```