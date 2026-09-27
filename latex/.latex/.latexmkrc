# latexmk-Konfiguration
#   - PDF landet im übergeordneten Ordner (latex/)
#   - Hilfsdateien (.aux, .log, .toc, ...) bleiben hier in build/
$pdf_mode = 1;            # pdflatex
$out_dir  = '..';         # PDF eine Ebene höher
$aux_dir  = 'build';      # alles andere versteckt in .latex/build/
