# Image to ASCII

Este programa recibe una imagen como entrada y la devuelve en formato ASCII,
ya sea en una imagen o en un archivo de texto sin formato.

Los argumentos que permite son:

* **-i INPUT, --input INPUT**: INPUT indica la imagen de entrada.
* **-o OUTPUT, --output OUTPUT**: OUTPUT indica el nombre del archivo de salida.
* **--format PNG/TXT/BOTH**: PNG indica salida en imagen, TXT en texto plano y 
    BOTH es para salida en ambos formatos.
* **--size WIDTH HEIGHT**: WIDTH y HEIGHT indican número de caracteres en ancho y alto
    respectivamente de la imagen o texto de salida.
* **-w WIDTH, --width WIDTH**: WIDTH indica lo mismo que size sólo que para el ancho.
* **--height HEIGHT**: HEIGHT indica lo mismo que size sólo que para el alto.
* **-f FONT, --font FONT**: Font indica la fuente que se usará en la conversión.
* **--invert**: Si este argumento es usado se invertirá el contraste. Úselo si el
    fondo en el que se mostrará la imagen o texto de salida es oscuro.
* **-b WIDTH HEIGHT, --blocks WIDTH HEIGHT**: Cuando este argumento no es usado
    el programa asigna a cada pixel un caracter ASCII, lo que hace el programa
    más lento. La tupla (WIDTH, HEIGHT) indica el tamaño de la malla en la que se
    subdividirá la imagen para a cada cuadro asignarle un caracter ASCII(conversión
    por bloques).
* **-a [A], --autoscaled [A]**: Si este argumento es usado la imagen o texto de salida
    será proporcional a la imagen de entrada.
* **-c 1_TO_29, --contrast 1_TO_29**: Número entero entre 1 y 29 que indica el contraste (aún
    no funciona muy bien).
* **-u, --uniform**: Usa los mismos caracteres para la misma intensidad. Los caracteres
    son aleatorios por defecto.
* **-m, --margen**: Si este argumento es usado la imagen o texto de salida tendrá un borde.
* **-s**: Indica cuántos espacios hay entre caracteres en la misma línea.
* **-v, --verbose**: Si este argumento es usado la salida es mostrada en la terminal.
* **-h, --help**: Ayuda.
                        
## Ejemplos
