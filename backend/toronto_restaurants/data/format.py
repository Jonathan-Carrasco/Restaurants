import csv

'''
Mappings from mainCategory -> general Category
'''

Multicultural = ('afghan','russian','hawaiian','australian','burmese',
                          'brazilian')
American = ('burgers','barbeque','american','hotdogs','new american',
                     'pizza','steakhouse','cheesesteak','donuts','southern')
Latin_American = ('mexican','tex-mex','colombian','cuban','venezuelan',
                           'argentine','nicaraguan','salvadoran','peruvian')
East_Asian = ('japanese','chinese','singaporean','noodles','sushi',
                       'korean','taiwanese', 'hot pot')
South_Asian = ('indian','pakistani','bangladeshi','himalayan/nepalese')
Southeast_Asian = ('thai','cambodian','malaysian','indonesian','vietnamese')
Middle_Eastern = ('lebanese','syrian','turkish','falafel','kebab','donairs',
                  'persian/iranian')
Western_European = ('belgian','french','cajun/creole','waffles')
Southern_European = ('greek','italian','spanish','portuguese','iberian',
                              'tapas','salads')
Northern_European = ('british','scandinavian','sandwiches')
Central_European = ('hungarian','polish','german','slovakian','bagels')
Canadian = ('canadian','poutine')
African = ('ethiopian','moroccan','carribean')

'''
Frozen set's are used so that keys can be arrays
'''

categoryMapping = { frozenset(Multicultural): 'Multicultural',
                    frozenset(American): 'American',
                    frozenset(Latin_American): 'Latin American',
                    frozenset(East_Asian): 'East Asian',
                    frozenset(South_Asian): 'South Asian',
                    frozenset(Southeast_Asian): 'Southeast Asian',
                    frozenset(Middle_Eastern): 'Middle Eastern',
                    frozenset(Western_European): 'Western European',
                    frozenset(Southern_European): 'Southern European',
                    frozenset(Northern_European): 'Northern European',
                    frozenset(Central_European): 'Central European',
                    frozenset(Canadian): 'Canadian',
                    frozenset(African): 'African'
}

fields = []
rows = []

# Read the original csv for restaurants
with open('restaurants.csv', 'r') as readFile:
    csvreader = csv.reader(readFile)

    # Extract the field names through first row
    fields = next(csvreader)

    # Add a new field for our new csv file
    fields.append("generalCategory")
    rows.append(fields)

    # If new fields area added, categoryIndex will be different
    categoryIndex = 7

    # Add the general Category to each row in our csv
    for row in csvreader:
        for specific, general in categoryMapping.items():
            if row[categoryIndex] in specific:
                row.append(general)
                rows.append(row)
                break

# Save the previous rows we created to our new csv file
with open('generalCategories.csv', 'w') as writeFile:
    writer = csv.writer(writeFile)
    writer.writerows(rows)

readFile.close()
writeFile.close()
