from data import data_manager
from psycopg2 import sql


def get_shows():
    return data_manager.execute_select('SELECT id, title FROM shows;')

def get_shows_by_parm(column='rating', order='desc', limit=0, offset=0):

    return data_manager.execute_select(
        sql.SQL("""
            SELECT shows.id, shows.title, shows.year, shows.runtime, shows.homepage, shows.trailer,
            to_char(shows.rating::float, '0.9') as rating,
            string_agg(genres.name, ', ' ORDER BY genres.name) as genres
            FROM shows
            JOIN show_genres on shows.id = show_genres.show_id
            JOIN genres on show_genres.genre_id = genres.id
            GROUP BY shows.id
            ORDER BY 
                case when %(order)s = 'asc' then {column} end ASC, 
                case when %(order)s = 'desc' then {column} end DESC 
            LIMIT %(limit)s
            OFFSET %(offset)s
        """).format(column=sql.Identifier(column)),
        {'order': order, 'limit': limit, 'offset': offset}
    )


def get_show_by_id(id):

    return data_manager.execute_select(
        sql.SQL("""
            SELECT shows.id, shows.title, shows.year, shows.runtime, shows.homepage, shows.trailer,
            to_char(shows.rating::float, '0.9') as rating,
            string_agg(genres.name, ', ' ORDER BY genres.name) as genres
            FROM shows
            JOIN show_genres on shows.id = show_genres.show_id
            JOIN genres on show_genres.genre_id = genres.id
            WHERE shows.id = %(id)s
            GROUP BY shows.id 
        """),
        {'id': id}, False)


def get_show_seasons(id):

    return data_manager.execute_select(
        sql.SQL("""
            SELECT s.season_number, s.title, s.overview
            FROM shows
            JOIN seasons s on shows.id = s.show_id
            WHERE shows.id = %(id)s
        """),
        {'id': id})


def get_show_characters(id, limit = 3):

    return data_manager.execute_select(
        sql.SQL("""
            SELECT sc.id, sc.character_name, a.name, a.birthday, a.death, a.biography
            FROM actors a
            JOIN show_characters sc on a.id = sc.actor_id
            WHERE sc.show_id = %(id)s
            LIMIT %(limit)s
        """),
        {'id': id, 'limit': limit})

def get_show_count():

    return data_manager.execute_select(
        """
        SELECT COUNT(*) FROM shows
        """
    )