# Image to ASCII

Este programa recibe una imagen como entrada y la devuelve en formato ASCII
ya sea en una imagen o en un archivo de texto sin formato.

Los argumentos que permite son:

* **-i INPUT, --input INPUT**: INPUT indica la imagen de entrada.
* **-o OUTPUT, --output OUTPUT**: OUTPUT indica el nombre del archivo de salidad
* **--format PNG/TXT/BOTH**: PNG indica salida en imagen, TXT en texto plano y 
    BOTH es para salida en ambos formatos.
* **--size WIDTH HEIGHT**: WIDTH y HEIGHT indican número de carácteres en ancho y alto
    respectivamente de la imagen o texto de salida.
* **-w WIDTH, --width WIDTH**: WIDTH indica lo mismo que size solo que para el ancho.
* **--height HEIGHT**: HEIGHT indica lo mismo que size solo que para el alto.
* **-f FONT, --font FONT**: Font indica la fuente que se usara en la conversión.
* **--invert**: Si este argumento es pasado se invertirá el contraste. úselo si el
    fondo en el que se mostrara la imagen o texto de salida es oscuro.
* **-b WIDTH HEIGHT, --blocks WIDTH HEIGHT**: Cuando este argumento no es pasado
    el programa asigna a cada píxel un carácter ASCII, lo que hace el programa
    más lento. La tupla (WIDTH, HEIGHT) indica el tamaño de la malla en la que se
    subdividirá la imagen para a cada cuadro asignarle un carácter ASCII(conversión
    por bloques).
* **-a [A], --autoscaled [A]**: Si este argumento es pasado la imagen o texto de salida
    será proporcional a la imagen de entrada.
* **-c 1_TO_29, --contrast 1_TO_29**: entero entre 1 y 29 que indica el contraste(aún
    no funciona muy bien).
* **-u, --uniform**: Usa los mismos carácteres para la misma intensidad. los carácteres
    son aleatorios por defecto.
* **-m, --margen**: Si este argumento es pasado la imagen o texto de salida tendrá un borde.
* **-s**: Indica cuantos espacios hay entre carácteres en la misma líneas.
* **-v, --verbose**: Si este argumento es pasado la salida es mostrada en la terminal.
* **-h, --help**: ayuda.
                        
## Examples
