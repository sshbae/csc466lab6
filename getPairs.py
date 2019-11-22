import numpy as np 

def main():
    userIds = np.random.randint(0, 24893, 14500)
    itemIds = np.random.randint(0, 100, 14500)
    pairs = list(map(lambda x, y:(x,y), userIds, itemIds)) 
    
    with open('testPairs.csv', 'w') as f:
        for pair in pairs:
            f.write(f"{pair[0]},{pair[1]}\n")

if __name__ == '__main__':
    main()