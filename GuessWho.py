"""
    Guess Who

       This program will simulate a person guessing game.  The game will begin
    by prompting the user to read the intstructions and to see a list of the
    people that it can guess.  Once the user is ready, the game will begin.
    The game will then determine which country your person is from and then
    ask a series of yes or no questions to narrow it down.  Once it thinks
    it has a guess, it will make one.  If it is wrong, the user will have a
    change to tell the game who they were thinking of, and the game will learn
    and store that information for later.  Finally, the game will give the user
    the option to play again.

    Last Updated: 9/23/2021
"""

import json
import random


#   Names of the files containing candidates and questions
ENG_FNAME  = "EngGuess.txt"
AMER_FNAME = "USGuess.txt"
CAN_FNAME  = "CanGuess.txt"
QUES_FNAME = "QuestionList.txt"


def pre_game():
    """
    This sets up a few things before the game begins.  This function will
    get the names of all the remembered candidates from each country.  It will
    also display those candidates and instructions if the user asks to see
    them.

    Parameters: N/A

    Returning: N/A
    """
    
    print("\n{: ^80}".format("Guess Who\n"))
    print("================================================================" +
          "================")
    print("Would you like to read the instructions first?")
    
    eng, amer, canad = get_names()
    
    print_instrs()
    print_figs(eng, amer, canad)

    print("\n{: ^80}".format("The Game") )
    print("================================================================" +
          "================")



def get_names():
    """
    This function will open the three files containing the list of possible
    candidates and store them to respective lists.  If the one of the files
    cannot be found, then an appropriate message will be displayed.

    Parameters: N/A
        
    Returning: 3 lists containing the candidates from each country.
    """
    
    english, american, canadian = [],[],[]

    try:
        infile = open(ENG_FNAME, "r")
        for line in infile:
            english.append(line.strip())
        infile.close()

        infile = open(AMER_FNAME, "r")
        for line in infile:
            american.append(line.strip())
        infile.close()
            
        infile = open(CAN_FNAME, "r")
        for line in infile:
            canadian.append(line.strip())
        infile.close()
        pass
    except IOError as excep:
        print("Not such file or directory exists, closing the program.")
        exit
    
    return english, american, canadian



def validate_ans():
    """
    This function will ensure that the only accpetable answer is either "Yes"
    or "No".  If the user enters something different, they will be prompted
    to enter an appropriate answer.

    Parameters: N/A

    Returning: string containing the appropriate answer (ans)
    """
    
    ans = ""
    while True:
        if ans != "YES" and ans != "NO":
            print("Please enter 'Yes' or 'No'")
            ans = input().upper()
            print()
            continue
        else:
            break
    return ans



def print_instrs():
    """
    This function will print a short paragraph that will describe the
    instructions of the guessing game.

    Parameters: N/A

    Returning: N/A
    """
    
    ans = validate_ans()
    if ans == "YES":
        print("\n\n")
        print("{: ^90}".format(" Instructions") )
        print("==============================================================" +
              "==================")
        print("    \t\tThis game will ask the user a series of questions that ")
        print("\twill try to narrow down the person that the user is thinking")
        print("\tof based on the list figures.  The only acceptable answers to")
        print("\tthe questions are 'Yes' and 'No'.")
        print("=============================================================="
              "==================\n\n")



def print_figs(english, american, canadian):
    """
    This function will print each candidate that it has learned and where they
    are from.

    Parameters: list of candidates from England (english)
                list of candidates from the United States (american)
                list of candidates from Canada (canadian)

    Returning: N/A
    """
    
    print("Would you like to view the list of figures?")
    ans = validate_ans()

    if ans == "YES":
        ctr = 0
        print("England")
        while ctr < len(english):
           print(english[ctr], end = "\n")
           ctr = ctr + 1
           
        ctr = 0
        print("\nUnited States")
        while ctr < len(american):
            print(american[ctr], end = "\n")
            ctr = ctr + 1
            
        ctr = 0
        print("\nCanada")
        while ctr < len(canadian):
            print(canadian[ctr], end = "\n")
            ctr = ctr + 1

    input("\nPress enter to start the game")    



def get_questions():
    """
    This function will store the list of questions from the file containing
    them along with their answers.
    
    Parameters: N/A

    Returning: returning the list of questions from the file (ques)
    """
    
    ques = []
    
    try:
        with open(QUES_FNAME) as data:
            ques = json.load(data)
        pass
    except IOError as excep:
        print("No such file or directory exists, closing the program.")
        exit
    data.close()
    
    return ques



def get_line(ctr):
    """
    This function will randomly choose a winning line for the game to say
    to the user after it has made a successful guess.

    Parameters: variable containing the number of questions asked (ctr)

    Returning: N/A
    """
    
    rand_num = random.randint(1,2)
    if rand_num == 1:
        print("I knew it!  It only took me", ctr, "questions.")
    elif rand_num == 2:       
        print("That one was easy.  It only took me", ctr,
                "questions.")



def learn(ques_list, guess, curr, branch):
    """
    This function learn about the person the user is thinking of.  It will
    first ask who they are, and then prompt for a question to ask about them.
    It will then update the appropriate file with the new information.

    Parameters: The list of questions to ask (ques_list)
                The game's guess (guess)
                The current position (curr)
                The next position (branch)
                
    Returning: The name of the person the user has supplied (person)
    """
    
    print("Who is it?")
    person = input()
    print("Interesting.  Give me a question that would've been " +
          "true for ", person, ".")
    newQ = input()
                
    ques_list.append([newQ, person, guess])
    ques_list[curr][branch] = len(ques_list)-1

    try:
        with open(QUES_FNAME, 'w') as outfile:
            json.dump(ques_list, outfile, indent=1)
        outfile.close()
        pass
    except IOError as excep:
        print("No such file or directory named", QUES_FNAME,
                          "exists, closing the program.")
        exit
    return person



def guess(ques_list, curr, branch, quest_ctr, loc_flag):
    """
    This function will be executed if the game has a guess of who the user
    is thinking of.  If the game is correct, then it will print how many
    questions it took and end the game.  If it is not correct, then it will
    prompt the user to enter the person's name and to give a question about
    them so that the game can learn.  Finally this function will ask the user
    if they wish to play again and return their answer.  

    Parameters: The list of questions to ask (ques_list)
                The current position (curr)
                The next position (branch)
                The number of questions asked (quest_ctr)
                Indicator of the country of origin (loc_flag)                

    Returning:
    """
    guess = str(ques_list[curr][branch])
    print("You are thinking of", guess, "\nAm I right?", end = " ")
    ans = validate_ans()

    # If we guessed correctly    
    if ans == "YES":
        get_line(quest_ctr)
        not_yet = False

    # If we did not guess correctly, add the person and a question
    # about them to the files       
    elif ans == "NO":
        person = learn(ques_list, guess, curr, branch)
        add_fig(person, loc_flag)

    # Do you want to play again?
    print("Thanks for playing!  Do you want to play again?")
    cont = input().upper()
    return cont



def game(ques_list, quest_ctr):
    """
    This function contains the main algorithm for the game.  The game begins by
    asking the first question in the list of questions.  Depending on the answer
    the branch condition is set, to tell which node to go to next.  Then, if
    the game knows who it is, it will guess.  If the game is correct, the game
    will conclude and the user is prompted to play again.  If the game is
    wrong, the user is asked who they were thinking of along with a question
    to be stored so the game will remember the next time it is played.
    
    Parameters: The list of questions to ask (ques_list)
                The number of questions asked (quest_ctr)

    Returning: True or False depending on whether the user wishes to play again
    """
    curr, not_yet, loc_flag = 0, True, 0
    
    while not_yet:
        print(ques_list[curr][0])
        quest_ctr = quest_ctr + 1
        ans = validate_ans()

        if ans == "YES": branch = 1
        else: branch = 2

        # Determining location for appending a new name
        if ques_list[curr][branch] == 3: loc_flag = 0
        if ques_list[curr][branch] == 12: loc_flag = 1
        if ques_list[curr][branch] == 21: loc_flag = 2

        # If we have it, guess
        if isinstance (ques_list[curr][branch], str):
            cont = guess(ques_list, curr, branch, quest_ctr, loc_flag)
            
            if cont == "YES": return True
            else: return False
            
        # If we do not have it, go further down the tree        
        else:
            type(ques_list[curr][branch])
            curr = int(ques_list[curr][branch])



def add_fig(person, loc_flag):
    """
    This function will add a person to the list of candidates and update the
    file.

    Parameters: string of the new person (person)
                indicator of the country of origin (loc_flag)

    Returning: N/A
    """
    if loc_flag == 0:
        try:
            with open(ENG_FNAME, 'a') as outfile:
                outfile.write("\n" + person)
            outfile.close()
            pass
        except IOError as excep:
            print("No such file or directory named", ENG_FNAME,
                          "exists, closing the program.")
            
    elif loc_flag == 1:
        try:
            with open(AMER_FNAME, 'a') as outfile:
                outfile.write("\n" + person)
            outfile.close()
            pass
        except IOError as excep:
            print("No such file or directory named", AMER_FNAME,
                          "exists, closing the program.")      

    elif loc_flag == 2:
        try:
            with open(CAN_FNAME, 'a') as outfile:
                outfile.write("\n" + person)
            outfile.close()
            pass
        except IOError as excep:
            print("No such file or directory named", CAN_FNAME,
                          "exists, closing the program.")



# Main Function
if __name__ == "__main__":
    again = True
    while again == True:
        quest_ctr = 0
        pre_game()
        ques_list = get_questions()
        again = game(ques_list, quest_ctr)
    print("Thanks for playing!")
