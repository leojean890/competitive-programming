W = 200#9
H = 200#9
C = 1#7
DEMI = 100

mapping = ""
for y in range(C):
    mapping += input()

input()

empty = W*["."]
image = [empty]#[list(".........")]
for y in range(49):
    image.append(empty)#list("........."))
for y in range(H-100):
    #image.append([W//2*["."]]+list(input())+[W//2*["."]])
    image.append(50*["."]+list(input())+50*["."])
for y in range(50):
    image.append(empty)#list("........."))

#mapping = "..#.#..#####.#.#.#.###.##.....###.##.#..###.####..#####..#....#..#..##..##"
mapToBit = {".": "0", "#": "1"}

def convert(image, y, x):
    s = ""
    for (a,b) in ((y - 1, x - 1), (y - 1, x), (y - 1, x + 1), (y, x - 1), (y, x), (y, x + 1), (y + 1, x - 1), (y + 1, x), (y + 1, x + 1)):
        #s += mapToBit[image[a][b]] if 0 <= a < H and 0 <= b < W else "0"
        # si c flipped à l'instant, le prochain ne le sera pas, donc on prend l'inverse (pas dans la map => 1)
        if flipped == (not 0 <= a < H or not 0 <= b < W or image[a][b] == "."):
            s += "1"
        else:
            s += "0"

    inLookup = mapping[int(s, 2)] == "#"

    return "#" if flipped == inLookup else "."
    # car si flipped, au prochain ce ne sera pas flipped, donc on prend la valeur telle quelle,
    # sinon le prochain era flipped, on prend l'inverse

for it in range(50):
    flipped = it%2
    newImage = []
    for y in range(H):
        line = []
        for x in range(W):
            #newImage[y] = mapping(convert(image,y,x))
            line.append(convert(image,y,x))
        newImage.append(line)
    image = newImage

print(sum([line.count("#") for line in newImage])) # 18131
