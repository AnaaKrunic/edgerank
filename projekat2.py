import parse_files
import trie
import networkx as nx
from datetime import datetime
import pickle
import time
import os


def login(users_data):
    while True:
        username = input("Unesi ime i prezime: ")
        if username in users_data:
            return username


def create_friends_graph(people):
    G = nx.DiGraph()

    for person, data in people.items():
        G.add_node(person)  # cvor osobe

        for friend in data['friends']:
            G.add_node(friend)
            G.add_edge(person, friend, weight=1.5)

    save_graph_to_pickle(G, 'people_graph.pickle')


def calculate_affinity():
    decay_factor = 0.9
    time_passed_map = {}

    G = load_graph_from_pickle('people_graph.pickle')

    weight = 3
    for comment in comments:
        status_id = comments[comment]['status_id']
        comment_author = comments[comment]['comment_author']
        if status_id in statuses:
            status_author = statuses[status_id]['author']
            interaction_key = f"comment_{comment_author}_{comments[comment]['comment_published']}"
            if interaction_key not in time_passed_map:
                time_passed_map[interaction_key] = calculate_time_passed(comments[comment]['comment_published'])
            time_passed = time_passed_map[interaction_key]
            if G.has_edge(comment_author, status_author):
                G[comment_author][status_author]['weight'] += round(weight + (decay_factor ** time_passed) * 10000, 2)
            else:
                G.add_edge(comment_author, status_author, weight=round(weight + (decay_factor ** time_passed) * 10000, 2))

    weight = 1.5
    for reaction in reactions:
        status_id = reaction['status_id']
        reactor = reaction['reactor']
        if status_id in statuses:
            interaction_key = f"reaction_{reactor}_{reaction['reacted']}"
            if interaction_key not in time_passed_map:
                time_passed_map[interaction_key] = calculate_time_passed(reaction['reacted'])
            time_passed = time_passed_map[interaction_key]
            author = statuses[status_id]['author']
            if G.has_edge(reactor, author):
                G[reactor][author]['weight'] += round(weight + (decay_factor ** time_passed) * 10000, 2)
            else:
                G.add_edge(reactor, author, weight=round(weight + (decay_factor ** time_passed) * 10000, 2))

    weight = 4.5
    for share in shares:
        status_id = share['status_id']
        sharer = share['sharer']

        if status_id in statuses:
            interaction_key = f"share_{sharer}_{share['status_shared']}"
            if interaction_key not in time_passed_map:
                time_passed_map[interaction_key] = calculate_time_passed(share['status_shared'])
            time_passed = time_passed_map[interaction_key]
            author = statuses[status_id]['author']
            if G.has_edge(sharer, author):
                G[sharer][author]['weight'] += round(weight + (decay_factor ** time_passed) * 10000, 2)
            else:
                G.add_edge(sharer, author, weight=round(weight + (decay_factor ** time_passed) * 10000, 2))

    save_graph_to_pickle(G, 'people_graph.pickle')
    

def calculate_time_passed(timestamp):
    timestamp_datetime = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")

    current_datetime = datetime.now()

    time_passed = (current_datetime - timestamp_datetime).total_seconds() / (60 * 60 * 24)  # u danima

    return time_passed


def save_graph_to_pickle(graph, filename):
    with open(filename, 'wb') as file:
        pickle.dump(graph, file)


def load_graph_from_pickle(filename):
    with open(filename, 'rb') as file:
        graph = pickle.load(file)
    return graph


def status_popularity(status):
    popularity = 0.07 * int(status['num_comments']) + 0.05 * int(status['num_likes']) + 0.05 * int(status['num_likes'])\
                 + 0.09 * int(status['num_shares']) + 0.06 * int(status['num_loves']) + 0.06 * int(status['num_wows'])\
                 + 0.05 * int(status['num_hahas']) + 0.04 * int(status['num_sads']) + 0.02 * int(status['num_angrys'])\
                 + 0.07 * int(status['num_special'])

    return popularity


def statuses_edge_rank():
    G = load_graph_from_pickle('people_graph.pickle')
    for status_id, status_info in statuses.items():
        popularnost = status_popularity(statuses[status_id])/100
        vreme_raspada = calculate_time_passed(status_info['status_published'])
        if G.has_edge(user_id, status_info['author']):
            afinitet = G[user_id][status_info['author']]['weight']
        else:
            afinitet = 0.0

        status_info['edge_rank'] = popularnost + afinitet + (0.9 ** vreme_raspada)


def feed():
    sorted_statuses = sorted(statuses.items(), key=lambda x: x[1]['edge_rank'], reverse=True)
    sorted_statuses = [status_info for status_id, status_info in sorted_statuses]
    for i in range(0, 10):
        num_reactions = sorted_statuses[i]['num_likes'] + sorted_statuses[i]['num_loves'] + sorted_statuses[i]['num_wows']\
            + sorted_statuses[i]['num_hahas'] + sorted_statuses[i]['num_sads'] + sorted_statuses[i]['num_angrys'] + sorted_statuses[i]['num_special']
        print(sorted_statuses[i]['author'])
        print("posted on: " + sorted_statuses[i]['status_published'])
        print(sorted_statuses[i]['status_message'])
        print("reactions: " + num_reactions + ", " + "comments: " + sorted_statuses[i]['num_comments'] + ", " + "shares: " + sorted_statuses[i]['num_shares'])
        print("-" * 30)


'''
def prikazi_veze(user_id):
    G = load_graph_from_pickle('people_graph.pickle')
    for neighbor in G.neighbors(user_id):
        edge_weight = G[user_id][neighbor]['weight']
        print(f"Edge weight between {user_id} and {neighbor}: {edge_weight}")
'''

if __name__ == '__main__':
    # putanje do fajlova
    friends_file_path = r'.\dataset\friends.csv'
    comments_file_path = r'.\dataset\original_comments.csv'
    statuses_file_path = r'.\dataset\original_statuses.csv'
    reactions_file_path = r'.\dataset\original_reactions.csv'
    shares_file_path = r'.\dataset\original_shares.csv'

    users = parse_files.load_friends(friends_file_path)
    comments = parse_files.load_comments(comments_file_path)
    reactions = parse_files.load_reactions(reactions_file_path)
    shares = parse_files.load_shares(shares_file_path)
    statuses = parse_files.load_statuses(statuses_file_path)

    start_time = time.time()

    graph_pickle_path = 'people_graph.pickle'

    if os.path.exists(graph_pickle_path):
        load_graph_from_pickle(graph_pickle_path)
    else:
        create_friends_graph(users)
        calculate_affinity()
        save_graph_to_pickle(load_graph_from_pickle('people_graph.pickle'), graph_pickle_path)

    end_time = time.time()

    execution_time = end_time - start_time
    print(f"Program execution time: {execution_time:.2f} seconds")

    user_id = login(users)

    statuses_edge_rank()

    while True:
        izbor = input("\nIzaberite 1 za prikaz objava, 2 za pretragu, 0 za izlaz: ")
        try:
            izbor = int(izbor)
            if izbor == 0:
                print("Izlaz iz programa.")
                break
            elif izbor == 1:
                feed()
            elif izbor == 2:
                trie.search(statuses)
        except:
            print("Nepoznat izbor. Molimo izaberite 1, 2 ili 0.")
