"""
Author @ Villaire A. Pierre

A wordle clone
The most basic objective is to have the game generate a random word and give the user chances at __guessing that word. 
"""

from bs4 import BeautifulSoup as bs
from PyDictionary import PyDictionary as pdc
import os,string,random
import urllib.request as rq

class Bordle():

    __CPU:string
    __guess:string
    __turns:int
    __hintLimit:int 

    def __init__(self):
        self.__turns = 6
        self.hintLimit = 1

    """get random word for game"""
    def getBordle(self):
        try:
            with open("content/urls") as urls:
                options = list(urls.read())
                url = random.choice(options)
                req = rq.open(url)
                soup = bs(req.read(), "html.parser")
                
                for e in soup(["script","style"]): 
                    e.extract()
                txt = list(soup.get_text(strip=True))
                self.__CPU = random.choice(txt)
        except Exception:
            with open("content/local.txt") as local:
                options = list(local.read())
                self.__CPU = random.choice(options)


    """display a hint to the user"""
    def getHint(self):
        print("Hint Requested!")
        print("What hint would you like?\n")
        ans = input("Please enter \"d\" for a definition of the word or \"r\" to reveal a random letter in the word! Quit with \"q\"\n").lower()

        if not isinstance(ans,str):
            print("Sorry I didnt understand that!")
            #return False
        if self.__hintLimit < 1:
            print("Sorry You are all out of hints!\n")
            #return False
        else:
            while self.hintLimit > 0:
                if ans not in ["d","r","q"]:
                    print("Sorry I didnt understand that.")
                    print("Please enter \"d\" for a definition of the word or \"r\" to reveal a random letter in the word! Quit with \"q\"\n")
                    continue
                elif ans in "d":
                    self.define()
                elif ans in "r":
                    self.reveal()
                elif ans in "q":
                    print("Quitting!")
                    break
                else:
                    print("Sorry I still do not understand! Exiting...")
                    #return False
        #return True


    def define(self):
        definition = pdc.meaning(self.__CPU)
        print("The definition of the word is as follows!\n")
        for defi in definition:
            print(definition[defi])
        self.__hintLimit = 0

    
    def reveal(self):
        hint = random.randint(0,len(self.__CPU))
        print("The word contains the letter ", self.__CPU[hint])
        self.__hintLimit = 0


    """display starting message"""
    def displayIntroMessage():
        print("\n\nWELCOME TO BORDLE!")
        print("Todays we have a 5 letter word for you to __guess!")
        print("You have 6 tries to guess the word!\n\n")


    """compute the ordinal"""
    def ordinal(turns:int)->str:
        if turns == 1:
            ordinal = "'st"
        elif turns == 2:
            ordinal = "'nd"
        else:
            ordinal = "'th"
        return ordinal


    """display the results of a wrong guess"""
    def display(self):
        response = ""
        good = "✅ "
        bad = "❎"
        included = "~" 

        for i in range(len(self.__CPU)):
            if self.__guess[i] == self.__CPU[i]:
                response+=good
            elif self.__guess[i] in self.__CPU:
                response+=included
            else:
                response+=bad

        print(self.__guess)
        print(response)


    """
    validate the guess the user gives
    returns a boolean value if the guess is valid or not
    """
    def validate_guess(self) -> bool:
        self.__guess = self.__guess.lower()
        if len(self.__guess) != len(self.__CPU):
            print("Please enter a", len(self.__CPU), "letter word!\n")

        if True in [char.isdigit() for char in self.__guess]:
            print("Sorry! Numbers are not allowed!")


    """start the game"""
    def bordleStart(self):
        while(self.__turns > 0):
            self.__guess = input("Please Enter Your Guess! Enter \"h\" If You Would Like a Hint!")
            if not self.validate_guess():
                print("Sorry ")
            if self.__guess == "h":             
                self.getHint()
                continue

            if self.__guess == self.__CPU:
                print("CONGRATULATIONS, YOU WIN! THE WORD WAS", self.__CPU)
                print("PLAY AGAIN? (y/n)")
                ans = input().lower()
                
                if ans not in "y":
                    print("THANKS FOR PLAYING.\n GOODBYE!")
                    break
                else:
                    self.reset()
                    continue
            else:
                self.display()
                self.__turns -= 1


    """reset the game if user wants to play again"""
    def reset(self):
        self.turns = 6
        self.hintLimit = 1
    
    
    def game_end():
        pass
    

    """prototype to record stats"""
    def record_stats(self):
        pass