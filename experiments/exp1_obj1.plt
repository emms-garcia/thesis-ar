
set encoding utf8
set term postscript
set grid
set output "exp1_obj1.eps"
unset label                            # remove any previous labels
set xtic auto                          # set xtics automatically
set ytic 0.01
set title "Modelo tridimensional de una rueda"
set xlabel "Número de imagen"
set ylabel "Tiempo (s)"
set yrange [0:0.055]
plot "exp1_cube/3d_overlap.dat" using 1:($2 == 0 ? NaN : $2) title 'Superposición' with points pointtype 7 pointsize 1 , \
"exp1_obj1/image_processing.dat" using 1:2 title 'Procesamiento de imagen' with lines , \
"exp1_obj1/qr_detect.dat" using 1:2 title 'Detección de QR' with lines , \
"exp1_obj1/all.dat" using 1:2 title 'Proceso completo' with lines
