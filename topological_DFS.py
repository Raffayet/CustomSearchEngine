from graph import Graph
from datetime import datetime
import time
from difflib import SequenceMatcher


possible_phone_numbers = []
possible_names = []
possible_surnames = []


from difflib import SequenceMatcher

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

class TrieNode(object):
    """
    Our trie node implementation. Very basic. but does the job
    """

    def __init__(self, char):
        self.char = char
        self.children = []
        # Is it the last character of the word.`
        self.word_finished = False
        # How many times this character appeared in the addition process
        self.counter = 1


def add(root, word):
    """
    Adding a word in the trie structure
    """
    node = root
    for char in word:
        found_in_child = False
        # Search for the character in the children of the present `node`
        for child in node.children:
            if child.char == char:
                # We found it, increase the counter by 1 to keep track that another
                # word has it as well
                child.counter += 1
                # And point the node to the child that contains this char
                node = child
                found_in_child = True
                break
        # We did not find it so add a new chlid
        if not found_in_child:
            new_node = TrieNode(char)
            node.children.append(new_node)
            # And then point node to the new child
            node = new_node
    # Everything finished. Mark it as the end of a word.
    node.word_finished = True


def find_prefix(root, prefix, word_type):
    node = root
    word_length = 0
    number_of_characters = 0

    if not root.children:
        return False, 0
    for char in prefix:
        number_of_characters += 1
        char_not_found = True

        for child in node.children:

            if child.char.lower() == char.lower():
                char_not_found = False

                node = child
                word_length += 1
                break

        if char_not_found:
            return False

    if node.word_finished:
        return "Success"

    possible_names.clear()
    possible_surnames.clear()
    get_possible_words(node.children, prefix, word_type)

    if word_type == "name":
        return possible_names
    elif word_type == "surname":
        return possible_surnames


def find_prefix_for_numbers(root, prefix, number_type):
    node = root
    phone_number_length = 0
    number_of_characters = 0

    if not root.children:
        return False, 0
    for char in prefix:
        if char == '-' or char == ' ':
            continue
        number_of_characters += 1
        char_not_found = True

        for child in node.children:

            if child.char == char:

                char_not_found = False

                node = child
                phone_number_length += 1
                break

        if char_not_found:
            if number_type == "normal":
                return False
            elif number_type == "blocked":
                return False, 0

    if node.word_finished:
        return "Success"

    possible_phone_numbers.clear()
    get_possible_phone_numbers(node.children, prefix)
    return possible_phone_numbers


def get_possible_phone_numbers(children, prefix):
    for i in children:
        if not i.word_finished:     #funkcija koja dobavlja sve moguce brojeve iz datog prefiksa
            get_possible_phone_numbers(i.children, prefix + i.char)
        else:
            possible_phone_numbers.append(prefix+i.char)


def get_possible_words(children, prefix, word_type):
    for i in children:
        if not i.word_finished:     #funkcija koja dobavlja sve moguce reci iz datog prefiksa (imena i prezimena)
            get_possible_words(i.children, prefix + i.char, word_type)
        else:
            if word_type == "name":
                possible_names.append(prefix+i.char)
            elif word_type == "surname":
                possible_surnames.append(prefix+i.char)


def graph_from_edgelist(E, directed=False):

    g = Graph(directed)
    V = set()
    for e in E:
        V.add(e[0])
        V.add(e[1])

    vertices = {}
    for v in V:
        vertices[v] = g.insert_vertex(v)

    for e in E:
        src = e[0]
        dest = e[1]
        element = e[2:] if len(e) > 2 else None
        g.insert_edge(vertices[src], vertices[dest], element)

    return g


def dfs(g, u, discovered):
  """Primenjuje DFS na neotkriven deo grafa(Graph) g počevši od čvora(Vertex) u.

  discovered je rečnik koji mapira svaki čvor na ivicu koja je koriščen za njegovo pronalaženje
  prilikom DFS.
  Nove ivice se dodaju u ovaj rečnik.
  """
  for e in g.incident_edges(u):    # za svaku odlaznu granu iz u
    v = e.opposite(u)
    if v not in discovered:        # provera da li je čvor već posećen
      discovered[v] = e            # e je ivica kojom je otkriven čvor v
      dfs(g, v, discovered)        # rekurzivna pretraga od v


def dfs_complete(g):
    """Primenjuje DFS nad celim grafom i vraća šumu kao rečnik.

    Rezultat mapira svaki čvor v na ivicu koja je korišćena za njegovo otkrivanje.
    (Čvorovi koji su koreni DFS stabla su mapirani na None.)
    """
    forest = {}
    for u in g.vertices():
        if u not in forest:
            forest[u] = None             # u će biti koren stabla
            dfs(g, u, forest)
    return forest


def topological_dfs(graph):
    pass


def find_nodes_without_outgoing_edges(graph):
    nodes = []
    for vertex in graph.vertices():
        if graph.count_incident_edges(vertex, True) == 0:
            nodes.append(vertex)

    return nodes


def main(trie, trie_blocked_numbers, popilarity_graph, phonebook_graph, trie_names, trie_surnames):
    introduction()
    input_control(trie, trie_blocked_numbers, popilarity_graph, phonebook_graph, trie_names, trie_surnames)


def introduction():
    print("\n     TELEFONSKA CENTRALA\n\n")
    print("         DOBRO DOSLI!\n")
    print("===============================")


def menu():
    print("\n1) Simulacija pozivanja uzivo\n")
    print("2) Simulacija pozivanja iz fajla\n")
    print("3) Istorija poziva za dva broja\n")
    print("4) Istorija poziva jednog broja\n")
    print("5) Pretraga telefonskog imenika\n")
    print("e) Izlaz iz aplikacije")


def input_control(trie, trie_blocked_numbers, popularity_graph, phonebook_graph, trie_names, trie_surnames):
    menu()
    option = input("\nUnesite opciju: ")
    while option not in ("1", "2", "3", "4", "5", "e"):
        print("\nInvalid option. Try again.\n")
        option = input("\nUnesite opciju: ")

    if option == "1":
        live_calling(trie, trie_blocked_numbers, popularity_graph, phonebook_graph, trie_names, trie_surnames)
    elif option == "2":
        calling_from_file(trie, trie_blocked_numbers, popularity_graph, phonebook_graph, trie_names, trie_surnames)
    elif option == "3":
        call_history_two_numbers(trie, trie_blocked_numbers, popularity_graph, phonebook_graph, trie_names, trie_surnames)
    elif option == "4":
        call_history_each_number(trie, trie_blocked_numbers, popularity_graph, phonebook_graph, trie_names, trie_surnames)
    elif option == "5":
        search_phonebook(trie, trie_blocked_numbers, popularity_graph, phonebook_graph, trie_names, trie_surnames)
    else:
        exit()


def live_calling(trie, trie_blocked_numbers, popularity_graph, phonebook_graph, trie_names, trie_surnames):
    print("\nUnesite dva broja telefona")
    calling_number = input("\nUnesite pozivajuci broj: ")
    numbers = find_prefix_for_numbers(trie, calling_number, "normal")
    blocked_numbers = find_prefix_for_numbers(trie_blocked_numbers, calling_number, "blocked")

    while blocked_numbers == "Success" or not numbers or not calling_number.isnumeric() and (
            ' ' not in calling_number and '-' not in calling_number):
        print("\nNepostojeci ili blokirani broj telefona. Pokusajte ponovo.")
        calling_number = input("\nUnesite pozivajuci broj: ")
        numbers = find_prefix_for_numbers(trie, calling_number, "normal")
        blocked_numbers = find_prefix_for_numbers(trie_blocked_numbers, calling_number, "blocked")

    if numbers and numbers != "Success":
        calling_number = did_you_mean(numbers, trie_blocked_numbers)

    called_number = input("\nUnesite pozvani broj: ")

    numbers = find_prefix_for_numbers(trie, called_number, "normal")
    blocked_numbers = find_prefix_for_numbers(trie_blocked_numbers, called_number, "blocked")

    while blocked_numbers == "Success" or not numbers or not called_number.isnumeric()\
            and (' ' not in called_number and '-' not in called_number):
        print("\nNepostojeci ili blokirani broj telefona. Pokusajte ponovo.")
        called_number = input("\nUnesite pozvani broj: ")
        numbers = find_prefix_for_numbers(trie, called_number, "normal")
        blocked_numbers = find_prefix_for_numbers(trie_blocked_numbers, called_number, "normal")

    if numbers and numbers != "Success":
        called_number = did_you_mean(numbers, trie_blocked_numbers)

    calling_number = calling_number.replace(" ", "").replace("-", "")
    called_number = called_number.replace(" ", "").replace("-", "")

    if calling_number == called_number:
        print("Pozivajuci i pozvani broj moraju biti razliciti!\n")
        live_calling(trie, trie_blocked_numbers, popularity_graph, phonebook_graph, trie_names, trie_surnames)

    print("\nPoziv je poceo.")

    start_time = datetime.now()
    formatted_start_time = format_dates(start_time)

    while True:
        i = input("\nUnesite 'q' da biste zavrsili poziv.")
        if i == 'q':
            break
        print("\nLos unos:", i)

    end_time = datetime.now()
    print("\nPozivajuci broj: " + str(calling_number))
    print("Pozvani broj: " + str(called_number))
    formatted_end_time = format_dates(end_time)
    duration = end_time - start_time
    print("Pocetak poziva: " + formatted_start_time)
    formatted_duration = format_duration(str(duration))
    print("Trajanje: " + formatted_duration)
    update_popularity_graph(calling_number, called_number, popularity_graph, duration)
    input_control(trie, trie_blocked_numbers, popularity_graph, phonebook_graph, trie_names, trie_surnames)


def did_you_mean(numbers, trie_blocked_numbers):
    print("\nNiste uneli odgovarajuc broj. Da li ste mislili na jedan od ponudjenih?\n")
    available_options = []
    for i in range(len(numbers)):
        available_options.append(str(i))
        if i > 4:
            break
        blocked_numbers = find_prefix_for_numbers(trie_blocked_numbers, numbers[i], "blocked")
        if not blocked_numbers == "Success":
            print(str(i+1) + ") " + numbers[i])
    option = input("\nUnesite redni broj broja telefona: ")
    while str(int(option) - 1) not in available_options:
        print("\nNiste uneli odgovarajucu opciju. Pokusajte ponovo.")
        option = input("\nUnesite redni broj broja telefona: ")

    return numbers[int(option)-1]


def did_you_mean_name(names):
    print("\nNiste uneli odgovarajuce ime. Da li ste mislili na jedno od ponudjenih?\n")
    available_options = []
    for i in range(len(names)):
        available_options.append(str(i))
        if i > 4:
            break
        print(str(i + 1) + ") " + names[i].capitalize())
    option = input("\nUnesite redni broj imena: ")
    while str(int(option) - 1) not in available_options:
        print("\nNiste uneli odgovarajucu opciju. Pokusajte ponovo.")
        option = input("\nUnesite redni broj imena: ")

    return names[int(option) - 1]


def format_duration(duration):
    hh, mm, ss = duration.split(':')
    if int(hh) == 0 and int(mm) == 0:
        return ss + " sekundi"
    if int(hh) == 0 and int(mm) > 0 and float(ss) == 0:
        return mm + " minuta"
    if int(hh) == 0 and int(mm) > 0 and float(ss) > 0:
        return mm + " minuta i " + ss + " sekundi"
    if int(hh) > 0 and int(mm) == 0 and float(ss) == 0:
        return hh + " sati"
    if int(hh) > 0 and int(mm) == 0 and float(ss) > 0:
        return hh + " sati i " + ss + " sekundi"
    if int(hh) > 0 and int(mm) > 0 and float(ss) == 0:
        return hh + " sati i " + mm + " minuta"
    if int(hh) > 0 and int(mm) > 0 and float(ss) > 0:
        return hh + " sati, " + mm + " minuta i " + ss + " sekundi"


def update_popularity_graph(u, v, popularity_graph, duration):
    vertex_u = popularity_graph.insert_vertex(u)
    vertex_v = popularity_graph.insert_vertex(v)
    popularity_graph.insert_edge(vertex_u, vertex_v, duration)


def calculate_popularity():
    pass


def format_dates(date):
    formatted_date = date.strftime("%d/%m/%Y %H:%M:%S")
    return formatted_date


def calling_from_file(trie, trie_blocked_numbers, popularity_graph, phonebook_graph, trie_names, trie_surnames):
    outgoing_calls = popularity_graph.get_all_calls()

    for call in outgoing_calls:
        print("\nPozivajuci broj: " + str(call[0]))
        print("Pozivan broj: " + str(call[1]))
        print("Datum i vreme poziva: " + str(call[2][2:12] + " " + call[2][12:20]))
        print("Trajanje poziva: " + str(call[2][24:32]))
        print("=================================================================================")
        update_popularity_graph(call[0], call[1], popularity_graph, call[2][24:32])

    input_control(trie, trie_blocked_numbers, popularity_graph, phonebook_graph, trie_names, trie_surnames)


def call_history_two_numbers(trie, trie_blocked_numbers, popularity_graph, phonebook_graph, trie_names, trie_surnames):
    calling_number = input("\nUnesite prvi broj: ")
    called_number = input("\nUnesite drugi broj: ")

    calling_number = calling_number.replace(" ", "").replace("-", "")
    called_number = called_number.replace(" ", "").replace("-", "")

    history_outgoing, history_incoming = popularity_graph.get_history(calling_number, called_number)

    for i in history_incoming:
        history_outgoing.append(i)

    for call in history_outgoing:
        print("\nPozivajuci broj: " + str(call[0]))
        print("Pozivan broj: " + str(call[1]))
        print("Datum i vreme poziva: " + str(call[2][2:12] + " " + call[2][12:20]))
        print("Trajanje poziva: " + str(call[2][24:32]))
        print("=================================================================================")

    input_control(trie, trie_blocked_numbers, popularity_graph, phonebook_graph, trie_names, trie_surnames)


def call_history_each_number(trie, trie_blocked_numbers, popularity_graph, phonebook_graph, trie_names, trie_surnames):
    phone_number = input("\nUnesite broj telefona: ")
    phone_number = phone_number.replace(" ", "").replace("-", "")

    history_outgoing, history_incoming = popularity_graph.get_history_each_number(phone_number)

    for call in history_outgoing:
        print("\nPozivajuci broj: " + str(call[0]))
        print("Pozivan broj: " + str(call[1]))
        print("Datum i vreme poziva: " + str(call[2][2:12] + " " + call[2][12:20]))
        print("Trajanje poziva: " + str(call[2][24:32]))
        print("=================================================================================")

    for call in history_incoming:
        print("\nPozivajuci broj: " + str(call[0]))
        print("Pozivan broj: " + str(call[1]))
        print("Datum i vreme poziva: " + str(call[2][2:12] + " " + call[2][12:20]))
        print("Trajanje poziva: " + str(call[2][24:32]))
        print("=================================================================================")

    input_control(trie, trie_blocked_numbers, popularity_graph, phonebook_graph, trie_names, trie_surnames)


def search_phonebook(trie, trie_blocked_numbers, popularity_graph, phonebook_graph, trie_names, trie_surnames):
    print("\n1) Pretraga po imenu")
    print("\n2) Pretraga po prezimenu")
    print("\n3) Pretraga po broju telefona")

    option = input("\nUnesite kriterijum pretrage: ")

    while option not in ("1", "2", "3"):
        print("Pogresna opcija.")
        option = input("\nUnesite kriterijum pretrage: ")

    if option == "1":
        search_phonebook_by_name(trie, trie_blocked_numbers, popularity_graph, phonebook_graph, trie_names, trie_surnames)
    elif option == "2":
        search_phonebook_by_surname(trie, trie_blocked_numbers, popularity_graph, phonebook_graph, trie_names, trie_surnames)
    elif option == "3":
        search_phonebook_by_number(trie, trie_blocked_numbers, popularity_graph, phonebook_graph, trie_names, trie_surnames)


def search_phonebook_by_name(trie, trie_blocked_numbers, popularity_graph, phonebook_graph, trie_names, trie_surnames):
    name = input("\nUnesite ime: ")
    names = find_prefix(trie_names, name, "name")

    while not names:
        print("\nNepostojece ime. Pokusajte ponovo.")
        name = input("\nUnesite ime: ")
        names = find_prefix(trie_names, name, "name")

    if names and names != "Success":
        name = did_you_mean_name(names)
    name = name.capitalize()
    print(name)

    people_outgoing, people_incoming = phonebook_graph.get_history_each_word(name)

    for person in people_outgoing:
        person_data = person[0].split(" ")
        name = person_data[0]
        surname = person_data[1]
        print("\nIme: " + name)
        print("Prezime: " + surname)
        print("Broj telefona: " + str(person[1]))
        print("=================================================================================")

    for person in people_incoming:
        person_data = person[0].split(" ")
        name = person_data[0]
        surname = person_data[1]
        print("\nIme: " + name)
        print("Prezime: " + surname)
        print("Broj telefona: " + str(person[1]))
        print("=================================================================================")

    input_control(trie, trie_blocked_numbers, popularity_graph, phonebook_graph, trie_names, trie_surnames)


def search_phonebook_by_surname(trie, trie_blocked_numbers, popularity_graph, phonebook_graph, trie_names, trie_surnames):
    surname = input("\nUnesite prezime: ")
    surnames = find_prefix(trie_surnames, surname, "surname")

    while not surnames:
        print("\nNepostojece prezime. Pokusajte ponovo.")
        surname = input("\nUnesite prezime: ")
        surnames = find_prefix(trie_surnames, surname, "surname")

    if surnames and surnames != "Success":
        surname = did_you_mean_name(surnames)
    surname = surname.capitalize()
    print(surname)

    people_outgoing, people_incoming = phonebook_graph.get_history_each_word(surname)

    for person in people_outgoing:
        person_data = person[0].split(" ")
        name = person_data[0]
        surname = person_data[1]
        print("\nIme: " + name)
        print("Prezime: " + surname)
        print("Broj telefona: " + str(person[1]))
        print("=================================================================================")

    for person in people_incoming:
        person_data = person[0].split(" ")
        name = person_data[0]
        surname = person_data[1]
        print("\nIme: " + name)
        print("Prezime: " + surname)
        print("Broj telefona: " + str(person[1]))
        print("=================================================================================")

    input_control(trie, trie_blocked_numbers, popularity_graph, phonebook_graph, trie_names, trie_surnames)


def search_phonebook_by_number(trie, trie_blocked_numbers, popularity_graph, phonebook_graph, trie_names, trie_surnames):
    number = input("\nUnesite broj telefona: ")
    numbers = find_prefix_for_numbers(trie, number, "normal")

    while not numbers or not number.isnumeric() and (
            ' ' not in number and '-' not in number):
        print("\nNepostojeci broj telefona. Pokusajte ponovo.")
        number = input("\nUnesite broj: ")
        numbers = find_prefix_for_numbers(trie, number, "normal")

    if numbers and numbers != "Success":
        number = did_you_mean(numbers, trie_blocked_numbers)

        numbers_outgoing, numbers_incoming = phonebook_graph.get_history_each_number(number)

        for number in numbers_outgoing:
            person_data = number[0].split(" ")
            name = person_data[0]
            surname = person_data[1]
            print("\nIme: " + name)
            print("Prezime: " + surname)
            print("Broj telefona: " + str(number[1]))
            print("=================================================================================")

        for number in numbers_incoming:
            person_data = number[0].split(" ")
            name = person_data[0]
            surname = person_data[1]
            print("\nIme: " + name)
            print("Prezime: " + surname)
            print("Broj telefona: " + str(number[1]))
            print("=================================================================================")

        input_control(trie, trie_blocked_numbers, popularity_graph, phonebook_graph, trie_names, trie_surnames)
    input_control(trie, trie_blocked_numbers, popularity_graph, phonebook_graph, trie_names, trie_surnames)


def read_phones_data(root, trie_names, trie_surnames):
    with open("test data/test_phones.txt") as file1:
        phones = file1.readlines()
        edges = []
        for phone in phones:
            phone = phone.replace("\n", "")
            phone_data = phone.split(",")
            phone_data[1] = phone_data[1].replace("\n", "").replace(" ", "").replace("-", "")
            edges.append(phone_data)
            if phone_data[1] != "Phone Number" and phone_data[0] != "Name":
                add(root, phone_data[1])
                person = phone_data[0].split(" ")
                name = person[0]
                surname = person[1]
                add(trie_names, name)
                add(trie_surnames, surname)
        graph = graph_from_edgelist(edges, True)
        find_nodes_without_outgoing_edges(graph)
    return graph


def read_blocked_phones_data(trie_blocked_numbers):
    with open("test data/blocked.txt") as file2:
        blocked_phones = file2.readlines()
        for blocked_phone in blocked_phones:
            blocked_phone = blocked_phone.replace("\n", "").replace(" ", "").replace("-", "")
            add(trie_blocked_numbers, blocked_phone)
    return trie_blocked_numbers


def read_calls_data(root):
    with open("test data/test_calls.txt") as file:
        calls = file.readlines()
        edges = []
        for call in calls:
            call = call.replace("\n", "").replace(" ", "").replace("-", "")
            call_data = call.split(",")
            edges.append(call_data)
        graph = graph_from_edgelist(edges, True)
        find_nodes_without_outgoing_edges(graph)
    return graph


if __name__ == '__main__':
    root = TrieNode('*')
    trie_initial_blocked_numbers = TrieNode('*')
    trie_names = TrieNode('*')
    trie_surnames = TrieNode('*')
    phonebook_graph = read_phones_data(root, trie_names, trie_surnames)
    trie_blocked_numbers = read_blocked_phones_data(trie_initial_blocked_numbers)
    popularity_graph = read_calls_data(root)
    main(root, trie_blocked_numbers, popularity_graph, phonebook_graph, trie_names, trie_surnames)

