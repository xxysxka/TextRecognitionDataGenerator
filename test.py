from trdg.generators import (
    GeneratorFromDict,
    GeneratorFromRandom,
    GeneratorFromStrings,
    GeneratorFromWikipedia,
)


generator = GeneratorFromStrings(
    ['Test1', 'Test2', 'Test3'],
    count=5, 
    blur=2,
    random_blur=True
)

for ret, lbl in generator:
    img = ret[0]
    box = ret[1]
    img.show()
    print(box)
