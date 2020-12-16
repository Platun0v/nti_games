import requests
from cs_go.Error import CSGOError


class CSGOAnalysing:
    def __init__(self, api_key, steam_id):
        self.api_key = api_key
        self.steam_id = steam_id
        self.data = ""

    def start(self):
        json_data = self.get_data()
        self.parse_data(json_data)
        return self.get_score()

    def parse_data(self, json_file):
        arr = ['total_contribution_score',
               'total_matches_played',
               'total_kills',
               'total_deaths',
               'total_rounds_played',
               'total_planted_bombs',
               'total_defused_bombs',
               'total_weapons_donated',
               'total_mvps',
               'total_wins',
               'last_match_rounds',
               'last_match_wins',
               'last_match_kills',
               'last_match_deaths',
               'last_match_mvps',
               'last_match_damage',
               'last_match_contribution_score']

        self.data = {}
        for x in json_file:
            if x["name"] in arr:
                self.data[x["name"]] = x["value"]

    def get_score(self):
        dct = self.get_score_total()
        dct["score"] = round(0.70 * dct["score"] + 0.30 * self.get_score_last() \
            if self.get_score_last() != 0 else dct["score"], 2)
        return dct

    def get_score_last(self):
        if self.data['last_match_rounds'] > 1:
            win = 1 if self.data['last_match_rounds'] / 2 <= self.data['last_match_wins'] else 0.5
            kd = 1 if self.data['last_match_kills'] / self.data['last_match_deaths'] >= 2 \
                else (self.data['last_match_kills'] / self.data['last_match_deaths']) / 2
            mvp = 1 if self.data['last_match_rounds'] / self.data['last_match_mvps'] <= 3 \
                else 3 / (self.data['last_match_rounds'] / self.data['last_match_mvps'])
            avg_dmg = 1 if self.data['last_match_damage'] / self.data['last_match_rounds'] <= 150 \
                else 150 / (self.data['last_match_damage'] / self.data['last_match_rounds'])
            avg_cs = 1 if self.data['last_match_contribution_score'] >= 70 \
                else self.data['last_match_contribution_score'] / 70
            return (win + kd + mvp + avg_cs + avg_dmg) * 20
        else:
            return 0

    def get_score_total(self):
        avg_cs = 1 if (self.data['total_contribution_score'] / self.data['total_matches_played']) >= 70 \
            else ((self.data['total_contribution_score'] / self.data['total_matches_played']) / 70)
        kd = 1 if (self.data['total_kills'] / self.data['total_deaths']) >= 2 \
            else ((self.data['total_kills'] / self.data['total_deaths']) / 2)
        plant_n_defuse = 1 if (self.data['total_rounds_played'] / (
                self.data['total_planted_bombs'] + self.data['total_defused_bombs'])) <= 13 \
            else 13 / (self.data['total_rounds_played'] / (
                self.data['total_planted_bombs'] + self.data['total_defused_bombs']))
        donate = 1 if (self.data['total_rounds_played'] / self.data['total_weapons_donated']) <= 5 \
            else (5 / (self.data['total_rounds_played'] / self.data['total_weapons_donated']))
        mvp = 1 if (self.data['total_wins'] / self.data['total_mvps']) <= 3 \
            else (3 / (self.data['total_wins'] / self.data['total_mvps']))

        dct = {
            "score": (avg_cs + kd + plant_n_defuse + donate + mvp) * 20,
            "kd": round(self.data['total_kills'] / self.data['total_deaths'], 2),
            "avg_cs": round(self.data['total_contribution_score'] / self.data['total_matches_played']),
            "avg_plant_defuse": round(self.data['total_rounds_played'] /
                                (self.data['total_planted_bombs'] + self.data['total_defused_bombs'])),
            "avg_give_weapon": round(self.data['total_rounds_played'] / self.data['total_weapons_donated']),
            "avg_mvp": round(self.data['total_wins'] / self.data['total_mvps'])
        }
        return dct

    def get_data(self):
        return self.get_request()['playerstats']['stats']

    def get_request(self):
        req = requests.get(f"http://api.steampowered.com/ISteamUserStats/GetUserStatsForGame/v0002/?appid=730&"
                           f"key={self.api_key}&steamid={self.steam_id}")

        if req.status_code != 200:
            raise CSGOError("У вас закрытый аккаунт или вы не играете в CSGO")

        return req.json()
