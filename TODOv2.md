# TODO 

added some comment in main.py to explain what to change

## time

- save the console print of the market in logs.txt file in the same folder of output, so i can lookup for error possible easily

- all time must be in UTC Milliseconds so with 14 digits (as example 1642750097 must be 1642750097000)

- the date time must be in GMT+0 as example "01_21_2022_Alcaraz v Berrettini.json" have date 01/21/2022 08:28:17 and that value 1642750097 in date but
![time](./documentation/images/3.png?raw=true "time") 
here say that is in format GMT +1, i need al time and data in GMT+0 time, in that market as example date must be: 1642753697000 (in ms), only add 3600 (3600000 in ms)

the same rules upper here are valid for props trades.condition.time

always when you use time keep in mind the rule above

- already fixed "adds" instead of "odds"

- already fixed main.py row 139 in type of bets, it's column 31 and not 33 where we have the type of bets

- there is a typo in props selection[].avg.back.stack -> stake 

- i need to change 

    "avg": {
        "back": {
            "odds": 0,
            "stack": 0,
            "toWin": 0
        },
        "lay": {
            "odds": 0,
            "bank": 0,
            "liability": 0
        }
    }

    TO ->

    "avg": {
        "back": {
            "odds": 0,
            "stake": 0,
            "liability": 0,
            "toWin": 0
        },
        "lay": {
            "odds": 0,
            "stake": 0,
            "liability": 0,
            "toWin": 0
        }
    }

- the formula to calculate selections[].avg.back/lay don't works, i already check 

    def getAvg(block,runner,char,params=[]):

and i there is an error in that formula

the formula must be something like that

    BACK FORMULA
    {
        stake = 0
        oddsWeight = 0

        for i of backBets{ // where backBets are all the bets for that selection of type "B"
            oddsWeight += i.odds * i.stake 
            stake += i.stake
        }

        odds = oddsWeight / stake
        liability = stake
        toWin = stake*(odds-1)
    }

    LAY FORMULA
    {
        stake = 0
        oddsWeight = 0

        for i of layBets{ // where backBets are all the bets for that selection of type "L"
            oddsWeight += i.odds * i.stake 
            stake += i.stake
        }

        odds = oddsWeight / stake
        liability = stake*(odds-1)
        toWin = stake
    }


i post you and example in "02_08_2022_Rakhimova v Martic.json"
![avg1](./documentation/images/4.png?raw=true "avg1") 
![avg2](./documentation/images/5.png?raw=true "avg2") 


- currentGame props must have the values always as a string

     "currentGame": {
        "runnerA": 40,
        "runnerB": "AD",
        "server": "B"
    }

    must become

       "currentGame": {
        "runnerA": "40", // as string 
        "runnerB": "AD", // as string 
        "server": "B"
    }

- change commission formula in main.py row 95 if "UK" OR "DEMO" => 0.02, 0.05 otherwise

- id numeration if the trade must be made automatically, start from 1 in order to the last ( not taken fomr colum AB but do it via code)

# ADD TIME SET VALUE

As i added time for aFirstSet and aSecondSet in csvToExcel, now the value present in column C row 2 and 3 (if aSecondSet is present) 
i need to copy that in info.setTime props of the json

if the time are not present leave the value at null

example:

market: "Konjuh v Boulter"

    "info": {
        ...
        setTime: {
            second: 1646087471000,
            third: 1646089151000
        },
        ...
    },

![avg2](./documentation/images/6.png?raw=true "avg2") 

# ADD PARAMS VALUE

As i added some params in csvToExcel i need to copy here in the JSON

we just add a props to main object called "params"

    params: [
        {
            runnerId: number
            params1: number // =0 if not present in Excel
            params2: number
            params3: number
            params4: number
            params5: number
            params6: number
            params7: number
            params8: number
            params9: number
            params10: number
        }
    ]

copied from first row of the block, columns BN to BW for runnerA and columns BX to CG for runnerB

as example from "Alcaraz v Berrettini" i need that value:

    "params": [
            {
                "runnerId": 25215583,
                "params1": 2.45,
                "params2": 2.54,
                "params3": 6.5,
                "params4": 0,
                "params5": 0,
                "params6": 0,
                "params7": 0,
                "params8": 0,
                "params9": 0,
                "params10": 0
            },
            {
                "runnerId": 8962036,
                "params1": 4.2,
                "params2": 34.6,
                "params3": 34.5,
                "params4": 0,
                "params5": 0,
                "params6": 0,
                "params7": 0,
                "params8": 0,
                "params9": 0,
                "params10": 0
            }
        ]

![avg2](./documentation/images/7.png?raw=true "avg2") 


