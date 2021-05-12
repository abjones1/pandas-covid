import sqlite3


def main():
    max_cases = get_max("covid.db")
    print("The maximum number of cases, {cases}, has occurred in {state}."
          .format(cases=max_cases[0], state=max_cases[1]))


def get_max(db_file):
    query = '''SELECT tot_cases, state
                FROM us_cases_deaths_by_state
                ORDER BY tot_cases DESC;'''

    connection = sqlite3.connect(db_file)
    cursor = connection.cursor()
    cursor.execute(query)
    results = cursor.fetchone()
    cursor.close()
    connection.close()
    return results


main()
