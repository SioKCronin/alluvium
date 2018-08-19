output = open("~/Desktop/cleaned.json", "a")

with open("~/Desktop/final.json") as f:
    for line in f:
        if 'delete' in data:
            continue
        else:
            count +=1
            output.write(line)
    print(count, "records processed")
