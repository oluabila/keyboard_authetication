# keyboard

Generates dataset for the study of typing patterns of people to distinguish 
them from one another.

---------------------------------------------

Records feature:

##### Keyup-Keydown time – time between the release of one key and the press of next key.

Generates txt files for the timings.

----------------------------------------------------------------------------------------


Run `keyboard.py`  to see it in action.

* Run `keyboard.py` and provide name for user who is recording the keystrokes  EX. Olha
* You can modify the number of recordings in one execution by modifying `frequency_keyWord_entry` inside `keyboard.py` to increase the force of the process of indenfying the legitimate user. 

There are three possible modes: 1 - studying; 0 - authorization; 2 - exit. After finishing studying/ authorization, .txt files with the user_name for timing intervals, mathematical expectation and despersion in `output/` folder.
 


#### Note

This script works for Windows Systems.

У каталог site=packages додані необхідні для роботи програми бібліотеки. 
Якщо виникнуть проблему з їх пошуком чи не буди змоги завантажити ії через cmd.

Щоб запустити програму:
python keyboard.py

Потрібен пітон версії 3.7 та вище та відповідні бібліотеки. Програма працює для ОС Windows.

Для створення власного .ехе файлу можете використати команду:
pyinstaller -F keyboard.py
