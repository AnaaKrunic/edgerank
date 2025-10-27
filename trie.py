from collections import defaultdict
import string


class TrieNode:
    def __init__(self):
        self.children = {}
        self.post_indices = []


class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word, post_index):
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
            node.post_indices.append(post_index)


def search_trie(trie, query):
    node = trie.root
    for char in query:
        if char not in node.children:
            return []  # rec nije pronađena
        node = node.children[char]

    return node.post_indices


def search_phrase(phrase, statuses):
    containing_phrase = []
    lowercase_phrase = phrase.lower()

    for status_id, status_info in statuses.items():
        status_message = status_info['status_message'].lower()
        if lowercase_phrase in status_message:
            containing_phrase.append(status_id)

    return containing_phrase


def clean_text(text):
    text = text.translate(str.maketrans("", "", string.punctuation))
    text = " ".join(text.split())
    return text


def rank_results(statuses, search_results, query_words):
    ranked_results = defaultdict(int)

    for post_index in search_results:
        edge_rank = statuses[post_index]['edge_rank']

        for query_word in query_words:
            if query_word in statuses[post_index]['status_message'].lower():
                ranked_results[post_index] += 1

        ranked_results[post_index] += edge_rank

    return sorted(ranked_results.keys(), key=lambda x: ranked_results[x], reverse=True)


def search(statuses):
    trie = Trie()

    for status_id, status_info in statuses.items():
        status_message = status_info['status_message']
        words = status_message.lower().split()
        for word in words:
            trie.insert(clean_text(word), status_id)

    query = input("Pretrazite: ")
    query_words = query.lower().split()

    if query.startswith('"') and query.endswith('"'):
        phrase = query[1:-1]
        search_results = search_phrase(phrase, statuses)
    else:
        query_words = query.lower().split()
        search_results = []
        for query_word in query_words:
            search_results.extend(search_trie(trie, query_word))

    ranked_results = rank_results(statuses, search_results, query_words)
    if len(ranked_results) > 10:
        top_results = ranked_results[:10]
    else:
        top_results = ranked_results

    if len(top_results) == 0:
        print("Nema objava za unetu pretragu")
    else:
        for status_id in top_results:
            num_reactions = statuses[status_id]['num_likes'] + statuses[status_id]['num_loves'] + statuses[status_id]['num_wows']\
                + statuses[status_id]['num_hahas'] + statuses[status_id]['num_sads'] + statuses[status_id]['num_angrys'] + statuses[status_id]['num_special']
            print(statuses[status_id]['author'])
            print("posted on: " + statuses[status_id]['status_published'])
            print(statuses[status_id]['status_message'])
            print("reactions: " + num_reactions + ", " + "comments: " + statuses[status_id]['num_comments'] + ", " + "shares: " + statuses[status_id]['num_shares'])
            print("-" * 30)
