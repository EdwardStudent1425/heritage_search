class InputQuery:
    """
    This class preprocess an input query.
    """
    @staticmethod
    def preprocess_query(raw_query: dict) -> dict:
        """
        check whether a query has appropriate keys
        """
        base_keys = [
            'archive_case_number',
            'arrest_max',
            'arrest_min',
            'birth_max',
            'birth_min',
            'birth_region',
            'birth_year',
            'birthplace',
            'body',
            'burial_city',
            'burial_place',
            'burial_region',
            'burial_village',
            'categories',
            'conviction_max',
            'conviction_min',
            'conviction_org',
            'death_max',
            'death_min',
            'death_year',
            'deathplace',
            'detentionplace',
            'execution_max',
            'execution_min',
            'indictment',
            'liveplace',
            'name',
            'nationality',
            'patronymic',
            'place_birth',
            'profession',
            'release_max',
            'release_min',
            'sentence',
            'social',
            'surname'
        ]
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
