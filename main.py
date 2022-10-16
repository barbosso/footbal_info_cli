import requests
from bs4 import BeautifulSoup
from prettytable import PrettyTable
from prettytable import DOUBLE_BORDER
from PyInquirer import prompt
from examples import custom_style_2

headers = {
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (HTML, like Gecko) Chrome/100.0.4896.160 "
                  "YaBrowser/22.5.3.673 browser/2.5 Safari/537.36 "
}


def get_table():
    table = PrettyTable()
    table.field_names = ["Поз", "Команда", "И",
                         "В", "Н", "П", "З", "Пр", "+/-", "O"]
    table.align = "l"
    table.set_style(DOUBLE_BORDER)
    r = requests.get("https://soccer365.ru/competitions/13/", headers=headers)
    soup = BeautifulSoup(r.text, "lxml")
    commands = soup.find("div", id="competition_table").find(
        "tbody").findAll("tr")
    for command in commands:
        item = command.findAll("td")
        position = item[0].text
        club_name = item[1].find("a").text
        games = item[2].text
        wins = item[3].text
        drawn = item[4].text
        loss = item[5].text
        goals = item[6].text
        conceded_goals = item[7].text
        difference = item[8].text
        points = item[9].text.strip()
        table.add_row([position, club_name, games, wins, drawn,
                      loss, goals, conceded_goals, difference, points])
    print(table)


def get_current_tur():
    table = PrettyTable()
    table.field_names = ["Время", "Дом", "Счет", "Гости"]
    table.align = "l"
    table.set_style(DOUBLE_BORDER)
    r = requests.get("https://soccer365.ru/competitions/13/", headers=headers)
    soup = BeautifulSoup(r.text, "lxml")
    calendar_tour = soup.find("div", id="next_tur")
    tur = calendar_tour.find("div", class_="block_header").text.strip()
    matches = calendar_tour.findAll("div", class_="game_block")
    table.title = tur
    for match in matches:
        status_match = match.find("div", class_="status").text
        team1 = match.findAll("div", class_="name")[0].text
        team2 = match.findAll("div", class_="name")[1].text
        team1_goals = match.findAll("div", class_="gls")[0].text
        team2_goals = match.findAll("div", class_="gls")[1].text
        table.add_row([status_match, team1, team1_goals +
                      " : " + team2_goals, team2])
    print(table)


def get_next_tur():
    table = PrettyTable()
    table.field_names = ["Время", "Дом", "Счет", "Гости"]
    table.align = "l"
    table.set_style(DOUBLE_BORDER)
    r = requests.get(
        "https://soccer365.ru/competitions/13/shedule/", headers=headers)
    soup = BeautifulSoup(r.text, "lxml")
    calendar_tour = soup.find("div", class_="live_comptt_bd").findNext(
        "div", class_="live_comptt_bd")
    tur = calendar_tour.find("div", class_="cmp_stg_ttl").text
    matches = calendar_tour.findAll("div", class_="game_block")
    table.title = tur
    for match in matches:
        team1 = match.findAll("div", class_="name")[0].text
        team2 = match.findAll("div", class_="name")[1].text
        status_match = match.find("div", class_="status").find("span").text
        team1_goals = match.findAll("div", class_="gls")[0].text
        team2_goals = match.findAll("div", class_="gls")[1].text
        table.add_row([status_match, team1, team1_goals +
                      " : " + team2_goals, team2])
    print(table)

#
# def get_table_bombardirs():
#     r = requests.get("https://soccer365.ru/competitions/13/", headers=headers)
#     soup = BeautifulSoup(r.text, "lxml")
#     tableb = soup.find("div", class_="live_comptt_bd")


def main():
    questions = [
        {
            'type': 'list',
            'name': 'user_option',
            'message': 'Welcome to RFPL',
            'choices': ["Таблица", "Текущий Тур", "Следующий Тур"]
        }
    ]

    answers = prompt(questions, style=custom_style_2)
    if answers.get("user_option") == "Таблица":
        get_table()
    elif answers.get("user_option") == "Текущий Тур":
        get_current_tur()
    elif answers.get("user_option") == "Следующий Тур":
        get_next_tur()


if __name__ == "__main__":
    main()
