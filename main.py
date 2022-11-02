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

def get_commands(url):
    club_list = []
    club_dict = {}
    r = requests.get(url + 'teams/', headers=headers)
    soup = BeautifulSoup(r.text, 'lxml')
    commands = soup.find("table", class_="teams").find("tbody").findAll("tr")
    for command in commands:
        item = command.findAll("td")
        club_name = item[0].find("a").text
        club_url = "https://soccer365.ru" + item[0].find("a", href=True)['href']
        club_list.append(club_name)
        club_dict.update({club_name: club_url})
    questions = [{
        'type': 'list',
        'name': 'Выберите команду',
        'message': 'Выберите команду',
        'choices': club_list
    }]
    answers = prompt(questions, style=custom_style_2)
    club = answers.get('Выберите команду')
    club_link = club_dict[club]
    print(club, club_link)
    get_club_info(club,club_link)
    
    
def get_table(url):
    table = PrettyTable()
    table.field_names = ["Поз", "Команда", "И",
                         "В", "Н", "П", "З", "Пр", "+/-", "O"]
    table.align = "l"
    table.set_style(DOUBLE_BORDER)
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, "lxml")
    # commands = soup.find("div", id="competition_table").find("tbody").findAll("tr")
    try:
        commands = soup.find("div", id="competition_table").find("tbody").findAll("tr")
    except AttributeError:
        commands = soup.find("table", class_="stngs").find("tbody").findAll("tr")
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


def get_current_tur(url):
    table = PrettyTable()
    table.field_names = ["Время", "Дом", "Счет", "Гости"]
    table.align = "l"
    table.set_style(DOUBLE_BORDER)
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, "lxml")
    if soup.find("div", id="next_tur"):
        calendar_tour = soup.find("div", id="next_tur")
    else:
        calendar_tour =  soup.find("div", class_="live_comptt_bd")
    try:
        tur = calendar_tour.find("div", class_="block_header").text.strip()
    except AttributeError:
        tur = ""
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


def get_next_tur(url):
    table = PrettyTable()
    table.field_names = ["Время", "Дом", "Счет", "Гости"]
    table.align = "l"
    table.set_style(DOUBLE_BORDER)
    r = requests.get(url+"shedule/", headers=headers)
    soup = BeautifulSoup(r.text, "lxml")
    calendar_tour = soup.find("div", class_="live_comptt_bd").findNext("div", class_="live_comptt_bd")
    try:
        tur = calendar_tour.find("div", class_="cmp_stg_ttl").text
    except AttributeError:
        tur = ""
    try:
        matches = calendar_tour.findAll("div", class_="game_block")
    except AttributeError:
        print("Недоступно")
        main()

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


def get_club_shedule(club_link):
    table = PrettyTable()
    table.field_names = ["Дата", "Командa 1", "Счет", "Команда 2"]
    table.align = "l"
    table.set_style(DOUBLE_BORDER)    
    r = requests.get(club_link, headers=headers)
    soup = BeautifulSoup(r.text, "lxml")
    shedule_list = soup.find("div", class_="block_body_nopadding")
    items = shedule_list.findAll("div", class_="game_block")
    for item in items[:10]:
        date = item.find("div", class_="status").get_text(strip=True)
        team1 = item.find("div", class_="result").find("div", class_="ht")
        team1name = team1.find("div", class_="name").text
        team1goals = team1.find("div", class_="gls").text
        team2 = item.find("div", class_="result").find("div", class_="at")
        team2name = team2.find("div", class_="name").text
        team2goals = team2.find("div", class_="gls").text
        table.add_row([date, team1name, team1goals + " : " + team2goals, team2name ])
    print(table)
    

def get_club_info(club, club_link):
    questions = [
        {
            'type': 'list',
            'name': 'club_option',
            'message': 'Welcome to RFPL',
            'choices': ["Расписание", "Результаты"]
        }
    ]
    
    r = requests.get(club_link, headers=headers)
    soup = BeautifulSoup(r.text, 'lxml')
    title = soup.find("div", class_="profile_info").find("h1").text
    subtitle = soup.find("div", class_="profile_info").find("div", class_="profile_en_title").text
    table_tr = soup.find("table", class_="profile_params").find("tbody").findAll("tr")
    def get_item(index: int):
        item = table_tr[index].findAll("td")[1].get_text(strip=True)
        return item
    
    
    table = PrettyTable([title, subtitle])
    table.align = "l"
    table.set_style(DOUBLE_BORDER)
    table.add_rows([   
        ["Полное название", get_item(0)],
        ["Главный тренер", get_item(1)],
        ["Стадион", get_item(2)],
        ["Год основания", get_item(3)],
        ["Рейтинг УЕФА", get_item(4)],
        ])
    print(table)
    answers = prompt(questions, style=custom_style_2)
    if answers.get("club_option") == "Расписание":
        get_club_shedule(club_link+"&tab=shedule")
    elif answers.get("club_option") == "Результаты":
        get_club_shedule(club_link+"&tab=result_last")


def championat(url):
    questions = [
        {
            'type': 'list',
            'name': 'user_option',
            'message': 'Welcome to RFPL',
            'choices': ["Таблица", "Текущий Тур", "Следующий Тур", "Команды"]
        }
    ]

    answers = prompt(questions, style=custom_style_2)
    if answers.get("user_option") == "Таблица":
        get_table(url)
    elif answers.get("user_option") == "Текущий Тур":
        get_current_tur(url)
    elif answers.get("user_option") == "Следующий Тур":
        get_next_tur(url)
    elif answers.get("user_option") == "Команды":
        get_commands(url)

def main():
    dict_competitions = {
	"Премьер-Лига Россия":"https://soccer365.ru/competitions/13/",
	"Первая Лига Россия":"https://soccer365.ru/competitions/687/",
	"Премьер-Лига Англия":"https://soccer365.ru/competitions/12/",
	"Чемпионшип Англия":"https://soccer365.ru/competitions/565/",
	"Примера Испания":"https://soccer365.ru/competitions/16/",
	"Серия А Италия":"https://soccer365.ru/competitions/15/",
	"Лига 1 Франция":"https://soccer365.ru/competitions/18/",
	"Бундеслига":"https://soccer365.ru/competitions/17/",
    }
    
    questions = [
        {
            'type': 'list',
            'name': 'user_option',
            'message': 'Welcome to Footbal Info',
            'choices': dict_competitions.keys()
        }
    ]
    answers = prompt(questions, style=custom_style_2)
    answer = answers.get("user_option")
    championat(dict_competitions[answer])


if __name__ == "__main__":
    main()
