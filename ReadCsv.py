import csv

users = {} # This keeps all the users and their average star points.
businesses = {} # This keeps all the business ids and their average star points.
reviews = {} # Business ids and the users who share post about this business and their comments and the star points.



groups = {}
element_numbers_of_each_group = {}
group_freq = {}
vocab = {}

global number_of_reviews
global sum_of_star_points
global average_star_point_of_all
global number_of_all_groups



def csv_user_reader(file_obj):
    """
    Read a csv file
    """
    reader = csv.reader(file_obj)
    for row in reader:
        users[row[0]] = row[1]

def csv_business_reader(file_obj):
    """
    Read a csv file
    """
    reader = csv.reader(file_obj)
    for row in reader:
        businesses[row[0]] = row[3]

def csv_review_reader(file_obj):
    number_of_reviews = 0
    sum_of_star_points = 0
    """
    Read a csv file
    """
    reader = csv.reader(file_obj)
    for row in reader:
        #row[0] is user id
        #row[1] is business id that the user whose id is row[0], talked about.
        #row[2] is the comment of the user.
        #row[3] is the given star point to the business by the user.
        number_of_reviews += 1
        sum_of_star_points += float(row[3])

        if row[1] not in reviews:
            reviews[row[1]] = {}
            if row[0] not in reviews[row[1]]:
                comment_plus_starPoint = ""
                comment_plus_starPoint += row[2]
                comment_plus_starPoint += " *Star_Point_Of_The_Comment_is* "
                comment_plus_starPoint += row[3]
                reviews[row[1]][row[0]] = []
                reviews[row[1]][row[0]].append(comment_plus_starPoint)
            else:
                comment_plus_starPoint = ""
                comment_plus_starPoint += row[2]
                comment_plus_starPoint += " *Star_Point_Of_The_Comment_is* "
                comment_plus_starPoint += row[3]
                reviews[row[1]][row[0]].append(comment_plus_starPoint)
        else:
            if row[0] not in reviews[row[1]]:
                comment_plus_starPoint = ""
                comment_plus_starPoint += row[2]
                comment_plus_starPoint += " *Star_Point_Of_The_Comment_is* "
                comment_plus_starPoint += row[3]
                reviews[row[1]][row[0]] = []
                reviews[row[1]][row[0]].append(comment_plus_starPoint)
            else:
                comment_plus_starPoint = ""
                comment_plus_starPoint += row[2]
                comment_plus_starPoint += " *Star_Point_Of_The_Comment_is* "
                comment_plus_starPoint += row[3]
                reviews[row[1]][row[0]].append(comment_plus_starPoint)

    global average_star_point_of_all
    average_star_point_of_all = sum_of_star_points/number_of_reviews


def csv_writer(data, path):
    """
    Write data to a CSV file path
    """
    with open(path, "w") as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        for line in data:
            writer.writerow(line)



# def normalizeTheReviews():
#     global lines
#     lines = []
#     global average_star_point_of_all
#     for i in reviews.keys():
#         for j in reviews[i].keys():
#             u = float(users[j])# The average star point that is given by the user whose id is j.
#             r = float(businesses[i])-average_star_point_of_all #Business' star point mines average star point of all comments.
#             c = float(reviews[i][j][0].split(" *Star_Point_Of_The_Comment_is* ")[1])
#             #Star point of the review whose star point is going to be normalized.
#             x = u + r + c # Normalized star point of the review.
#             one_line = ""
#             one_line += i
#             one_line += ","
#             one_line += j
#             one_line += ","
#             one_line += reviews[i][j][0].split(" *Star_Point_Of_The_Comment_is* ")[0]
#             one_line += ","
#             one_line += str(x)
#             lines.append(one_line.strip().split(","))
#
#     csv_writer(lines,"review_normalized.csv")


def calculate_Naive_Bayes(words):
    global result
    global max
    max = 0
    global max_sense
    max_sense=""
    number_of_all_groups = number_of_reviews
    for group in groups:
        result = 1
        result *= group_freq[group]/number_of_all_groups
        for word in words:
            if word in vocab:
                if groups[group][word] is 0:
                    result *= 1/(element_numbers_of_each_group[group]+len(vocab))
                else:
                    result *= (groups[group][word]+1)/(element_numbers_of_each_group[group]+len(vocab))

            if result>max:
                max = result
                max_sense = group
                


    return

def test_data_for_naive_bayes():

    return

def train_data_for_naive_bayes():
    groups["negative"] = {}
    groups["notr"] = {}
    groups["positive"] = {}
    element_numbers_of_each_group["negative"] = 0
    element_numbers_of_each_group["notr"] = 0
    element_numbers_of_each_group["positive"] = 0
    group_freq["negative"] = 0
    group_freq["notr"] = 0
    group_freq["positive"] = 0
    for i in reviews.keys():
        for j in reviews[i].keys():
            rating_of_revies = float(reviews[i][j][0].split(" *Star_Point_Of_The_Comment_is* ")[1])
            review = reviews[i][j][0].split(" *Star_Point_Of_The_Comment_is* ")[0]
            if (rating_of_revies >= 0) and (rating_of_revies < 2):
                group_freq["negative"] += 1
                #group1
                words = review.split(" ")
                for element in words:
                    element_numbers_of_each_group["negative"] += 1
                    if element not in vocab:
                        vocab[element] = 1
                    if element in groups["negative"]:
                        groups["negative"][element] += 1
                    else:
                        groups["negative"][element] = 1
            elif (rating_of_revies >= 2) and (rating_of_revies <= 3):
                group_freq["notr"] += 1
                #group2
                words = review.split(" ")
                for element in words:
                    element_numbers_of_each_group["notr"] += 1
                    if element not in vocab:
                        vocab[element] = 1
                    if element in groups["notr"]:
                        groups["notr"][element] += 1
                    else:
                        groups["notr"][element] = 1
            elif (rating_of_revies > 3) and (rating_of_revies <= 5):
                group_freq["positive"] += 1
                #group3
                words = review.split(" ")
                for element in words:
                    element_numbers_of_each_group["positive"] += 1
                    if element not in vocab:
                        vocab[element] = 1
                    if element in groups["positive"]:
                        groups["positive"][element] += 1
                    else:
                        groups["positive"][element] = 1

    return

if __name__ == "__main__":
    csv_path = "user.csv"
    with open(csv_path, "r") as f_obj:
        csv_user_reader(f_obj)

    csv_path = "business.csv"
    with open(csv_path, "r") as f_obj:
        csv_business_reader(f_obj)

    csv_path = "review.csv"
    with open(csv_path, "r") as f_obj:
        csv_review_reader(f_obj)

    #normalizeTheReviews()
    train_data_for_naive_bayes()
