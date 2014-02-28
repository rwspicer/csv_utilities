#!/bin/bash

red='\e[0;91m'
NC='\e[0m'
bold=`tput bold`
normal=`tput sgr0`

barrow_at_whole=./support_files/brw_at.csv
barrow_at_1=./support_files/brw_at_1.csv
barrow_at_2=./support_files/brw_at_2.csv
barrow_at_3=./support_files/brw_at_3.csv






# --- test plotter

# ------- multi file no avg
echo -e "${red}${bold}testing plotter -- multiple files no avg${normal}${NC}"
python plotter.py --data_0=${barrow_at_1} --data_1=${barrow_at_2} --data_2=${barrow_at_3}  --title="barrow air temp" --y_label="dec c" --x_label="days" --output_png=./support_files/plotter_multi_file.png 
echo -e "${red}${bold}end test\n${normal}${NC}"

# ------- multi file with avg
echo -e "${red}${bold}testing plotter -- multiple files with avg${normal}${NC}"
python plotter.py --data_0=${barrow_at_1} --data_1=${barrow_at_2} --data_2=${barrow_at_3}  --title="barrow air temp" --y_label="dec c" --x_label="days" --output_png=./support_files/plotter_multi_file_avg.png 
echo -e "${red}${bold}end test\n${normal}${NC}"

# ------- multi-col no avg
echo -e "${red}${bold}testing plotter -- 1 file multiple column${normal}${NC}"
python plotter.py --data_0=${barrow_at_whole} --multi_col_mode=t --num_cols=10 --title="barrow air temp" --y_label="dec c" --x_label="days" --output_png=./support_files/plotter_multi_col.png 
echo -e "${red}${bold}end test\n${normal}${NC}"

# ------- multi-col avg
echo -e "${red}${bold}testing plotter -- 1 file multiple column with avg${normal}${NC}"
python plotter.py --data_0=${barrow_at_whole} --multi_col_mode=t --num_cols=10 --title="barrow air temp" --y_label="dec c" --x_label="days" --output_png=./support_files/plotter_multi_col_avg.png --plot_avg=t
echo -e "${red}${bold}end test\n${normal}${NC}"
