# excelToJson

The propose of that project is to convert t and excel file to some JSON file that i will upload in my personal DB

As alway we need to work for block in the excel, one single block are like that 

![block](./documentation/images/1.png?raw=true "1")
a block always start with a Date in colum B, "OPEN" in column AD (with upper "final if is not the first"), end ends at "FINAL" in column AD.

From each block in the excel  need to generate and save a JSON file with fileName "MM_DD_YYY_marketName.json"

### Final format

That will be the final format of the JSON
```JS
{
    created: {type: Number},        // UTC millisecond timestamp when generated the file
    lastUpdate: {type: Number},     // UTC millisecond timestamp when generated the file
    trade: {
        // for that part take attention of columns from B to N
        info: {
            strategyId: {type: String}, // the ID in second row of each columns G "strategy"
            tennisTournamentId: {type: String}, // the ID in second row of each columns H "event"
            date: {type: Number},   // UTC millisecond timestamp of the market (get date in column A and time in column C)
            marketInfo: {
                marketName: {type: String}, // market columns D
                marketId: {type: String},   // leave empty for the moment
                marketType: {type: String},   // "MATCH_ODDS" if marketName (column D not have substring " - Set * Winner"), otherwise if have substring " - Set 1 Winner" -> "SET_1_WINNER",  otherwise if have substring " - Set 2 Winner" -> "SET_2_WINNER"
                sport: {type: String},      // "TENNIS"
            },
            executor: [{type: String}],     // COLUMN F
            exchange: {
                name: {type: String},       // COLUMN E
                commission: {type: Number}, // IF contains "UK" 0.02 othrwise 0.05
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
            runnerId: {type: Number},   // the third row in columns name, if empty CALL THE API TO RETRIVE ID, i explain that in point API RUNNER
            runnerName: {type: String}, // the name of the runner, first row in column I or J
            winner: {type: Boolean}, // if the runnerName is the same name in column K true, false otherwise
            bsp: {type: Number}, // the second row of the columns of runner
            sets: {
                secondSet: {type: Number}, // column L for runnerA, columns for runner B, the first row
                thirdSet: {type: Number}, // column L for runnerA, columns for runner B, the second row
            }
            avg: {
                back: {
                    odds: {type: Number}, // the Weighted arithmetic mean for each bets B "back" (column AF), its like: odds = (summation of odds (column AG) * stake (columns AH) ) / (sum of the stake)
                    stake: {type: Number}, // the sum of stake bets B "back" (column AF) over the runner (colum AE to select which ones)
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
        // PENSARE A RIMUOVE SI VEDE GIA IN TABELLA DEI TRADE, MAGARI UTILE PER FILTRARE MA NON CREDO SERVA
        exposition: [{
            back: {type: Number},
            lay: {type: Number},
            selectionN: {type: Number},
        }],
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
    }
});
```
### API RUNNER

If the runner column (I or J) have only name, below a float point like "1.10" and no other number below we missed the runner ID

you need to make an HTTP POST call @ http://217.61.104.122/api/runners/infoByName
with body like that

```json
{
    "name": "Elias Ymer" // take from the first row column J or K
}
```

and the response should be: 

```json
[
    {
        "id": 7414305,
        "name": "Elias Ymer",
        "sport": "TENNIS",
        "_id": "61bfbb3bcb8f47cf0614aa35"
    }
]
```

the id propriety are that you need, if return empty array [] so leave the props in the JSON null


### EXAMPLE

![EXAMPLE](./documentation/images/2.png?raw=true "example")

for that market "Ostapenko v Sasnovich" 11-Feb 16:44:51

i need a JSON like that
```JS
    {
    created: 1646174829000,        // UTC millisecond timestamp when generated the file
    lastUpdate: 1646174829000,     // UTC millisecond timestamp when generated the file
    trade: {
        // for that part take attention of columns from B to N
        info: {
            strategyId: "the empty strategy ID", // the ID in second row of each columns G "strategy", if empty put that " "
            tennisTournamentId: 61fe7f84a4eaad5dc977082f, // the ID in second row of each columns H "event"
            date: 1613058291000,   // UTC millisecond timestamp of the market (get date in column A and time in column C)
            marketInfo: {
                marketName: Ostapenko v Sasnovich, // market columns D
                marketId: null,   // leave empty for the moment
                marketType: "MATCH_ODDS",   // "MATCH_ODDS" if marketName (column D not have substring " - Set * Winner"), otherwise if have substring " - Set 1 Winner" -> "SET_1_WINNER",  otherwise if have substring " - Set 2 Winner" -> "SET_2_WINNER"
                sport: "TENNIS",      // "TENNIS"
            },
            executor: ["KITO"],     // COLUMN F
            exchange: {
                name: "UK KEVIN",       // COLUMN E
                commission: 0.02, // IF contains "UK" 0.02 othrwise 0.05
            },
            note: {
                description: {type: String}, // empty
                entry: "troppo tilt, 40-0, entro su sasnovich", // merge all the comments here from column N
                exit: {type: String}, // empty
                position: {type: String}, // empty
                mm: {type: String}, // empty
                odds: {type: String}, // empty
                post: {type: String}, // empty
            }
        },
        // for that part take attention of columns from I to M
        selections: [{ // array of objet, one each for runner (runnerA in columns I and runnerB in column J)
            runnerId: 8827537,   // the third row in columns name, if empty CALL THE API TO RETRIVE ID, i explain that in point API RUNNER
            runnerName: "Jelena Ostapenko", // the name of the runner, first row in column I or J
            winner: true, // if the runnerName is the same name in column K true, false otherwise
            bsp: 1.5, // the second row of the columns of runner
            sets: {
                secondSet: null, // column L for runnerA, columns for runner B, the first row
                thirdSet: null, // column L for runnerA, columns for runner B, the second row
            }
            avg: {
                back: {
                    odds: 1.82, // the Weighted arithmetic mean for each bets B "back" (column AF), its like: odds = (summation of odds (column AG) * stake (columns AH) ) / (sum of the stake)
                    stake: 35.56, // the sum of stake bets B "back" (column AF) over the runner (colum AE to select which ones)
                },
                lay: {
                    odds: 2.18, // the Weighted arithmetic mean for each bets B "back" (column AF), its like: odds = (summation of odds (column AG) * stake (columns AH) ) / (sum of the stake)
                    bank: 41.44, // the sum of the stake bets L "lay" (column AF) over the runner (colum AE to select which ones)
                    liability: 49.01, // liability = stake * (odds - 1)
                }
            }
        }],
        trades: [ // for that part take attention of columns from N to AK, now we merge matched bets and point to have single trade for each row
            {// row 193
                id: 1, // the seq id, column AB
                selectionN: 0, // sequential number of runner (0 for runnerA, 1 for runnerB)
                type: "back" // columns AF ->if B "back" , if L "lay"
                odds: 1.96, // columns AG
                stake: 20, // colum AK
                liability: 20, // if type=="B" so liability = stake (column AK), if "L" : liability = stake*(odds-1)
                ifWin: 19.2, // if type=="B" ifWin = stake*(odds-1), if "L" : ifWin = stake (columns AK)
                options: "OPEN" // columns AD
                condition: {
                    tennis: {
                        isTennis: true, // true always
                        point: { // 0 if the cell are empty
                            set1: {
                                runnerA: 7, // column O
                                runnerB: 6, // column P
                            },
                            set2: {
                                runnerA: 4, // column Q
                                runnerB: 6, // column R
                            },
                            set3: {
                                runnerA: 1, // column S
                                runnerB: 1, // column T
                            },
                            set4: {
                                runnerA: 0, // column U
                                runnerB: 0, // column V
                            },
                            set5: {
                                runnerA: 0, // column W
                                runnerB: 0, // column X
                            },
                            currentGame: {
                                runnerA: "0", // column Y
                                runnerB: "0", // column Z
                                server: "B" // column AA
                            }
                        }
                    },
                    football: { 
                        isFootball: false, // false
                        point: {
                            home: 0, // 0 
                            away: 0, // 0 
                        }
                    },
                    horse: { 
                        isHorse: false, // false
                    },
                    note: "", // column N
                    time: 1613056309000, // UTC millisecond timestamp of the bets, column AC, (first date is the same of market, if have bets in different day, such as 23:34:46 and after 00:12:46 so the second have day = firstdate +1)
                }
            },
            {// row 194
                id: 2, // the seq id, column AB
                selectionN: 0, // sequential number of runner (0 for runnerA, 1 for runnerB)
                type: "lay" // columns AF ->if B "back" , if L "lay"
                odds: 2.52, // columns AG
                stake: 15.56, // colum AK
                liability: 23.65, // if type=="B" so liability = stake (column AK), if "L" : liability = stake*(odds-1)
                ifWin: 15.56, // if type=="B" ifWin = stake*(odds-1), if "L" : ifWin = stake (columns AK)
                options: "CLOSE" // columns AD
                condition: {
                    tennis: {
                        isTennis: true, // true always
                        point: { // 0 if the cell are empty
                            set1: {
                                runnerA: 7, // column O
                                runnerB: 6, // column P
                            },
                            set2: {
                                runnerA: 4, // column Q
                                runnerB: 6, // column R
                            },
                            set3: {
                                runnerA: 2, // column S
                                runnerB: 1, // column T
                            },
                            set4: {
                                runnerA: 0, // column U
                                runnerB: 0, // column V
                            },
                            set5: {
                                runnerA: 0, // column W
                                runnerB: 0, // column X
                            },
                            currentGame: {
                                runnerA: "0", // column Y
                                runnerB: "0", // column Z
                                server: "A" // column AA
                            }
                        }
                    },
                    football: { 
                        isFootball: false, // false
                        point: {
                            home: 0, // 0 
                            away: 0, // 0 
                        }
                    },
                    horse: { 
                        isHorse: false, // false
                    },
                    note: "", // column N
                    time: 1613056462000, // UTC millisecond timestamp of the bets, column AC, (first date is the same of market, if have bets in different day, such as 23:34:46 and after 00:12:46 so the second have day = firstdate +1)
                }
            },
            { // row 195
                id: 3, // the seq id, column AB
                selectionN: 1, // sequential number of runner (0 for runnerA, 1 for runnerB)
                type: "back" // columns AF ->if B "back" , if L "lay"
                odds: 1.64, // columns AG
                stake: 15.56, // colum AK
                liability: 15.56, // if type=="B" so liability = stake (column AK), if "L" : liability = stake*(odds-1)
                ifWin: 9.96 , // if type=="B" ifWin = stake*(odds-1), if "L" : ifWin = stake (columns AK)
                options: "OPEN" // columns AD
                condition: {
                    tennis: {
                        isTennis: true, // true always
                        point: { // 0 if the cell are empty
                            set1: {
                                runnerA: 7, // column O
                                runnerB: 6, // column P
                            },
                            set2: {
                                runnerA: 4, // column Q
                                runnerB: 6, // column R
                            },
                            set3: {
                                runnerA: 2, // column S
                                runnerB: 1, // column T
                            },
                            set4: {
                                runnerA: 0, // column U
                                runnerB: 0, // column V
                            },
                            set5: {
                                runnerA: 0, // column W
                                runnerB: 0, // column X
                            },
                            currentGame: {
                                runnerA: "0", // column Y
                                runnerB: "0", // column Z
                                server: "A" // column AA
                            }
                        }
                    },
                    football: { 
                        isFootball: false, // false
                        point: {
                            home: 0, // 0 
                            away: 0, // 0 
                        }
                    },
                    horse: { 
                        isHorse: false, // false
                    },
                    note: "", // column N
                    time: 1613056462000, // UTC millisecond timestamp of the bets, column AC, (first date is the same of market, if have bets in different day, such as 23:34:46 and after 00:12:46 so the second have day = firstdate +1)
                }
            }
            {// row 196
                id: 4, // the seq id, column AB
                selectionN: 1, // sequential number of runner (0 for runnerA, 1 for runnerB)
                type: "lay" // columns AF ->if B "back" , if L "lay"
                odds: 1.98, // columns AG
                stake: 25.88, // colum AK
                liability: 25.36, // if type=="B" so liability = stake (column AK), if "L" : liability = stake*(odds-1)
                ifWin: 25.88 , // if type=="B" ifWin = stake*(odds-1), if "L" : ifWin = stake (columns AK)
                options: "CLOSE" // columns AD
                condition: {
                    tennis: {
                        isTennis: true, // true always
                        point: { // 0 if the cell are empty
                            set1: {
                                runnerA: 7, // column O
                                runnerB: 6, // column P
                            },
                            set2: {
                                runnerA: 4, // column Q
                                runnerB: 6, // column R
                            },
                            set3: {
                                runnerA: 3, // column S
                                runnerB: 1, // column T
                            },
                            set4: {
                                runnerA: 0, // column U
                                runnerB: 0, // column V
                            },
                            set5: {
                                runnerA: 0, // column W
                                runnerB: 0, // column X
                            },
                            currentGame: {
                                runnerA: "0", // column Y
                                runnerB: "0", // column Z
                                server: "B" // column AA
                            }
                        }
                    },
                    football: { 
                        isFootball: false, // false
                        point: {
                            home: 0, // 0 
                            away: 0, // 0 
                        }
                    },
                    horse: { 
                        isHorse: false, // false
                    },
                    note: "", // column N
                    time: 1613056462000, // UTC millisecond timestamp of the bets, column AC, (first date is the same of market, if have bets in different day, such as 23:34:46 and after 00:12:46 so the second have day = firstdate +1)
                }
            }
        ],
        // PENSARE A RIMUOVE SI VEDE GIA IN TABELLA DEI TRADE, MAGARI UTILE PER FILTRARE MA NON CREDO SERVA
        exposition: [{
            back: {type: Number},
            lay: {type: Number},
            selectionN: {type: Number},
        }],
        result: {
            grossProfit: -9.82, // column AJ + column AK
            netProfit: -9.82, // column AK
            rr: -0.49, // column AK/column AI
            commissionPaid: 0, // column AJ
            maxRisk: -20, // -column AI
            correctionPl: 0, // 0
            finalScore:{ // from the row where "FINAL" are in column AD, get the point at here left, column 0
                tennis: { // 0 if the cell are empty
                     set1: {
                        runnerA: 7, // column O
                        runnerB: 6, // column P
                    },
                    set2: {
                        runnerA: 4, // column Q
                        runnerB: 6, // column R
                    },
                    set3: {
                        runnerA: 6, // column S
                        runnerB: 3, // column T
                    },
                    set4: {
                        runnerA: 0, // column U
                        runnerB: 0, // column V
                    },
                    set5: {
                        runnerA: 0, // column W
                        runnerB: 0, // column X
                    },
                    currentGame: {
                        runnerA: "0", // 0
                        runnerB: "0", // 0
                        server: "0" // 0
                    }
                },
                football: {
                    home: 0, // 0
                    away: 0, // 0
                }
            }
        },
    }
});
```



