from psycopg2 import pool

class Database:
    __connection_pool = None

    @classmethod
    def initialize(cls, minconn, maxconn, **kwargs):
        cls.__connection_pool = pool.SimpleConnectionPool(minconn, maxconn, **kwargs)

    @classmethod
    def get_connection(cls):
        return cls.__connection_pool.getconn()

    @classmethod
    def return_connection(cls, connection):
        Database.__connection_pool.putconn(connection)
    
    @classmethod
    def close_all_connections(cls):
        Database.__connection_pool.closeall()

    @classmethod
    def create_tables(cls):
        with CursorFromConnectionFromPool() as cursor:
                cursor.execute("""CREATE TABLE vote_averages(
                                id bigint primary key,
                                description text
                            );

                            CREATE TABLE IF NOT EXISTS movies(
                                id bigint primary key,
                                revenue bigint,
                                title text,
                                release_date text,
                                backdrop_path text,
                                budget bigint,
                                vote_average bigint references vote_averages(id)
                            );

                            CREATE TABLE IF NOT EXISTS directors(
                                movie_id bigint references movies(id) primary key,
                                name text,
                                image text
                            );

                            CREATE TABLE IF NOT EXISTS actors(
                                id bigint primary key,
                                name text,
                                image text
                            );

                            CREATE TABLE IF NOT EXISTS genres(
                                id bigint primary key,
                                name text
                            );

                            CREATE TABLE IF NOT EXISTS acts_in(
                                movie_id bigint references movies(id),
                                actor_id bigint references actors(id)
                            
                            );

                            CREATE TABLE IF NOT EXISTS is_about(
                                movie_id bigint references movies(id),
                                genre_id bigint references genres(id)
                            );

                            INSERT INTO vote_averages VALUES (0, 'Pesima') on conflict do nothing;
                            INSERT INTO vote_averages VALUES (1, 'Terrible') on conflict do nothing;
                            INSERT INTO vote_averages VALUES (2, 'Malisima') on conflict do nothing;
                            INSERT INTO vote_averages VALUES (3, 'Mala') on conflict do nothing;
                            INSERT INTO vote_averages VALUES (4, 'Buen intento pero le falta') on conflict do nothing;
                            INSERT INTO vote_averages VALUES (5, 'Meh') on conflict do nothing;
                            INSERT INTO vote_averages VALUES (6, 'No esta mal') on conflict do nothing;
                            INSERT INTO vote_averages VALUES (7, 'Buena') on conflict do nothing;
                            INSERT INTO vote_averages VALUES (8, 'Muy buena') on conflict do nothing;
                            INSERT INTO vote_averages VALUES (9, 'Excelente') on conflict do nothing;
                            INSERT INTO vote_averages VALUES (10, 'Perfecta') on conflict do nothing;

                            INSERT INTO genres VALUES (28, 'Acción') on conflict do nothing;
                            INSERT INTO genres VALUES (12, 'Aventura') on conflict do nothing;
                            INSERT INTO genres VALUES (16, 'Animación') on conflict do nothing;
                            INSERT INTO genres VALUES (35, 'Comedia') on conflict do nothing;
                            INSERT INTO genres VALUES (80, 'Crimen') on conflict do nothing;
                            INSERT INTO genres VALUES (99, 'Documental') on conflict do nothing;
                            INSERT INTO genres VALUES (18, 'Drama') on conflict do nothing;
                            INSERT INTO genres VALUES (10751, 'Familia') on conflict do nothing;
                            INSERT INTO genres VALUES (14, 'Fantasia') on conflict do nothing;
                            INSERT INTO genres VALUES (36, 'Historia') on conflict do nothing;
                            INSERT INTO genres VALUES (27, 'Horror') on conflict do nothing;
                            INSERT INTO genres VALUES (10402, 'Musical') on conflict do nothing;
                            INSERT INTO genres VALUES (9648, 'Misterio') on conflict do nothing;
                            INSERT INTO genres VALUES (10749, 'Romance') on conflict do nothing;
                            INSERT INTO genres VALUES (878, 'Ciencia Ficción') on conflict do nothing;
                            INSERT INTO genres VALUES (10770, 'Película de TV') on conflict do nothing;
                            INSERT INTO genres VALUES (53, 'Thriller') on conflict do nothing;
                            INSERT INTO genres VALUES (10752, 'Guerra') on conflict do nothing;
                            INSERT INTO genres VALUES (37, 'Western') on conflict do nothing;
                            """)


class CursorFromConnectionFromPool:
    def __init__(self):
        self.connection = None
        self.cursor = None
    
    def __enter__(self):
        self.connection = Database.get_connection()
        self.cursor = self.connection.cursor()
        return self.cursor
    
    def __exit__(self, exception_type, exception_value, exception_traceback):
        if exception_value is not None:
            self.connection.rollback()
        else:
            self.cursor.close()
            self.connection.commit()
        Database.return_connection(self.connection)