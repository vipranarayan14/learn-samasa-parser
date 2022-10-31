import sys
import re

from subprocess import run


def get_form(query):
    cmd = ["sh", "-c", f"echo '{query}' | lt-proc -gc all_gen.bin"]
    process = run(cmd, capture_output=True, check=True)
    output = process.stdout.decode()

    form = output.split("\n")[0]
    return form


def generate_vigraha(input_str, linga):
    samasa_exp_re = r'<([a-zA-Z]+)-([a-zA-Z]+)>T(\d)'

    samasa_exp = re.search(samasa_exp_re, input_str)

    if samasa_exp:
        (word1, word2, vibhakti) = samasa_exp.groups()
        
        varga = 'nA'
        vacanas = ['eka', 'xvi', 'bahu']

        for vacana in vacanas: 

            query = f'^{word1}<vargaH:{varga}><lifgam:{linga}><viBakwiH:{vibhakti}><vacanam:{vacana}><level:1>$'
            form = get_form(query)

            print(form + ' ' + word2)

    else:
        print('exp not parsed')


input_str = sys.argv[1]
linga = sys.argv[2]

generate_vigraha(input_str, linga)
