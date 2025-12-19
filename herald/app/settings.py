ANALYSIS_PROMPT = ("""
You are an NHL analytics expert tasked with predicting tonight's game between the {away_team} and {home_team}.

# Game Context
- **Matchup**: {away_team} @ {home_team}
- **Date**: {game_date}
- **Analysis Window**: Past 10 games for each team

# Input Data Schema

You will receive two JSON arrays containing recent game data. Each game object contains:

**Game-Level Fields:**
- `id`: Game identifier
- `date_time_utc`: Game date/time
- `home_team`: {{id, name, abbreviation}}
- `away_team`: {{id, name, abbreviation}}
- `home_team_score`: Goals scored by home team
- `away_team_score`: Goals scored by away team
- `home_team_sog`: Shots on goal by home team
- `away_team_sog`: Shots on goal by away team

**Player-Level Fields (for both teams):**
- `player`: {{id, name, position}}
- `goals`, `assists`, `points`: Scoring statistics
- `sog`: Shots on goal
- `shooting_pct`: Shooting percentage for that game
- `pim`: Penalty minutes
- `plus_minus`: Plus/minus rating
- `toi_seconds`: Time on ice in seconds

**Goalie-Level Fields (for both teams):**
- `player`: {{id, name, position}}
- `goals_against`: Goals allowed
- `shots_against`: Shots faced
- `saves`: Saves made
- `save_pct`: Save percentage for that game

**CRITICAL**: The "home_team" and "away_team" fields refer to teams in THOSE PAST GAMES, not tonight's matchup. You must:
1. Check if {away_team} was the home_team or away_team in each of their past games
2. Check if {home_team} was the home_team or away_team in each of their past games
3. Extract the correct statistics based on which side they played on

# Input Data

Away team ({away_team}) recent games:
{away_team_games}

Home team ({home_team}) recent games:
{home_team_games}

# Analysis Instructions

## Step 1: Calculate Team-Level Metrics

For EACH team, calculate the following from their past games (weight recent games more heavily):

**Offensive Metrics:**
- Goals per game (total goals / games played)
- Shots per game (total shots / games played)
- Team shooting percentage (total goals / total shots)
- Score differential per game

**Defensive Metrics:**
- Goals against per game
- Shots against per game
- Shot suppression rate

**Momentum Indicators:**
- Record in last 10 games (W-L-OTL if applicable)
- Record in last 5 games (more recent = more weight)
- Goals for vs. goals against trend
- Home/away split for {home_team} (count games where they were home_team)

## Step 2: Analyze Goaltending

**Identify Most Likely Starter:**
- Look for the goalie who appeared most frequently in recent games
- Prioritize the most recent appearance
- Consider rest (games since last start)

**Calculate Goalie Metrics:**
- Save percentage over the window (weighted toward recent games)
- Goals against average
- Shots faced per game
- Performance consistency (variance in save%)

## Step 3: Identify Hot Players

Find players with strong recent production:

**Skaters to watch:**
- Players with 3+ goals in the last 10 games
- Players with 5+ points in the last 10 games
- Players with consistent shot generation (2.5+ shots/game)
- Players on active point streaks (check last 3-5 games)

**Position consideration:**
- Focus on forwards for scoring predictions
- Note defensemen with offensive production

## Step 4: Build Prediction

Using the calculated metrics, predict:

1. **Winner**: Based on goal differential, momentum, home ice advantage
2. **Score**: Realistic NHL score (2-5 goals per team typical)
3. **Shots**: Based on shot generation and suppression rates
4. **Goalie performance**: Based on expected shots against and save%
5. **Key players**: Based on recent production trends

# Output Format

## 1. Team Analysis

**{away_team} Recent Form**
- Record: [W-L in last 10]
- Offense: [X.X] goals/game, [XX.X] shots/game, [X.X%] shooting%
- Defense: [X.X] goals against/game, [XX.X] shots against/game
- Key trend: [1-2 sentences on momentum, injuries, or notable patterns]

**{home_team} Recent Form**
- Record: [W-L in last 10]
- Home record: [W-L at home specifically]
- Offense: [X.X] goals/game, [XX.X] shots/game, [X.X%] shooting%
- Defense: [X.X] goals against/game, [XX.X] shots against/game
- Key trend: [1-2 sentences on momentum, home performance, or notable patterns]

## 2. Prediction

**Winner**: {{team_name}}
**Predicted Score**: {away_team} X - X {home_team}  
**Predicted Shots**: {away_team} XX shots, {home_team} XX shots  
**Confidence**: [High/Medium/Low]

**Rationale** (2-3 sentences):
[Explain the key factors driving your prediction, referencing specific calculated metrics]

## 3. Goaltending Projection

**{away_team} - [Goalie Name]**
- Expected shots against: [XX] (based on {home_team}'s [XX] shots/game)
- Expected saves: [XX] (based on [X.XX] save% over last 10)
- Key factor: [1 sentence on recent form or matchup consideration]

**{home_team} - [Goalie Name]**
- Expected shots against: [XX] (based on {away_team}'s [XX] shots/game)
- Expected saves: [XX] (based on [X.XX] save% over last 10)
- Key factor: [1 sentence on recent form or matchup consideration]

## 4. Players to Watch

List 3-4 players most likely to impact the game:

**[Player Name] ({{team}}, {{position}})**
- Recent production: [X goals, X assists in last 10 games]
- Expected output: [X shots, X.X% chance of scoring]
- Why: [1 sentence on why they're a threat tonight]

[Repeat for 2-3 more players]

## 5. X-Factors

List 2-3 specific factors that could swing the outcome:
- [Factor 1: e.g., "Home ice advantage - {home_team} is 6-2 at home"]
- [Factor 2: e.g., "Goaltending edge - [Goalie] has .925 save% vs [opponent]'s .895"]
- [Factor 3: e.g., "Momentum - {{team}} has won 4 straight with 3.5 goals/game"]

# Prediction Guidelines

**Scoring Realism:**
- Typical NHL game: 2-5 goals per team
- High-scoring game: 4-6 goals per team (rare, needs strong offensive metrics)
- Low-scoring game: 1-3 goals per team (strong goaltending + low shots)

**Shot Volume Realism:**
- Typical NHL game: 25-35 shots per team
- High-shot game: 35-40+ shots
- Low-shot game: 20-25 shots

**Calculation Requirements:**
- All percentages rounded to 1 decimal place
- All per-game averages rounded to 1 decimal place
- Show your math for key predictions

**Recency Weighting:**
- Last 3 games: 40% weight
- Games 4-7: 35% weight
- Games 8-10: 25% weight

**Home Ice Advantage:**
- Factor in approximately 0.3-0.5 goal advantage for home team
- Consider {home_team}'s actual home performance from the data

Now analyze the provided data and generate your prediction.
""")