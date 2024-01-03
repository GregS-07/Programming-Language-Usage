import pandas as pd 
import PySimpleGUI as psg
import matplotlib.pyplot as plt 
from typing import List
import time
from datetime import datetime

languageList = [
    "Abap", "Ada", "C/C++", "C#", "Cobol", "Dart", "Delphi/Pascal", "Go", "Groovy",
    "Haskell", "Java", "JavaScript", "Julia", "Kotlin", "Lua", "Matlab", "Objective-C",
    "Perl", "PHP", "Powershell", "Python", "R", "Ruby", "Rust", "Scala", "Swift",
    "TypeScript", "VBA", "Visual Basic"
]

themes = ["Black", "DarkAmber", "Tan", "Topanga", "Reddit", "Default"]

def createWindow(): 
    # layout = [
    #     [psg.Menu([["Theme", themes]])],
    #     [psg.Text("Programming Language Popularity", font=("Helvetica", 25), justification="center")],
    #     [psg.Text("Languages", justification="left"), psg.Input(justification="left", key="-LANGS-", default_text="Python,Ada...")],
    #     [psg.Text("Starting Date", justification="left"), psg.Input(justification="right", key="-START-", default_text="YYYY-MM")],
    #     [psg.Text("Ending Date"), psg.Input(key="-END-", default_text="YYYY-MM")],
    #     [psg.Button("Enter", key="-ENTER-")]   
    # ]
    layout = [
        [psg.Menu([["Theme", themes]])],

        [psg.Text("Programming Language Popularity", font=("Helvetica", 25), justification="center")],

        # Language input row
        [psg.Text("Languages", size=(15, 1), justification="left"), 
        psg.Input(size=(30, 1), justification="left", key="-LANGS-", default_text="Python, Ada...")],

        [psg.Text("Starting Date", size=(15, 1), justification="left"), 
        psg.Input(size=(30, 1), justification="left", key="-START-", default_text="YYYY-MM")],

        [psg.Text("Ending Date", size=(15, 1), justification="left"), 
        psg.Input(size=(30, 1), justification="left", key="-END-", default_text="YYYY-MM")],

        [psg.Checkbox("Auto-Export", default=True, key="-EXPORT-")],

        [psg.Button("Enter", key="-ENTER-", size=(10, 1), pad=((0, 0), (10, 10)))],
    ]

    return psg.Window("Language Popularity", layout)

window = createWindow()

df = pd.read_csv("languages.csv")
df["Date"] = pd.to_datetime(df["Date"])
def plotGraph(langs, start, end):
    filteredDf = df[(df["Date"] >= start) & (df["Date"] <= end)]
    endDf = filteredDf[langs + ["Date"]]
    print(endDf)
    for lang in langs:
        print(lang)
        plt.plot(endDf["Date"], endDf[lang], label=lang)
    plt.xlabel("Date (YYYY-MM)")
    plt.ylabel("Use (%)")
    plt.title(f"Popularity of {', '.join(langs)}")
    plt.legend()
    if values["-EXPORT-"]:
        plt.savefig(f"{'_'.join(langs)}_popularity_{datetime.now().strftime('%H_%M_%S')}.png")
    plt.show()

def errorPopup(err: str):
    psg.popup_error(f"There has been an error. {err}")

while True:
    event, values = window.read()
    if event == psg.WIN_CLOSED or event == "Exit":
        break
    
    if event == "-ENTER-":
        error = False
        langs = values["-LANGS-"].split(",")
        langs = [lang.strip().capitalize() for lang in langs]
        def replaceArr(langs: List[str], replacementString: str, caseString: str) -> List[str]:
            return list(map(lambda x: replacementString if x == caseString else x, langs))
        for lang in langs:
            if lang not in languageList:
                match lang:
                    case "C":
                        langs = replaceArr(langs, "C/C++", "C")
                    case "C++":
                        langs = replaceArr(langs,"C/C++","C++")
                    case "Pascal":
                        langs = replaceArr(langs,"Delphi/Pascal","Pascal")
                    case "Delphi":
                        langs = replaceArr(langs,"Delphi/Pascal","Delphi")
                    case "Javascript":
                        langs = replaceArr(langs,"JavaScript","Javascript")
                    case "Js":
                        langs = replaceArr(langs,"JavaScript","Js")
                    case "Php":
                        langs = replaceArr(langs,"PHP","Php")
                    case "Visual basic":
                        langs = replaceArr(langs,"Visual Basic","Visual basic")
                    case _:
                        errorPopup(f"{lang} was not found in the dataset.")
                        error = True
        
        startDate = values["-START-"]
        try:
            if int(startDate.split("-")[0]) < 2004 or int(startDate.split("-")[0]) > 2023:
                errorPopup("The year is not within 2004-2023.")
                error = True
            elif int(startDate.split("-")[1]) < 1 or int(startDate.split("-")[1]) > 12:
                errorPopup("The month is not within 1-12.")
                error = True
            endDate = values["-END-"]
            if int(endDate.split("-")[0]) < 2004 or int(endDate.split("-")[0]) > 2023:
                errorPopup("The year is not within 2004-2023.")
                error = True
            elif int(endDate.split("-")[1]) < 1 or int(endDate.split("-")[1]) > 12:
                errorPopup("The month is not within 1-12.")
                error = True
        except:
            errorPopup("Make sure the date follows the YYYY-MM date format.")
            error = True
        if not error:
            plotGraph(langs, startDate, endDate)
    
    if event in themes:
        window.close()
        psg.theme(event.lower())
        window = createWindow()
window.close()



