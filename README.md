# excelToJson

The propose of that project is to convert t and excel file to some JSON file that i will upload in my personal DB

As alway we need to work for block in the excel, one single block are like that 

![block](./documentation/images/1.png?raw=true "1")
a block always start with a Date in colum B, "OPEN" in column AD (with upper "final if is not the first"), end ends at "FINAL" in column AD.

As the previous project palce path value 

```python
    path = "./InputFolder/"
    exportPath = "./OutputFiles/"
```

Every time i will run the code it will generate a subFolder in exportPath with the name "MM_DD_YYYY_hh_mm_ss" with the date of when the script is started.

Inside that folder from each block in the excel  need to generate and save a JSON file with fileName "MM_DD_YYYY_marketName.json" in the folder with the date taken from the market columns B

### Final format

That will be the final format of the JSON
```JS
{
    created: {type: Number},        // UTC millisecond timestamp when generated the file
    lastUpdate: {type: Number},     // UTC millisecond timestamp when generated the file
    trade: {
        // for that part take attention of columns from B to N
        info: {
            strategyId: {type: String}, // explained in API STRATEGY paragraph
            tennisTournamentId: {type: String}, // the ID in second row of each columns H "event"
            date: {type: Number},   // UTC millisecond timestamp of the market (get date in column A and time in column C)
            marketInfo: {
                marketName: {type: String}, // market columns D
                marketId: {type: String},   // leave empty for the moment
                marketType: {type: String},   // "MATCH_ODDS" if marketName (column D not have substring " - Set * Winner"), otherwise if have substring " - Set 1 Winner" or " - Set 2 Winner" -> "SET_WINNER"
                eventName: {type: String}, // "Match Odds" if marketName (column D not have substring " - Set * Winner"), otherwise if have substring " - Set 1 Winner" or " - Set 2 Winner" -> "Set 1 Winner" or "Set 2 Winner"
                sport: {type: String}      // always "TENNIS"
            },
            executor: [{type: String}],     // COLUMN F
            exchange: {
                name: {type: String},       // COLUMN E
                commission: {type: Number}, // IF column E contains "UK" 0.02 otherwise 0.05
            },
            note: {
                description: {type: String}, // empty
                entry: {type: String}, // merge all the comments here from column N
                exit: {type: String}, // empty
                position: {type: String}, // empty
                mm: {type: String}, // empty
                odds: {type: String}, // empty
                post: {type: String}, // empty
            }
        },
        // for that part take attention of columns from I to M
        selections: [{ // array of objet, one each for runner (runnerA in columns I and runnerB in column J)
            selectionN: {type: Number}, // sequential number of runner, 0 for runnerA, 1 for runnerB
            runnerId: {type: Number},   // the third row in columns name, if empty CALL THE API TO RETRIVE ID, i explain that in point API RUNNER
            runnerName: {type: String}, // the name of the runner, first row in column I or J
            winner: {type: Boolean}, // if the runnerName is the same name in column K true, false otherwise
            bsp: {type: Number}, // the second row of the columns of runner I or J
            sets: {
                secondSet: {type: Number}, // column L for runnerA, columns for runner B, the first row
                thirdSet: {type: Number}, // column L for runnerA, columns for runner B, the second row
            }
            avg: {
                back: {
                    odds: {type: Number}, // the Weighted arithmetic mean for each bets B "back" (column AF), its like: odds = (summation of odds (column AG) * stake (columns AH) ) / (sum of the stake)
                    stake: {type: Number}, // the sum of stake bets B "back" (column AF) over the runner (colum AE to select which ones)
                    toWin: {type: Number}, // toWin = stake (odds-1)
                },
                lay: {
                    odds: {type: Number}, // the Weighted arithmetic mean for each bets B "back" (column AF), its like: odds = (summation of odds (column AG) * stake (columns AH) ) / (sum of the stake)
                    bank: {type: Number}, // the sum of the stake bets L "lay" (column AF) over the runner (colum AE to select which ones)
                    liability: {type: Number}, // liability = stake * (odds - 1)
                }
            }
        }],
        trades: [ // for that part take attention of columns from N to AK, now we merge matched bets and point to have single trade for each row
            {
                id: {type: Number}, // the seq id, column AB
                selectionN: {type: Number}, // sequential number of runner (0 for runnerA, 1 for runnerB)
                type: {type: String} // columns AF ->if B "back" , if L "lay"
                odds: {type: Number}, // columns AG
                stake: {type: Number}, // colum AK
                liability: {type: Number}, // if type=="B" so liability = stake (column AK), if "L" : liability = stake*(odds-1)
                ifWin: {type: Number}, // if type=="B" ifWin = stake*(odds-1), if "L" : ifWin = stake (columns AK)
                options: {type: String} // columns AD
                condition: {
                    tennis: {
                        isTennis: {type: Boolean}, // true always
                        point: { // 0 if the cell are empty
                            set1: {
                                runnerA: {type: Number}, // column O
                                runnerB: {type: Number}, // column P
                            },
                            set2: {
                                runnerA: {type: Number}, // column Q
                                runnerB: {type: Number}, // column R
                            },
                            set3: {
                                runnerA: {type: Number}, // column S
                                runnerB: {type: Number}, // column T
                            },
                            set4: {
                                runnerA: {type: Number}, // column U
                                runnerB: {type: Number}, // column V
                            },
                            set5: {
                                runnerA: {type: Number}, // column W
                                runnerB: {type: Number}, // column X
                            },
                            currentGame: {
                                runnerA: { type: String}, // column Y
                                runnerB: { type: String}, // column Z
                                server: { type: String} // column AA
                            }
                        }
                    },
                    football: { 
                        isFootball: {type: Boolean}, // false
                        point: {
                            home: {type: Number}, // 0 
                            away: {type: Number}, // 0 
                        }
                    },
                    horse: { 
                        isHorse: {type: Boolean}, // false
                    },
                    note: {type: String}, // column N
                    time: {type: Number}, // UTC millisecond timestamp of the bets, column AC, (first date is the same of market, if have bets in different day, such as 23:34:46 and after 00:12:46 so the second have day = firstdate +1)
                }
            }
        ],
        // for that part take attention of columns from O to K
        result: {
            grossProfit: {type: Number}, // column AJ + column AK
            netProfit: {type: Number}, // column AK
            rr: {type: Number}, // column AK/column AI
            commissionPaid: {type: Number}, // column AJ
            maxRisk: {type: Number}, // -column AI
            correctionPl: {type: Number}, // 0
            finalScore:{ // from the row where "FINAL" are in column AD, get the point at here left, column 0
                tennis: { // 0 if the cell are empty
                     set1: {
                        runnerA: {type: Number}, // column O
                        runnerB: {type: Number}, // column P
                    },
                    set2: {
                        runnerA: {type: Number}, // column Q
                        runnerB: {type: Number}, // column R
                    },
                    set3: {
                        runnerA: {type: Number}, // column S
                        runnerB: {type: Number}, // column T
                    },
                    set4: {
                        runnerA: {type: Number}, // column U
                        runnerB: {type: Number}, // column V
                    },
                    set5: {
                        runnerA: {type: Number}, // column W
                        runnerB: {type: Number}, // column X
                    },
                    currentGame: {
                        runnerA: { type: String}, // 0
                        runnerB: { type: String}, // 0
                        server: { type: String} // 0
                    }
                },
                football: {
                    home: {type: Number}, // 0
                    away: {type: Number}, // 0
                }
            }
        },
        // for that part take attention of columns from AS to BL
        stats: { // an array with a length of 2, contains id for runnerA and runnerB and their stats, IF TH STATS ARE ("#N/A" OR EMPTY OR 0) PUT 0"
            [
                runnerId: {type: Number},  // the runnerId, taken form column I or J third row if present, via API if not present
                stats1: {type: Number}, // runnerA column AS, runnerB column BC
                stats2: {type: Number}, // runnerA column AT, runnerB column BD
                stats3: {type: Number}, // runnerA column AU, runnerB column BE
                stats4: {type: Number}, // runnerA column AV, runnerB column BF
                stats5: {type: Number}, // runnerA column AW, runnerB column BG
                stats6: {type: Number}, // runnerA column AX, runnerB column BH
                stats7: {type: Number}, // runnerA column AY, runnerB column BI
                stats8: {type: Number}, // runnerA column AZ, runnerB column BJ
                stats9: {type: Number}, // runnerA column BA, runnerB column BK
                stats10: {type: Number}, // runnerA column BB, runnerB column BL
            ]
        }
    }
});
```
### API RUNNER 

If the runner column (I or J) have only name, below a float point like "1.10" and no other number below we missed the runner ID

you need to make an HTTP POST call @ http://217.61.104.122/api/runners/infoByName
with body like that

```json
{
    "name": "Elias Ymer" // take from the first row column I or J
}
```

and the response should be: 

```json
[
    {
        "id": 7414305,
        "name": "Elias Ymer"
    }
]
```

the ID propriety are that you need, if return empty array [] so leave the props in the JSON null, if it returns 2 value in the array take always the first one


### API STRATEGY

For the strategyId props we need to lookup at columns G

- If the columns are empty put that value: "6220e21a9344202f70a26818"
- it the cells have some text, as example  "KI - LOW LAY" you nee to make an API call

HTTP POST call @ http://217.61.104.122/api/strategy/infoByName

with that body

```json
{
    "name": "KI - LOW LAY" // take from the first row column G
}

and the response should be: 

```json
[
    {
        "name": "KI - LOW LAY",
        "id": "6220f6459344202f70a268d2"
    }
]
```
the ID propriety are that you need, if return empty array [] so leave the props in the JSON null, if it returns 2 value in the array take always the first one



## EXAMPLE 1

![EXAMPLE](./documentation/images/2.png?raw=true "example")

for that market "Ostapenko v Sasnovich" 11-Feb 16:44:51

in that example i made 2 API call cause no Ostapenko neither Sasnovich have the runner ID, 

that's the request
```json
{
    "name": "Jelena Ostapenko"
}
```
```json
{
    "name": "Aliaksandra Sasnovich"
}
```

and that's the response

for that one i take the first object
```json
[
    {
        "id": 8827537,
        "name": "Jelena Ostapenko",
        "sport": "TENNIS",
        "_id": "61bfbb46cb8f47cf0614ab45"
    },
    {
        "id": 19795365,
        "name": "Jelena Ostapenko",
        "sport": "TENNIS",
        "_id": "61bfbc07cb8f47cf0614bd97"
    }
]
```

"Jelena Ostapenko" ID --> 8827537


```json
[
    {
        "id": 7283310,
        "name": "Aliaksandra Sasnovich",
        "sport": "TENNIS",
        "_id": "61bfbb45cb8f47cf0614ab25"
    }
]
```

"Aliaksandra Sasnovich" ID --> 7283310

the Strategy column G are empty so i use "6220e21a9344202f70a26818" for strategyId


You can find that example in the folder "./OutputFiles/03_03_2022_18_16_22" wth the name "02_11_2022_Ostapenko v Sasnovich.json"


