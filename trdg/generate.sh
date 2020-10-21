#python run.py -c 2000 -fd ./fonts/industry/ --image_dir images/                bg_circuit_black_img/ -tc '#FFFFFF' -f 128 --margins 0,0,0,0 --fit -t 48 --     include_numbers -rs
 
#python run.py -c 2000 -fd ./fonts/industry/ --image_dir images/                bg_circuit_white_img/ -tc '#000000,#454545' -f 128 --margins 0,0,0,0 --fit -t   48 --include_numbers
 
#python run.py -c 2000 -fd ./fonts/industry/ --image_dir images/                bg_circuit_black_img/ -tc '#FFFFFF' -f 128 --margins 0,0,0,0 --fit -t 48  -k    2 -rk
 
#python run.py -c 100  --image_dir images/bg_circuit_black_img/ -tc '#FFFFFF' - f 128 --margins 40,40,40,40 --fit -t 48 -d  --dict ./dicts/Chinese_DRCD.txt -l  cn -fd ./fonts/TraditionalChinese_fonts
 
#python run.py -c 100 -fd ./fonts/TraditionalChinese_fonts/ --dict ./dicts/Chinese_DRCD.txt -l cn

#python run.py -c 1 -w 1 -l cn --dict ./dicts/Chinese_DRCD.txt -f 128  -fd /home/smartmore/tools/trdg/TextRecognitionDataGenerator/trdg/fonts/TraditionalChinese_fonts/

python run.py -c 3 -w 2 -or 2  -bb  --draw_bbox  -f 30 --radius 100 -cs 1


