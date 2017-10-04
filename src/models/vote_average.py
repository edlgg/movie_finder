from src.common.database import Database, CursorFromConnectionFromPool


class Vote_average:
    def __init__(self, id, description):
        self.id = id
        self.description = description

    def __repr__(self):
        return "<Genre {}>".format(self.description)


    @classmethod
    def load_by_id(cls, id):
        with CursorFromConnectionFromPool() as cursor:
                cursor.execute("SELECT * FROM vote_averages WHERE id=%s", (id,))
                movie_data = cursor.fetchone()
                if movie_data:
                    return cls(id=movie_data[0], description=movie_data[1])
    
    def json(self):
        return{
                'id': self.id,
                'description': self.description
             }
