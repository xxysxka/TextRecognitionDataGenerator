from trdg.generators import (
    GeneratorFromDict,
    GeneratorFromRandom,
    GeneratorFromStrings,
    GeneratorFromWikipedia,
)


generator = GeneratorFromDict(
    language=,
    count=2, 
    blur=2,
    random_blur=True
)

for ret, lbl in generator:
    img = ret[0]
    box = ret[1]
    img.show()
    print(box)
