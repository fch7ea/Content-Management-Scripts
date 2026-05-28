# Split footnotes - 2 spaces because the footnote gets translated as a space
footnotes = input("Paste footnotes as one line: ").split("  ")

# Remove the first entry because it's blank
footnotes.pop(0)

# Iterate each footnote and format it
with open(f"Downloads/result.txt", "w", encoding="utf-8") as outputFile:
    for i in range(len(footnotes)):
        outputFile.write("{# Footnote " + str(i+1) + " #}\n{% footnote hide=\"true\" %}" + footnotes[i].strip() + "{% endfootnote %}" + "\n\n")

print("Done :)")

    