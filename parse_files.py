from random import randint, random
from datetime import datetime, timedelta
import time
from collections import defaultdict

def load_comments(path):
    output_data = {}
    with open(path, encoding='UTF-8') as file:
        lines = file.readlines()
        comment = ""
        found_open_ellipsis = False
        found_close_ellipsis = False

        for index in range(1, len(lines)):

            line = lines[index]

            if line == "\n":
                comment += line

            if line[-1] == "\n":
                line = line[:-1]

            first_index = line.index("\"") if "\"" in line else -1
            if first_index > -1:
                found_open_ellipsis = True

            next_index = line.index("\"", first_index + 1) if "\"" in line[first_index + 1:] else -1
            if next_index > -1:
                found_close_ellipsis = True

            if found_open_ellipsis and not found_close_ellipsis:
                comment += line
                continue
            else:
                comment = line

            data = comment.split(",")
            n = len(data)

            if n < 14:
                raise Exception("Comment does not contain necessary data.")
            elif n > 14:
                comment_text = "".join(data[3:n - 10])
            else:
                comment_text = data[3]

            content = {
                "status_id": data[1],
                "parent_id": data[2],
                "comment_message": comment_text,
                "comment_author": data[n - 10],
                "comment_published": data[n - 9],
                "num_reactions": data[n - 8],
                "num_likes": data[n - 7],
                "num_loves": data[n - 6],
                "num_wows": data[n - 5],
                "num_hahas": data[n - 4],
                "num_sads": data[n - 3],
                "num_angrys": data[n - 2],
                "num_special": data[n - 1]
            }
            output_data[data[0]] = content

            found_open_ellipsis = found_close_ellipsis = False
            comment = ""
    return output_data


def load_friends(path):
    people_data = {}
    with open(path, 'r', encoding='UTF-8') as file:
        lines = file.readlines()
        for line in lines[1:]:
            data = line.strip().split(",")
            person = data[0]
            number_of_friends = int(data[1])
            friends = data[2:]

            people_data[person] = {
                "number_of_friends": number_of_friends,
                "friends": friends
            }
    return people_data


def load_statuses(path):
    extracted_statuses = {}
    with open(path, encoding='UTF-8') as file:
        lines = file.readlines()
        status = ""
        paired_ellipses = True

        for index in range(1, len(lines)):

            line = lines[index]

            if line == "\n":
                status += line
                continue

            # if line[-1] == "\n":
            #     line = line[:-1]
            line = line.strip()

            previous_index = -1

            while True:
                index = line.index("\"", previous_index+1) if "\"" in line[previous_index+1:] else -1
                if index == -1:
                    break
                paired_ellipses = not paired_ellipses
                previous_index = index

            status += line
            if not paired_ellipses:
                continue

            data = status.split(",")
            n = len(data)

            if n < 17:
                raise Exception("Status does not contain necessary data.")
            elif n > 17:
                status_message = "".join(data[1:n - 16])
            else:
                status_message = data[1]

            content = {
                "status_message": status_message,
                "link_name": data[n-15],
                "status_type": data[n-14],
                "status_link": data[n-13],
                "status_published": data[n-12],
                "author": data[n-11],
                "num_reactions": data[n-10],
                "num_comments": data[n-9],
                "num_shares": data[n-8],
                "num_likes": data[n-7],
                "num_loves": data[n-6],
                "num_wows": data[n-5],
                "num_hahas": data[n-4],
                "num_sads": data[n-3],
                "num_angrys": data[n-2],
                "num_special": data[n-1],
                "edge_rank": 0.0
            }
            extracted_statuses[data[0]] = content
            status = ""
            paired_ellipses = True

    return extracted_statuses


def generate_datetime_after_datetime(date_str):
    format_str = "%Y-%m-%d %H:%M:%S"
    start_datetime = time.strptime(date_str, format_str)
    end_datetime = time.localtime(time.time())

    start_time = time.mktime(start_datetime)
    end_time = time.mktime(end_datetime)

    ptime = start_time + random() * (end_time - start_time)
    return time.strftime(format_str, time.localtime(ptime))


def modify_date_to_recent(date_str):
    format_str = "%Y-%m-%d %H:%M:%S"
    old_date = datetime.strptime(date_str, format_str)

    days_ago = [_ for _ in range(30)]
    days_ago.extend(_ for _ in range(0, 16))
    days_ago.extend(_ for _ in range(0, 6))
    days_ago.extend(_ for _ in range(0, 2))

    rand_num = days_ago[randint(0, len(days_ago)-1)]
    generated_date = datetime.today() - timedelta(days=rand_num)

    new_date = old_date.replace(year=generated_date.year, month=generated_date.month, day=generated_date.day)
    return str(new_date)


def get_statuses_header():
    return ",".join(['status_id', 'status_message', "link_name", "status_type", "status_link",
                             "status_published", "author" "num_reactions", "num_comments", "num_shares",
                             "num_likes", "num_loves", "num_wows", "num_hahas", "num_sads", "num_angrys",
                             "num_special"])


def get_reaction_header():
    return "status_id,type_of_reaction,reactor,reacted"


def get_share_header():
    return "status_id,sharer,status_shared"


def get_comment_header():
    return "comment_id,status_id,parent_id,comment_message,comment_author,comment_published,num_reactions,num_likes," \
           "num_loves,num_wows,num_hahas,num_sads,num_angrys,num_special"


def load_shares(path):
    shares_data = []
    with open(path, encoding='UTF-8') as file:
        lines = file.readlines()
        '''        
        for line in lines[1:]:
            data = line.strip().split(",")
            reaction_info = {
                "status_id": data[0],
                "type_of_reaction": data[1],
                "reactor": data[2],
                "reacted": data[3]
            }
            reactions_data.append(reaction_info)
            '''
        for line in lines[1:]:
            data = line.strip().split(",")
            share_info = {
                "status_id": data[0],
                "sharer": data[1],
                "status_shared": data[2]
            }
            shares_data.append(share_info)
    return shares_data


def load_reactions(path):
    reactions_data = []

    with open(path, encoding='UTF-8') as file:
        lines = file.readlines()

        for line in lines[1:]:
            data = line.strip().split(",")
            reaction_info = {
                "status_id": data[0],
                "type_of_reaction": data[1],
                "reactor": data[2],
                "reacted": data[3]
            }
            reactions_data.append(reaction_info)

    return reactions_data


def adjust_date_time(statuses_path, comments_path, shares_path, reactions_path):
    '''
    Podešava datume test objava na datume u poslednjih mesec dana (sa većom verovatnoćom da su
    bliži današnjem datumu). U skladu sa tim, ažurira i datume komentara, deljenja i reakcija.
    :param statuses_path: putanja do fajla sa statusima
    :param comments_path: putanja do fajla sa komentarima
    :param shares_path: putanja do fajla sa deljenjima
    :param reactions_path: putanja do fajla sa reakcijama
    '''
    statuses = load_statuses(statuses_path)
    status_to_datetime = {}
    with open(statuses_path, "w") as file:
        file.write(get_statuses_header()+"\n")
        for status in statuses:
            status_datetime = status[4]
            new_status_datetime = modify_date_to_recent(status_datetime)
            status_to_datetime[status[0].strip()] = new_status_datetime
            file.write(",".join(status) + "\n")

    comments = load_comments(comments_path)
    with open(comments_path, "w") as file:
        file.write(get_comment_header() + "\n")
        for comment in comments:
            comment[5] = generate_datetime_after_datetime(status_to_datetime[comment[1]])
            file.write(",".join(comment) + "\n")

    shares = load_shares(shares_path)
    with open(shares_path, "w") as file:
        file.write(get_share_header() + "\n")
        for share in shares:
            share[2] = generate_datetime_after_datetime(status_to_datetime[share[0]])
            file.write(",".join(share) + "\n")

    reactions = load_reactions(reactions_path)
    with open(reactions_path, "w") as file:
        file.write(get_reaction_header() + "\n")
        for reaction in reactions:
            reaction[3] = generate_datetime_after_datetime(status_to_datetime[reaction[0]])
            file.write(",".join(reaction) + "\n")


if __name__ == '__main__':
    adjust_date_time("dataset/test_statuses.csv", "dataset/test_comments.csv", "dataset/test_shares.csv",
                     "dataset/test_reactions.csv")
