
# These are functions in my script

def multiply_sentence(sentence, count):
    return sentence * count

def countwords(func):
    """this is a simple example of a custom decorator - the idea would be that
       the function we are decorating returns some texty value, and we split
       this value by a blank space and then count the number of tokens (words).
    """
    def counter(*args, **kwargs):
        result = func(*args, **kwargs)
        words = len(result.split(' '))
        print(f"@script.countwords {words} words")
        return result

    return counter
