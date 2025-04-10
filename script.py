from leaguepedia_parser import get_tournaments, get_matches

def fetch_tournaments():
    from datetime import datetime

    current_year = datetime.now().year
    regions = ["Korea", "EMEA", "China"]  # LCK, LEC, LPL
    all_tournaments = []

    try:
        for region in regions:
            tournaments = get_tournaments(region=region, year=current_year)
            all_tournaments.extend([tournament.overviewPage for tournament in tournaments])

    except Exception as e:
        print(f"Error fetching tournaments: {e}")

    return all_tournaments

def fetch_match_data(tournament_name):
    try:
        matches = get_matches(tournament_overview_page=tournament_name)

        # Transform the data into a more readable format
        formatted_matches = []
        for match in matches:
            team1 = match.teams[0].name
            team2 = match.teams[1].name
            score = f"{match.teams[0].score} - {match.teams[1].score}" if match.teams[0].score and match.teams[1].score else "TBD"
            date = match.startDT.split(' ')[0]  # Extract the date from the startDT field
            formatted_matches.append({
                "region": tournament_name,  # Use the full tournament name for LCK/2025 tournaments
                "team1": team1,
                "team2": team2,
                "score": score,
                "date": date
            })

        return formatted_matches

    except Exception as e:
        print(f"Error fetching matches for tournament '{tournament_name}': {e}")
        return []

def generate_html(matches):
    html_content = """<!DOCTYPE html>
<html lang='en'>
<head>
    <meta charset='UTF-8'>
    <meta name='viewport' content='width=device-width, initial-scale=1.0'>
    <title>League of Legends Match Scores</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        table { width: 100%; border-collapse: collapse; margin-bottom: 40px; }
        th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
        th { background-color: #f4f4f4; }
        .winner { color: green; font-weight: bold; }
        .loser { color: red; }
        .tournament-link { margin-bottom: 20px; }
        .tabs { display: flex; margin-bottom: 20px; }
        .tab { margin-right: 10px; padding: 10px; background-color: #f4f4f4; border: 1px solid #ddd; cursor: pointer; }
        .tab.active { background-color: #ddd; font-weight: bold; }
        .tab-content { display: none; }
        .tab-content.active { display: block; }
    </style>
    <script>
        function showTab(region) {
            const tabs = document.querySelectorAll('.tab');
            const contents = document.querySelectorAll('.tab-content');
            tabs.forEach(tab => tab.classList.remove('active'));
            contents.forEach(content => content.classList.remove('active'));
            document.getElementById(region).classList.add('active');
            document.getElementById(`${region}-tab`).classList.add('active');
        }
    </script>
</head>
<body>
    <h1>League of Legends Match Scores</h1>
    <div class='tabs'>
        <div id='LEC-tab' class='tab' onclick="showTab('LEC')">LEC</div>
        <div id='LCK-tab' class='tab' onclick="showTab('LCK')">LCK</div>
        <div id='LPL-tab' class='tab' onclick="showTab('LPL')">LPL</div>
    </div>
"""
    regions = {"LEC": [], "LCK": [], "LPL": []}
    for match in matches:
        region = match['region'].split('/')[0]
        if region in regions:
            regions[region].append(match)

    for region, region_matches in regions.items():
        html_content += f"<div id='{region}' class='tab-content { 'active' if region == 'LEC' else '' }'>"
        tournaments = {}
        for match in region_matches:
            if match['region'] not in tournaments:
                tournaments[match['region']] = []
            tournaments[match['region']].append(match)

        for tournament, tournament_matches in tournaments.items():
            html_content += f"<h2 id='{tournament}'>{tournament}"
            if all(match['score'] != 'TBD' for match in tournament_matches):
                html_content += " (Finished)"
            html_content += "</h2>"
            html_content += f"""
            <details { 'open' if any(match['score'] == 'TBD' for match in tournament_matches) else '' }>
                <summary>Show Matches</summary>
                <table>
                    <thead>
                        <tr>
                            <th>Team 1</th>
                            <th>Team 2</th>
                            <th>Score</th>
                            <th>Date</th>
                        </tr>
                    </thead>
                    <tbody>
            """
            for match in tournament_matches:
                if match['score'] == "TBD":
                    team1_class = team2_class = ""
                else:
                    team1_score, team2_score = map(int, match['score'].split(' - '))
                    team1_class = "winner" if team1_score > team2_score else "loser"
                    team2_class = "winner" if team2_score > team1_score else "loser"
                html_content += f"""
                    <tr>
                        <td class='{team1_class}'>{match['team1']}</td>
                        <td class='{team2_class}'>{match['team2']}</td>
                        <td>{match['score']}</td>
                        <td>{match['date']}</td>
                    </tr>
                """

            html_content += """
                    </tbody>
                </table>
            </details>
            """

        html_content += "</div>"

    html_content += """
</body>
</html>
"""
    return html_content

def save_html_file(content, filename="index.html"):
    with open(filename, "w", encoding="utf-8") as file:
        file.write(content)

def main():
    print("Fetching available tournaments...")
    tournaments = fetch_tournaments()

    all_matches = []
    for tournament_name in tournaments:
        print(f"Fetching match data for tournament: {tournament_name}...")
        matches = fetch_match_data(tournament_name)
        all_matches.extend(matches)

    all_matches.sort(key=lambda match: match['date'])

    print("Generating HTML...")
    html_content = generate_html(all_matches)
    print("Saving HTML file...")
    save_html_file(html_content)
    print("Website generated successfully!")

if __name__ == "__main__":
    main()
