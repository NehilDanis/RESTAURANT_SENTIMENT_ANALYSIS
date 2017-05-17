from PorterStemmer import *
import re
import math

vocab = []#This is an array for the unique vocabulary.
p = PorterStemmer()#Here the porter stemmer is initialized.
number_of_total_senses = 0#This variable keeps the total number of senses.
senses = {}#This dictionary is to keep the number of existance of all different senses.
training_set = {}#This is going to be a nested dictionary.
sense_word = {}
cosine_similarity_dict = {}
unique_vocab = {}
count = 0
result_text = ""
word1 = ""#The first word to be compared.
word2 = ""#The second word to be compared.
total_document = ""#This is to keep all the sentences under one example.


#Here the output file işs created.
def print_out(line):
    output_file = open("output.txt","a")
    output_file.write(line)
    output_file.close()
    return

#This function is used to use stemmer.
def stemm(line,words):
    element = ''
    for c in line:
        if c.isalpha():
            element += c.lower()
        else:
            if element:
                element = p.stem(element, 0,len(element)-1)
                if element not in words:
                    words.append(element)
                element = ''
    return words


def train():

    global total_document
    global count
    global number_of_total_senses
    global control_blank_lines
    global file_length
    global line_counter

    control_blank_lines=0

    with open('train.txt') as trainFile:
        content = trainFile.readlines()
        file_length=len(content)
        line_counter=0
    for line in content:
        line_counter += 1
        if line!="\n":
            if count is 0:
                control_blank_lines=0
                number_of_total_senses += 1# Here we kept track of all senses.
                count=1
            else:
                line = line.lower()
                line=line.replace("<tag ","<tag")
                total_document+=line.strip()#All sentences that belong to the same example, added to each other.
                if line_counter==file_length:
                    item = re.findall( r'<.+>.+</>',total_document)
                    tag=item[0].split('"')#tag[1] gives the sense of that example.
                    disambiguated=tag[2].split(">")
                    disambiguated[1]=disambiguated[1].replace("</","")#disambiguated[1] gives the tagged word in the example text.
                    total_document = total_document.replace(item[0],"\0")#The tagged string is removed from total document for that example.
                    words = []
                    words = stemm(total_document,words)#Here the porter stemmer is used.

                    #This if else block is to keep the number of senses.
                    if tag[1] in senses:
                        senses[tag[1]] += 1
                    else:
                        senses[tag[1]] = 1

                    if tag[1] not in sense_word:
                        sense_word[tag[1]] = 0

                    if disambiguated[1] not in training_set:
                        training_set[disambiguated[1]]= {}
                        training_set[disambiguated[1]][tag[1]] = {}
                        for item in vocab:
                            training_set[disambiguated[1]][tag[1]][item] = 0
                    else:
                        if tag[1] not in training_set[disambiguated[1]]:
                            training_set[disambiguated[1]][tag[1]] = {}
                            for item in vocab:
                                training_set[disambiguated[1]][tag[1]][item] = 0

                    for v in words:
                        if v in training_set[disambiguated[1]][tag[1]]:
                            sense_word[tag[1]] += 1
                            training_set[disambiguated[1]][tag[1]][v] += 1


                    total_document=""
                    count = 0

        else:
            if control_blank_lines is 0:
                control_blank_lines = 1
                item = re.findall( r'<.+>.+</>',total_document)
                tag=item[0].split('"')#tag[1] gives the sense of that example.
                disambiguated=tag[2].split(">")
                disambiguated[1]=disambiguated[1].replace("</","")#disambiguated[1] gives the tagged word in the example text.
                total_document = total_document.replace(item[0],"\0")#The tagged string is removed from total document for that example.
                words = []
                words = stemm(total_document,words)#Here the porter stemmer is used.

                #This if else block is to keep the number of senses.
                if tag[1] in senses:
                    senses[tag[1]] += 1
                else:
                    senses[tag[1]] = 1

                if tag[1] not in sense_word:
                    sense_word[tag[1]] = 0

                if disambiguated[1] not in training_set:
                    training_set[disambiguated[1]]= {}
                    training_set[disambiguated[1]][tag[1]] = {}
                    for item in vocab:
                        training_set[disambiguated[1]][tag[1]][item] = 0
                else:
                    if tag[1] not in training_set[disambiguated[1]]:
                        training_set[disambiguated[1]][tag[1]] = {}
                        for item in vocab:
                            training_set[disambiguated[1]][tag[1]][item] = 0

                for v in words:
                    if v in training_set[disambiguated[1]][tag[1]]:
                        sense_word[tag[1]] += 1
                        training_set[disambiguated[1]][tag[1]][v] += 1


                total_document=""
                count = 0

    count = 0 #The count is setted zero for further usage.
    return

#Here the naive bayes is calculated.
def calculateNaiveBayes(exampleNumber,disambiguatedWord,words):
    global result
    global max
    max = 0
    global max_sense
    max_sense=""
    if disambiguatedWord in training_set:
        for sense in training_set[disambiguatedWord]:
            result = 1
            result *= senses[sense]/number_of_total_senses
            for word in words:
                if word in vocab:
                    if training_set[disambiguatedWord][sense][word] is 0:
                        result *= 1/(sense_word[sense]+len(vocab))
                    else :
                        result *= (training_set[disambiguatedWord][sense][word]+1)/(sense_word[sense]+len(vocab))

            if result>max:
                max = result
                max_sense = sense

    print_out(exampleNumber+" "+max_sense+"\n")

    return

#This function is to test the trained data.
def test():
    global result_text
    global count
    global control_blank_lines
    global file_length
    global line_counter
    control_blank_lines=0

    with open('test.txt') as testFile:#Test file is read in here.
        content = testFile.readlines()
        file_length=len(content)
        line_counter=0
    for line in content:
        line_counter += 1
        if line!="\n":
            if count is 0:
                control_blank_lines=0
                exampleNumber=line.strip()
                count=1
            else:
                line = line.lower()
                result_text+=line.strip()
                if line_counter==file_length:
                    item = re.findall( r'<tag>.+</>',result_text)
                    if len(item)>=1:
                        element=item[0].split(">")
                        disambiguated=element[1].split("<")

                    words=[]
                    words = stemm(result_text,words)#Porter stemmer is used.


                    calculateNaiveBayes(exampleNumber,disambiguated[0],words)#This function is called to calculate
                    #naive bayes.

                    result_text=""
                    count = 0


        else:
            if control_blank_lines is 0:
                control_blank_lines=1
                item = re.findall( r'<tag>.+</>',result_text)
                if len(item)>=1:
                    element=item[0].split(">")
                    disambiguated=element[1].split("<")

                words=[]
                words = stemm(result_text,words)#Porter stemmer is used.


                calculateNaiveBayes(exampleNumber,disambiguated[0],words)#This function is called to calculate
                #naive bayes.


                result_text=""
                count = 0


    count = 0
    return


#Here, the text file to find cosine similarity is read.
def read_cosine_similarity():
    global count
    global count_word
    global cosine_word
    global word1,word2
    global arrayOfWords
    global newLine
    newLine = ""
    arrayOfWords = []
    count_word = 0
    cosine_word = ""
    with open('cosine.txt') as cosineFile:
        content = cosineFile.readlines()
    for line in content:
        if line is not "\n":
            line = line.lower()
            if count is 0:
                count = 1
                line = line.strip()
                line = line[0:len(line)-1]
                cosine_word = line
                if count_word is 0:
                    word1 = cosine_word
                    count_word = 1
                else:
                    word2 = cosine_word
            else:
                line = line.strip()
                elements = line.split(" ")
                for item in elements:
                    if item[len(item)-1] is '.' or item[len(item)-1] is ',' or item[len(item)-1] is '?' or item[len(item)-1] is '!':
                        item = item[0:len(item)-1]
                        newLine += str(item)
                        newLine += str(" ")
                    else:
                        newLine += str(item)
                        newLine += str(" ")

                arrayOfWords = stemm(newLine,arrayOfWords)
                index = arrayOfWords.index(cosine_word)
                temp1 = index
                temp2 = index
                i = 1
                if index>=3 and len(arrayOfWords)-1-index>=3:
                    while i<=3:
                        if arrayOfWords[temp1-i] not in unique_vocab:
                            unique_vocab[arrayOfWords[temp1-i]] = 0
                        if arrayOfWords[temp2+i] not in unique_vocab:
                            unique_vocab[arrayOfWords[temp2+i]] = 0
                        i += 1
                elif index<3 and len(arrayOfWords)-1-index<3:
                    temp1 -= 1
                    temp2 += 1
                    while temp1>=0:
                        if arrayOfWords[temp1] not in unique_vocab:
                            unique_vocab[arrayOfWords[temp1]] = 0
                        temp1 -= 1
                    while temp2<=(len(arrayOfWords)-1):
                        if arrayOfWords[temp2] not in unique_vocab:
                            unique_vocab[arrayOfWords[temp2]] = 0
                        temp2 += 1

                elif index>=3 and len(arrayOfWords)-1-index<3:
                    temp2 += 1
                    while i<=3:
                        if arrayOfWords[temp1-i] not in unique_vocab:
                            unique_vocab[arrayOfWords[temp1-i]] = 0
                        i += 1
                    while temp2<=(len(arrayOfWords)-1):
                        if arrayOfWords[temp2] not in unique_vocab:
                            unique_vocab[arrayOfWords[temp2]] = 0
                        temp2 += 1

                elif index<3 and len(arrayOfWords)-1-index>=3:
                    temp1 -= 1
                    while temp1>=0:
                        if arrayOfWords[temp1] not in unique_vocab:
                            unique_vocab[arrayOfWords[temp1]] = 0
                        temp1 -= 1
                    while i<=3:
                        if arrayOfWords[temp2+i] not in unique_vocab:
                            unique_vocab[arrayOfWords[temp2+i]] = 0
                        i += 1
                arrayOfWords = []
                newLine = ""

        else :
            count = 0

    return

#To calculate the cosine similarity here a unique vocab is created.
def assign_cosine_similarity():
    global count
    global count_word
    global cosine_word
    global word1,word2
    global arrayOfWords
    global newLine

    cosine_similarity_dict[word1] = {}
    cosine_similarity_dict[word2] = {}

    for key in unique_vocab.keys():
        cosine_similarity_dict[word1][key]=0
        cosine_similarity_dict[word2][key]=0

    newLine = ""
    arrayOfWords = []
    count_word = 0
    cosine_word = ""
    with open('cosine.txt') as cosineFile:
        content = cosineFile.readlines()
    for line in content:
        if line is not "\n":
            line = line.lower()
            if count is 0:#Here the  word which is going to be compared  with the other word for finding cosine similarity.
                count = 1
                line = line.strip()
                line = line[0:len(line)-1]
                cosine_word = line
                if count_word is 0:
                    word1 = cosine_word#First word to be compared.
                    count_word = 1
                else:
                    word2 = cosine_word#Second word to be compared.
            else:
                line = line.strip()
                elements = line.split(" ")
                for item in elements:
                    if item[len(item)-1] is '.' or item[len(item)-1] is ',' or item[len(item)-1] is '?' or item[len(item)-1] is '!':
                        item = item[0:len(item)-1]
                        newLine += str(item)
                        newLine += str(" ")
                        newLine += str(" ")
                    else:
                        newLine += str(item)
                        newLine += str(" ")

                arrayOfWords = stemm(newLine,arrayOfWords)
                index = arrayOfWords.index(cosine_word)
                temp1 = index
                temp2 = index
                i = 1
                #Down below is for the finding the window of words.(+-3)
                if index>=3 and len(arrayOfWords)-1-index>=3:
                    while i<=3:
                        if arrayOfWords[temp1-i] in cosine_similarity_dict[cosine_word]:
                            cosine_similarity_dict[cosine_word][arrayOfWords[temp1-i]] += 1
                        if arrayOfWords[temp2+i] in cosine_similarity_dict[cosine_word]:
                            cosine_similarity_dict[cosine_word][arrayOfWords[temp2+i]] += 1
                        i += 1
                elif index<3 and len(arrayOfWords)-1-index<3:
                    temp1 -= 1
                    temp2 += 1
                    while temp1>=0:
                        if arrayOfWords[temp1] in cosine_similarity_dict[cosine_word]:
                            cosine_similarity_dict[cosine_word][arrayOfWords[temp1]] += 1
                        temp1 -= 1
                    while temp2<=(len(arrayOfWords)-1):
                        if arrayOfWords[temp2] in cosine_similarity_dict[cosine_word]:
                            cosine_similarity_dict[cosine_word][arrayOfWords[temp2]] += 1
                        temp2 += 1

                elif index>=3 and len(arrayOfWords)-1-index<3:
                    temp2 += 1
                    while i<=3:
                        if arrayOfWords[temp1-i] in cosine_similarity_dict[cosine_word]:
                            cosine_similarity_dict[cosine_word][arrayOfWords[temp1-i]] += 1
                        i += 1
                    while temp2<=(len(arrayOfWords)-1):
                        if arrayOfWords[temp2] in cosine_similarity_dict[cosine_word]:
                            cosine_similarity_dict[cosine_word][arrayOfWords[temp2]] += 1
                        temp2 += 1

                elif index<3 and len(arrayOfWords)-1-index>=3:
                    temp1 -= 1
                    while temp1>=0:
                        if arrayOfWords[temp1] in cosine_similarity_dict[cosine_word]:
                            cosine_similarity_dict[cosine_word][arrayOfWords[temp1]] += 1
                        temp1 -= 1
                    while i<=3:
                        if arrayOfWords[temp2+i] in cosine_similarity_dict[cosine_word]:
                            cosine_similarity_dict[cosine_word][arrayOfWords[temp2+i]] += 1
                        i += 1

                arrayOfWords = []
                newLine = ""
        else :
            count = 0





    return

#Here the cosine similarity between word1 and word2 is calculated.
def calculate_cosine_similarity():
    global square_of_word1
    global square_of_word2
    square_of_word1 = 0
    square_of_word2 = 0
    mult_of_words = 0

    for v in unique_vocab:
        square_of_word1 += (cosine_similarity_dict[word1][v]*cosine_similarity_dict[word1][v])
        square_of_word2 += (cosine_similarity_dict[word2][v]*cosine_similarity_dict[word2][v])
        mult_of_words += ((cosine_similarity_dict[word1][v]*cosine_similarity_dict[word2][v]))

    square_of_word1 = math.sqrt(square_of_word1)
    square_of_word2 = math.sqrt(square_of_word2)

    result_similarity = mult_of_words/(square_of_word1*square_of_word2)

    print_out("\n\nSimilarity between "+word1+" and "+ word2+" is "+str(result_similarity)+"\n")

    return


#Down below the vocabulary file is read.
vocabfile = open("vocabulary.txt", 'r')
while 1:
    output = ''
    word = ''
    line = vocabfile.readline()
    if line == '':
        break
    for c in line:
        if c.isalpha():
            word += c.lower()#Each character used after they turned into lower case.
        else:
            if word:
                word = p.stem(word, 0,len(word)-1)#Porter stemmer is used.
                if word not in vocab:#If the word is not already in the list then the word is added.
                    vocab.append(word)
                word = ''
vocabfile.close()

train()#This line is to train the program
test()#By using probability variables that are calculated by training the data, the test data is tested.
read_cosine_similarity()#This function is called to read the input file for the second task.
assign_cosine_similarity()#To calculate the cosine similarity here a unique vocab is created.
calculate_cosine_similarity()#Here the cosine similarity between two words are calculated.
