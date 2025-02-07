import leaguepedia_parser

regions = ['Korea', 'China']
year = 2025

def get_tournaments_by_region(regions: list[str], year: int):

    tdict = {}
    for r in regions:
        tournaments = leaguepedia_parser.get_tournaments(r, year)

        if tournaments:
            tmp = []
            for t in tournaments:
                tmp.append(t.__getattribute__('overviewPage'))

            tdict[r] = tmp

    return tdict

print(get_tournaments_by_region(regions, year))
