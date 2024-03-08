python -m cProfile [-o output_file] [-s sort_order] (-m module | myscript.py)

python -m cProfile -o 12.profile dva.py

python -m pstats 12.profile

pip install snakeviz

python -m cProfile -o program.prof my_program.py
snakeviz program.prof

snakeviz 12.profile