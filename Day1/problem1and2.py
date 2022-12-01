
# Compute the total calories brought by each elf
elfs_total_calories = []

with open('Day1/input.txt') as f:
    elf_total_calories = 0

    for line in f:
        # A blank line indicates that the inventory for the current elf has finished. The sum of the calories is 
        # appended as that elf's total calories and the summatory is re-initialised
        if line == '\n':
            elfs_total_calories.append(elf_total_calories)
            elf_total_calories = 0
        else:
            elf_total_calories += int(line)
    
    # The file does not necesarily end with a blank line, hence when we arrive at the end of the file
    # the current elf_total_calories must also be appended
    elfs_total_calories.append(elf_total_calories)

# Find the calories of the elf with the most calories
print(f'The elf with the most calories brings {max(elfs_total_calories)} calories')

# Find the sum of the top three elfs with the most calories
elfs_total_calories_cpy = elfs_total_calories.copy()
total_calories = 0
for _ in range(3):
    current_max_calories = max(elfs_total_calories_cpy)
    current_max_calories_index = elfs_total_calories_cpy.index(current_max_calories)
    total_calories += elfs_total_calories_cpy.pop(current_max_calories_index) 

print(f'The top three elfs bring {total_calories} in total')