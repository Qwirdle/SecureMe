from flask import *

def checkAnswers(userForm, answerKey):
    """Takes in a multiple choice web form, checks each answer, and returns a percentage of accuracy"""
    
    correct = 0

    for _, answer in enumerate(answerKey):
        if userForm.get(f"question{_ + 1}") == answer:
            correct += 1

    return (correct/len(answerKey))*100