import sys
import re

from subprocess import run


def get_forms(query):
    cmd = ["sh", "-c", f"echo '{query}' | lt-proc -gc all_gen.bin"]
    process = run(cmd, capture_output=True, check=True)
    output = process.stdout.decode()

    forms = output.split("\n")[:-1]
    return forms


def make_query(word, input_linga, vibhakti):
    queries = []

    varga = "nA"

    vacanas = ["eka", "xvi", "bahu"]
    lingas = [input_linga] if input_linga else ["puM", "swrI", "napuM"]

    for linga in lingas:

        for vacana in vacanas:

            queries.append(
                f"^{word}<vargaH:{varga}><lifgam:{linga}>"
                f"<viBakwiH:{vibhakti}><vacanam:{vacana}><level:1>$"
            )

    return "\n".join(queries)


def generate_vigraha(input_str, linga):
    samasa_exp_re = r"<([a-zA-Z]+)-([a-zA-Z]+)>T(\d)"

    samasa_exp = re.search(samasa_exp_re, input_str)

    if samasa_exp:
        (word1, word2, vibhakti) = samasa_exp.groups()

        query = make_query(word1, linga, vibhakti)

        forms = get_forms(query)

        for form in forms:

            if not form.startswith("#"):

                print(form + " " + word2)

    else:
        raise Exception("Unable to parse samasa expression.")


input_str = sys.argv[1]
linga = sys.argv[2] if len(sys.argv) > 2 else ""

generate_vigraha(input_str, linga)
