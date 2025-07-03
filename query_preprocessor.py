class InputQuery:
    """
    This class preprocess an input query.
    """
    @staticmethod
    def preprocess_query(raw_query: dict) -> dict:
        """
        check whether a query has appropriate keys
        """
        base_keys = ['surname', 'name', 'patronymic', 'birth_year',
                     'death_year', 'country', 'region', 'birth_settlement']
        query = dict()

        # is it necessary if i have a stable gui
        # чи є сенс взагалі це обробляти, якщо я можу від початку задати необхідний
        # дікт?

        # або хай буде, щоб потім було легше вивести повідомлення із вмістом запиту.
        for key, value in raw_query.items():
            if key in base_keys:
                query[key] = value
        return query

    @staticmethod
    def preprocess_sites(filename: str) -> list:
        '''
        preprocess a file within available sites` links
        '''
        with open(filename, "r", encoding='utf-8', newline='') as f:
            lines = [line.strip() for line in f if line.strip()]
            print(lines)
            return lines
