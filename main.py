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
    table.field_names = ["P", "Commands", "Games", "Wins", "Drawn", "Loss", "Points"]
    table.align = "l"
    table.set_style(DOUBLE_BORDER)
    r = requests.get("https://m.sports.ru/rfpl/table/", headers=headers)
    soup = BeautifulSoup(r.text, "lxml")
    commands = soup.findAll("tr", class_="b-tag-table__content-team")
    for command in commands:
        item = command.findAll("td")
        position = item[1].text
        name = item[2].text
        games = item[3].text
        wins = item[4].text
        drawn = item[5].text
        loss = item[6].text
        point = item[7].text
        table.add_row([position, name, games, wins, drawn, loss, point])
    print(table)


def get_calendar():
    r = requests.get("https://m.sports.ru/rfpl/calendar/", headers=headers)
    soup = BeautifulSoup(r.text, "lxml")
    one_tur = soup.findAll("section", class_="b-tag-tournament-calendar__stage")
    del one_tur[0:2]
    del one_tur[1:]
    table = PrettyTable()
    table.field_names = ["Дом", "Счет", "Гости", "Дата", "Статус"]
    table.align = "l"
    table.set_style(DOUBLE_BORDER)
    for tur in one_tur:
        head = tur.find("h5", class_="g-section-header").text
        matches = tur.findAll("article", class_="b-tag-tournament-calendar__stage-match")
        table.title = head
        for match in matches:
            team1 = match.findAll("div", class_="g-match-block-a__team-name")[0].text
            team2 = match.findAll("div", class_="g-match-block-a__team-name")[1].text
            gamescore = match.find("div", class_="g-score-a").text
            link_match = match.find("a").get("href")
            match_status = status_match(link_match).strip()
            matchday = match.find("div", class_="g-match-block-a__info").text[:-6]
            matchtime = match.find("div", class_="g-match-block-a__info").text[-6:]
            table.add_row([team1, gamescore, team2, matchday + " " + matchtime, match_status])

        print(table)


def status_match(url):
    """
    the function takes a link to the match and returns whether the match is completed or not
    """
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, "lxml")
    status = soup.find("div", class_="match-summary__state-info").find("span",
                                                                       class_="match-summary__state-status").text
    return status


def main():
    questions = [
        {
            'type': 'list',
            'name': 'user_option',
            'message': 'Welcome to RFPL',
            'choices': ["Таблица", "Расписание"]
        }
    ]

    answers = prompt(questions, style=custom_style_2)
    if answers.get("user_option") == "Таблица":
        get_table()
    elif answers.get("user_option") == "Расписание":
        get_calendar()


if __name__ == "__main__":
    main()
