
set encoding utf8
set term postscript
set grid
set output "exp1_obj5.eps"
unset label                            # remove any previous labels
set xtic auto                          # set xtics automatically
set ytic 0.01
set title "Modelo tridimensional de una silla"
set xlabel "Número de imagen"
set ylabel "Tiempo (s)"
set logscale y
plot "exp1_cube/3d_overlap.dat" using 1:($2 == 0 ? NaN : $2) title 'Superposición' with points pointtype 7 pointsize 1 , \
"exp1_obj5/image_processing.dat" using 1:2 title 'Procesamiento de imagen' with lines , \
"exp1_obj5/qr_detect.dat" using 1:2 title 'Detección de QR' with lines , \
"exp1_obj5/all.dat" using 1:2 title 'Proceso completo' with lines
