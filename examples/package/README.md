# Package Testing

You don't necessarily need to write tests just for local files or modules!
Gridtest also works to generate tests for modules installed with your Python.
This provides a quick example for that. First, generate a testing file:

```bash
$ gridtest generate requests requests-tests.yml
```

If I wanted to include private functions:

```bash
$ gridtest generate --include-private requests requests-tests.yml
```

In the case of requests, I don't really want to test post, delete, or patch
endpoints, so I can then open the file and just delete those chunks. 
