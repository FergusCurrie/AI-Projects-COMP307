# Method to get P( Fi | Class ) = iequal given the feature f, class and what i should equal
def pIgivenClass(f,c,iequal):
    return table[c][f][iequal] / (table[c][f][0] + table[c][f][1])

# Return probability of a class, 0 for non-spam 1 for spam
def pClass(c):
    return total[c] / (total[0]+total[1])

# Init table with table[0] = non-spam and table[1] = spam
table = [[],[]]
total = [1,1]
for i in range(0,12):
    table[0].append([1,1])
    table[1].append([1,1])

# Make table
file = open("ass3DataFiles/part2/spamLabelled.dat","r")
for line in file:
    # Get clean array of line
    line_data = line.strip().split("    ")
    line_data = [int(x.strip()) for x in line_data]
    approve = line_data[len(line_data)-1]
    total[approve] += 1

    # Loop through line data all but last index
    for i in range(0,len(line_data)-1):
        table[approve][i][line_data[i]] += 1

if(1):
    # Clean Output
    print()
    print()
    print("Printing the probabilites P(Fi|C) for each feature i: ")
    # FOR SPAM
    for i in range(0,len(table[1])):
        print("P(F",i," = 0 | SPAM) = ",pIgivenClass(i,1,0))
        print("P(F",i," = 1 | SPAM) = ",pIgivenClass(i,1,1))

    # FOR NOT SPAM
    for i in range(0,len(table[0])):
        print("P(F",i," = 0 | NOT-SPAM) = ",pIgivenClass(i,0,0))
        print("P(F",i," = 1 | NOT-SPAM) = ",pIgivenClass(i,0,1))


# Compare to test
if(1):
    # Clean Output
    print()
    print()
    print("Printing P(S|D), P(S¯|D), and Predicted:")

    file = open("ass3DataFiles/part2/spamUnLabelled.dat","r")
    for line in file:

        # Get clean array of line
        line_data = line.strip().split("    ")
        line_data = [int(x.strip()) for x in line_data]

        # For SPAM as 1.
        pSpam = pClass(1)
        for i in range(0,len(line_data)):
            pSpam *= pIgivenClass(i,1,line_data[i])

        # For NOT SPAM as 0.
        pNotSpam = pClass(0)
        for i in range(0, len(line_data)):
            pNotSpam *= pIgivenClass(i, 0, line_data[i])

        fclass = ""
        if pSpam >= pNotSpam:
            fclass = "spam"
        else:
            fclass = "notspam"

        # Normalise for output
        norm_pSpam = round(pSpam / (pSpam + pNotSpam),10)
        norm_pNotSpam = round(pNotSpam / (pSpam + pNotSpam),10)

        # Output
        print("P(S|D) = ",norm_pSpam,"  ---  P(~S|D) = ",norm_pNotSpam,"  ---  Predicted = ",fclass)
    print()



