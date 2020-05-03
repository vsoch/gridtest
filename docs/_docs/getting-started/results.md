---
title: Results
category: Getting Started
permalink: /getting-started/results/index.html
order: 7
---

### Results

GridTest currently provide a simple way to export a json file of results. As an
example, for the [custom-decorator](https://github.com/vsoch/gridtest/tree/master/examples/custom-decorator) example, we can run tests and generate a results.json
file as follows:

```bash
$ gridtest test --save results.json
[9/9] |===================================| 100.0% 
Name                           Status                         Summary                       
________________________________________________________________________________________________________________________
script.multiply_sentence.0     success                                                      
script.multiply_sentence.1     success                                                      
script.multiply_sentence.2     success                                                      
script.multiply_sentence.3     success                                                      
script.multiply_sentence.4     success                                                      
script.multiply_sentence.5     success                                                      
script.multiply_sentence.6     success                                                      
script.multiply_sentence.7     success                                                      
script.multiply_sentence.8     success                                                      

________________________________________________________________________________________________________________________
script.multiply_sentence.0     @script.countwords             5 words                       
script.multiply_sentence.1     @script.countwords             7 words                       
script.multiply_sentence.2     @script.countwords             7 words                       
script.multiply_sentence.3     @script.countwords             21 words                      
script.multiply_sentence.4     @script.countwords             31 words                      
script.multiply_sentence.5     @script.countwords             31 words                      
script.multiply_sentence.6     @script.countwords             41 words                      
script.multiply_sentence.7     @script.countwords             61 words                      
script.multiply_sentence.8     @script.countwords             61 words                      

9/9 tests passed
```

The results file is a list of results, each a dictionary of attributes for one of
the tests (meaning that the tests above would produce a list of nine entities). Here
is an example of one:

```json
[
    {
        "name": "script.multiply_sentence.8",
        "function": "script.multiply_sentence",
        "filename": "/home/vanessa/Desktop/Code/gridtest/examples/custom-decorator/script.py",
        "out": [],
        "err": [],
        "result": "You are my sunshine, my only sunshine.You are my sunshine, my only sunshine.You are my sunshine, my only sunshine.You are my sunshine, my only sunshine.You are my sunshine, my only sunshine.You are my sunshine, my only sunshine.You are my sunshine, my only sunshine.You are my sunshine, my only sunshine.You are my sunshine, my only sunshine.You are my sunshine, my only sunshine.",
        "params": {
            "metrics": [
                "@script.countwords"
            ],
            "grid": {
                "count": {
                    "list": [
                        1,
                        5,
                        10
                    ]
                },
                "sentence": {
                    "list": [
                        "He ran for the hills.",
                        "Skiddery-a rinky dinky dinky, skittery rinky doo.",
                        "You are my sunshine, my only sunshine."
                    ]
                }
            },
            "args": {
                "count": 10,
                "sentence": "You are my sunshine, my only sunshine."
            }
        },
        "raises": null,
        "success": true,
        "metrics": {
            "@script.countwords": [
                "61 words"
            ]
        },
        "module": "script"
    }
]
```

This might be useful, for example, to see that our function isn't putting a space between
string combinations, so we might be counting words incorrectly. Oh no! Thank goodness it's just a
dummy example.

### Interaface

Under development is a more interactive interface for exploring (and sharing)
the same information. We will provide CI templates that can generate these files
to render to some web interface.
