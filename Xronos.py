import subprocess
import PySimpleGUI as sg

def copy2clip(txt):
    cmd='echo '+txt.strip()+'|clip'
    return subprocess.check_call(cmd, shell=True)

def multi_input():
    try:
        while True:
            data = input()
            if not data: break
            yield data
    except KeyboardInterrupt:
        return

def GetAnswerFromPosition(MainString, Position):
    CheckPosition = Position
    OpenBracketCounter = 0

    while True:
        if MultilineString[CheckPosition] != "}":
            if MultilineString[CheckPosition] == "{":
                OpenBracketCounter = OpenBracketCounter + 1
        else:
            if OpenBracketCounter == 1:
                break
            else:
                OpenBracketCounter = OpenBracketCounter - 1

        CheckPosition = CheckPosition + 1

    return MainString[Position+8:CheckPosition]

def GetAllInstancesOfString(MainString, String):
    StartIndex = 0
    ReturnTable = []

    while StartIndex != -1:
        StartIndex = MainString.find(String, StartIndex, len(MainString))

        if StartIndex != -1:
            ReturnTable.append(StartIndex)
            StartIndex = StartIndex + 1
        else:
            break

    return ReturnTable


print("Enter:")
MultilineList = list(multi_input())
MultilineString = ''.join(MultilineList)

TableOfQuestions = GetAllInstancesOfString(MultilineString, "problem-environment problem")
TableOfAnswerPositions = GetAllInstancesOfString(MultilineString, "answer {")
TableOfVectorPositions = GetAllInstancesOfString(MultilineString, "answer [")

print("--------------------------------------------------------------")
print(len(TableOfVectorPositions))

# TotalSingleChoiceIndices = GetAllInstancesOfString(MultilineString, "text-left btn btn-secondary")
# CorrectSingleChoiceIndices = GetAllInstancesOfString(MultilineString, "text-left btn-secondary correct")

TotalChoiceIndices = GetAllInstancesOfString(MultilineString, "btn text-left btn-secondary")
CorrectChoiceIndices = GetAllInstancesOfString(MultilineString, "btn text-left btn-secondary correct")
ProblemNumberIndices = GetAllInstancesOfString(MultilineString, "id=\"problem")
EveryAnswer = TableOfAnswerPositions + CorrectChoiceIndices

AnswerDictionary = {}
for i in range(len(TableOfQuestions)):
    IndexName = "Question " + str(i+1)
    AnswerDictionary[IndexName] = {
        "Type" : "",
        "Answers" : [],
        "Choices" : 0
    }

    for v in TableOfAnswerPositions:
        MaxLength = None

        if i+1 >= len(TableOfQuestions):
            MaxLength = len(MultilineString)
        else:
            MaxLength = TableOfQuestions[i+1]

        if v > TableOfQuestions[i] and v < MaxLength:
            AnswerDictionary[IndexName]["Type"] = "Free-Response"
            AnswerDictionary[IndexName]["Answers"].append(GetAnswerFromPosition(MultilineString, v))

    for v in TotalChoiceIndices:
        MaxLength = None

        if i+1 >= len(TableOfQuestions):
            MaxLength = len(MultilineString)
        else:
            MaxLength = TableOfQuestions[i+1]

        if v > TableOfQuestions[i] and v < MaxLength:
            AnswerDictionary[IndexName]["Type"] = "Choice"
            AnswerDictionary[IndexName]["Choices"] += 1

    for v in CorrectChoiceIndices:
        MaxLength = None

        if i+1 >= len(TableOfQuestions):
            MaxLength = len(MultilineString)
        else:
            MaxLength = TableOfQuestions[i+1]

        if v > TableOfQuestions[i] and v < MaxLength:
            for count, value in enumerate(TotalChoiceIndices):
                if value == v:
                    AnswerDictionary[IndexName]["Type"] = "Choice"
                    AnswerDictionary[IndexName]["Answers"].append(count+1)

TotalChoicesSum = 0
for i, v in enumerate(AnswerDictionary):
    if AnswerDictionary[v]["Type"] == "Choice":
        NewTable = []
        for answerValue in AnswerDictionary[v]["Answers"]:
            dif = answerValue - TotalChoicesSum
            NewTable.append(dif)

        AnswerDictionary[v]["Answers"] = NewTable
    TotalChoicesSum = TotalChoicesSum + AnswerDictionary[v]["Choices"]

print(AnswerDictionary)

sg.theme('DarkBlack')
layout = []

for i, v in enumerate(AnswerDictionary):
    GuiTable = [sg.Text(v + ": ")]

    if AnswerDictionary[v]["Type"] == "Free-Response":
        for Answer in AnswerDictionary[v]["Answers"]:
            GuiTable.append(sg.Button(Answer, key='AnswerButton'))
    elif AnswerDictionary[v]["Type"] == "Choice":
        for Answer in AnswerDictionary[v]["Answers"]:
            GuiTable.append(sg.Text(Answer))

    layout.append(GuiTable)

window = sg.Window('Xronos Answers', layout)
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Cancel':
        break
    else:
        copy2clip(window[event].get_text())

window.close()