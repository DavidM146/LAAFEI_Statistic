import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image
import requests
from io import BytesIO

# Sample pitcher IDs, ranks, and team abbreviations (adjust with actual data)
pitcher_ids = [681911, 669093, 656629, 683004, 596133, 656641, 670280, 689017, 686752, 682243]
ranks = range(1, 11)
pitcher_name = ['Vesia, Alex', 'Estrada, Jeremiah', 'Kopech, Michael', 'Leiter, Jack', 'Weaver, Luke', 'Latz, Jacob', 'Bednar, David', 'Knack, Landon', 'Pepiot, Ryan', 'Miller, Bryce']
team_abbreviations = ['LAD', 'SD', 'LAD', 'TEX', 'NYY', 'TEX', 'PIT', 'LAD', 'TB', 'SEA']
LAAFEI = [114.02, 113.09, 113.07, 110.16, 109.67, 109.47, 109.43, 109.42, 109.34, 109.25]

# List of MLB teams and their corresponding ESPN logo URLs
mlb_teams = [
    {"team": "AZ", "logo_url": "https://a.espncdn.com/combiner/i?img=/i/teamlogos/mlb/500/scoreboard/ari.png&h=500&w=500"},
    {"team": "ATL", "logo_url": "https://a.espncdn.com/combiner/i?img=/i/teamlogos/mlb/500/scoreboard/atl.png&h=500&w=500"},
    {"team": "BAL", "logo_url": "https://a.espncdn.com/combiner/i?img=/i/teamlogos/mlb/500/scoreboard/bal.png&h=500&w=500"},
    {"team": "BOS", "logo_url": "https://a.espncdn.com/combiner/i?img=/i/teamlogos/mlb/500/scoreboard/bos.png&h=500&w=500"},
    {"team": "CHC", "logo_url": "https://a.espncdn.com/combiner/i?img=/i/teamlogos/mlb/500/scoreboard/chc.png&h=500&w=500"},
    {"team": "CWS", "logo_url": "https://a.espncdn.com/combiner/i?img=/i/teamlogos/mlb/500/scoreboard/chw.png&h=500&w=500"},
    {"team": "CIN", "logo_url": "https://a.espncdn.com/combiner/i?img=/i/teamlogos/mlb/500/scoreboard/cin.png&h=500&w=500"},
    {"team": "CLE", "logo_url": "https://a.espncdn.com/combiner/i?img=/i/teamlogos/mlb/500/scoreboard/cle.png&h=500&w=500"},
    {"team": "COL", "logo_url": "https://a.espncdn.com/combiner/i?img=/i/teamlogos/mlb/500/scoreboard/col.png&h=500&w=500"},
    {"team": "DET", "logo_url": "https://a.espncdn.com/combiner/i?img=/i/teamlogos/mlb/500/scoreboard/det.png&h=500&w=500"},
    {"team": "HOU", "logo_url": "https://a.espncdn.com/combiner/i?img=/i/teamlogos/mlb/500/scoreboard/hou.png&h=500&w=500"},
    {"team": "KC", "logo_url": "https://a.espncdn.com/combiner/i?img=/i/teamlogos/mlb/500/scoreboard/kc.png&h=500&w=500"},
    {"team": "LAA", "logo_url": "https://a.espncdn.com/combiner/i?img=/i/teamlogos/mlb/500/scoreboard/laa.png&h=500&w=500"},
    {"team": "LAD", "logo_url": "https://a.espncdn.com/combiner/i?img=/i/teamlogos/mlb/500/scoreboard/lad.png&h=500&w=500"},
    {"team": "MIA", "logo_url": "https://a.espncdn.com/combiner/i?img=/i/teamlogos/mlb/500/scoreboard/mia.png&h=500&w=500"},
    {"team": "MIL", "logo_url": "https://a.espncdn.com/combiner/i?img=/i/teamlogos/mlb/500/scoreboard/mil.png&h=500&w=500"},
    {"team": "MIN", "logo_url": "https://a.espncdn.com/combiner/i?img=/i/teamlogos/mlb/500/scoreboard/min.png&h=500&w=500"},
    {"team": "NYM", "logo_url": "https://a.espncdn.com/combiner/i?img=/i/teamlogos/mlb/500/scoreboard/nym.png&h=500&w=500"},
    {"team": "NYY", "logo_url": "https://a.espncdn.com/combiner/i?img=/i/teamlogos/mlb/500/scoreboard/nyy.png&h=500&w=500"},
    {"team": "OAK", "logo_url": "https://a.espncdn.com/combiner/i?img=/i/teamlogos/mlb/500/scoreboard/oak.png&h=500&w=500"},
    {"team": "PHI", "logo_url": "https://a.espncdn.com/combiner/i?img=/i/teamlogos/mlb/500/scoreboard/phi.png&h=500&w=500"},
    {"team": "PIT", "logo_url": "https://a.espncdn.com/combiner/i?img=/i/teamlogos/mlb/500/scoreboard/pit.png&h=500&w=500"},
    {"team": "SD", "logo_url": "https://a.espncdn.com/combiner/i?img=/i/teamlogos/mlb/500/scoreboard/sd.png&h=500&w=500"},
    {"team": "SF", "logo_url": "https://a.espncdn.com/combiner/i?img=/i/teamlogos/mlb/500/scoreboard/sf.png&h=500&w=500"},
    {"team": "SEA", "logo_url": "https://a.espncdn.com/combiner/i?img=/i/teamlogos/mlb/500/scoreboard/sea.png&h=500&w=500"},
    {"team": "STL", "logo_url": "https://a.espncdn.com/combiner/i?img=/i/teamlogos/mlb/500/scoreboard/stl.png&h=500&w=500"},
    {"team": "TB", "logo_url": "https://a.espncdn.com/combiner/i?img=/i/teamlogos/mlb/500/scoreboard/tb.png&h=500&w=500"},
    {"team": "TEX", "logo_url": "https://a.espncdn.com/combiner/i?img=/i/teamlogos/mlb/500/scoreboard/tex.png&h=500&w=500"},
    {"team": "TOR", "logo_url": "https://a.espncdn.com/combiner/i?img=/i/teamlogos/mlb/500/scoreboard/tor.png&h=500&w=500"},
    {"team": "WSH", "logo_url": "https://a.espncdn.com/combiner/i?img=/i/teamlogos/mlb/500/scoreboard/wsh.png&h=500&w=500"}
]

# Create a dictionary mapping team abbreviations to logo URLs
df_image = pd.DataFrame(mlb_teams)
image_dict = df_image.set_index('team')['logo_url'].to_dict()

# Function to plot player headshot
def player_headshot(pitcher_id: int, ax: plt.Axes):
    url = f'https://img.mlbstatic.com/mlb-photos/image/upload/d_people:generic:headshot:67:current.png/w_640,q_auto:best/v1/people/{pitcher_id}/headshot/silo/current.png'
    response = requests.get(url)
    img = Image.open(BytesIO(response.content))
    ax.imshow(img)
    ax.axis('off')

# Function to plot team logo
def team_logo(team_abbreviation: str, ax: plt.Axes):
    url = image_dict.get(team_abbreviation)
    if url:
        response = requests.get(url)
        img = Image.open(BytesIO(response.content))
        ax.imshow(img)
    ax.axis('off')

# Create figure with 10 rows and 5 columns
fig, axes = plt.subplots(10, 5, figsize=(10, 12))

# Add main title and subtitle
fig.suptitle('LAAFEI 2024 Leaderboard (Pitchers with at least 250 FF thrown)', fontsize=18, fontweight='bold', y=1)

# Add column titles
fig.text(0.1, 0.97, 'Rank', ha='center', va='center', fontsize=14, fontweight='bold')
fig.text(0.3, 0.97, 'Pitcher', ha='center', va='center', fontsize=14, fontweight='bold')
fig.text(0.5, 0.97, ' ', ha='center', va='center', fontsize=14, fontweight='bold')
fig.text(0.7, 0.97, ' ', ha='center', va='center', fontsize=14, fontweight='bold')
fig.text(0.9, 0.97, 'LAAFEI', ha='center', va='center', fontsize=14, fontweight='bold')

# Loop over each pitcher to display rank, name, headshot, logo, and LAAFEI
for idx, pitcher_id in enumerate(pitcher_ids):
    # Rank
    axes[idx, 0].text(0.5, 0.5, f'#{ranks[idx]}', fontsize=16, ha='center', va='center')
    axes[idx, 0].axis('off')
    
    # Pitcher name
    axes[idx, 1].text(0.5, 0.5, pitcher_name[idx], fontsize=12, ha='center', va='center')
    axes[idx, 1].axis('off')
    
    # Player headshot
    player_headshot(pitcher_id, axes[idx, 2])

    # Team logo
    team_logo(team_abbreviations[idx], axes[idx, 3])

    # LAAFEI
    axes[idx, 4].text(0.5, 0.5, f'{LAAFEI[idx]}', fontsize=16, ha='center', va='center')
    axes[idx, 4].axis('off')

# Adjust layout
plt.tight_layout()

# Save the plot as PDF and PNG
# plt.savefig("laafei_rankings.pdf", format="pdf")
plt.savefig("laafei_rankings3.png", format="png", dpi=300)

# Display plot
plt.show()