import psycopg2
from data_files.config import config


class DBManager:
    """Класс подключение к бд заполнение ее и фильтрация"""
    def __init__(self, database_name):
        self.params = config()
        self.params.update({'dbname': database_name})
        self.conn = psycopg2.connect(**self.params)
        self.cur = self.conn.cursor()

    def get_companies_and_vacancies_count(self):
        """"Количество вакансий у компаний"""
        self.cur.execute("""SELECT employers.title, COUNT(vacancies.vacancy_id) FROM employers LEFT JOIN vacancies 
                        ON employers.employer_id = vacancies.employer_id GROUP BY employers.title""")
        result = self.cur.fetchall()
        return result

    def get_all_vacancies(self):
        """Функция вывода компании вакансий зп и ссылке"""
        self.cur.execute("""SELECT  employers.title, vacancies.title, vacancies.salary, vacancies.url 
            FROM vacancies 
            INNER JOIN employers ON vacancies.employer_id = employer_id """)
        result = self.cur.fetchall()
        vacancies = []
        for row in result:
            vacancy = {
                "employer_name": row[0],
                "vacancy_name": row[1],
                "salary": row[2],
                "url": row[3]
            }
            vacancies.append(vacancy)
        return vacancies

    def get_avg_salary(self):
        """Функция поиска средней зп"""
        self.cur.execute("""SELECT AVG(CAST(salary AS numeric)) FROM vacancies""")
        result = self.cur.fetchone()[0]
        return result

    def get_vacancies_with_higher_salary(self):
        """Поиск вакансии по средней зп и фильтрации выше нее"""
        self.cur.execute("""SELECT AVG(CAST(salary AS numeric)) FROM vacancies""")
        avg_salary = self.cur.fetchone()[0]
        self.cur.execute(f"""SELECT * FROM vacancies WHERE CAST(salary AS numeric) > {avg_salary}""")
        result = self.cur.fetchall()
        return result

    def get_vacancies_with_keyword(self, word):
        """Получает список вакансий по слову"""
        self.cur.execute(f"SELECT * FROM vacancies WHERE title LIKE '%{word}%'")
        result = self.cur.fetchall()
        return result

    def close(self):
        """ Функция закрытия соединения с бд"""
        self.cur.close()
        self.conn.close()
