---
title: Results
category: Getting Started
permalink: /getting-started/results/index.html
order: 7
---

 - [Export](#export): as a json file for your own usage.
 - [Web Report](#report): an interactive web report to share more easily.


<a id="export">
## Export via Json

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

<a id="report">
## Web Reports

GridTest allows for generation of static html reports to go along with tests.

### Run Tests

As an example, we can start with the [interface](https://github.com/vsoch/gridtest/tree/master/examples/interface)
example, which is an extended example of the above. Running tests looks like this:

```bash
$ gridtest test
[12/12] |===================================| 100.0% 
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
script.unique_sentence.0       success                                                      
script.unique_sentence.1       success                                                      
script.unique_sentence.2       success                                                      

________________________________________________________________________________________________________________________
script.multiply_sentence.0     @script.countwords             5 words                       
script.multiply_sentence.0     @script.countletters           17 letters                    
script.multiply_sentence.1     @script.countwords             7 words                       
script.multiply_sentence.1     @script.countletters           43 letters                    
script.multiply_sentence.2     @script.countwords             7 words                       
script.multiply_sentence.2     @script.countletters           32 letters                    
script.multiply_sentence.3     @script.countwords             21 words                      
script.multiply_sentence.3     @script.countletters           85 letters                    
script.multiply_sentence.4     @script.countwords             31 words                      
script.multiply_sentence.4     @script.countletters           215 letters                   
script.multiply_sentence.5     @script.countwords             31 words                      
script.multiply_sentence.5     @script.countletters           160 letters                   
script.multiply_sentence.6     @script.countwords             41 words                      
script.multiply_sentence.6     @script.countletters           170 letters                   
script.multiply_sentence.7     @script.countwords             61 words                      
script.multiply_sentence.7     @script.countletters           430 letters                   
script.multiply_sentence.8     @script.countwords             61 words                      
script.multiply_sentence.8     @script.countletters           320 letters                   
script.unique_sentence.0       @script.countwords             5 words                       
script.unique_sentence.0       @script.countletters           17 letters                    
script.unique_sentence.1       @script.countwords             6 words                       
script.unique_sentence.1       @script.countletters           38 letters                    
script.unique_sentence.2       @script.countwords             6 words                       
script.unique_sentence.2       @script.countletters           30 letters                    

12/12 tests passed
```

As you can see, when you have multiple tests with more than one metric, the output
to the terminal can get crowded. We can help that with report generation.

### Generate Web Report

Generating the interface is simple! Remember that if we wanted to save the raw
results, we could add `--save` with a filename:

```bash
$ gridtest test --save results.json
```

You can do the same for the interface, but instead provide the --save-web
flag. If you don't provide an argument to this flag, it will generate
a folder for you in `/tmp` with files that can be added to a web server.
If you do provide a folder path, the same folder will be renamed
to be there (so make sure it doesn't exist). The following command
will save pages to a subfolder called "web" in the present working directory,
which should not exist.

```bash
$ gridtest test --save-web web/
```

You'll notice in the folder that we've generated some basic webby files (.html, .js. and .css)
and also the same results.json that will populate the interface.

```bash
$ tree web
web/
├── gridtest.css
├── gridtest.js
├── index.html
└── results.json
```

You should be able to put these static files on GitHub pages, or just cd
into the folder and run a webserver:

```bash
python -m http.server 9999
```

And see the content at `http://localhost:9999`. This
is a fairly simple results template that lets you select functions in the left
columns, and then see specific tests in the right table

![img/gridtest.png](../img/gridtest.png)

and mouse over the test name to see the output, error, and metrics recorded.

![img/detail.png](../img/detail.png)

The report generated above is available for viewing [here]({{ site.baseurl }}/pages/templates/report/)

You might next want to browse [tutorials]({{ site.baseurl }}/tutorials/) available.
