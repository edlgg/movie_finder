from common.database import Database, CursorFromConnectionFromPool

class Actor:
    def __init__(self, id, name, image):
        self.id = id
        self.name = name
        self.image = image

    def __repr__(self):
        return "<Name {}>".format(self.name)

    def save_to_db(self):
        with CursorFromConnectionFromPool() as cursor:
            cursor.execute("INSERT INTO actors (id, name, image) VALUES (%s, %s, %s) on conflict do nothing",(self.id, self.name, self.image))

    @classmethod
    def load_by_id(cls, id):
        with CursorFromConnectionFromPool() as cursor:
                cursor.execute("SELECT * FROM actors WHERE id=%s", (id,))
                director = cursor.fetchone()
                if director:
                    return cls(id=director[0], name=director[1], image=director[2])
    
    def json(self):
        return{
                'id': self.id,
                'name': self.name,
                'image':self.image
             }

class Actors:

    def __init__(self, name):
        self.name = name
    
    def json(self):
        return{
                'name': self.name
             }

    @classmethod
    def load_all_list_name(cls):
        with CursorFromConnectionFromPool() as cursor:
            cursor.execute("SELECT distinct name FROM actors")
            actors_data = cursor.fetchall()
            if actors_data:
                actors = []
                for actor in actors_data:
                    actors.append(actor[0])
                return actors
    
    @classmethod
    def load_by_movie_id(cls, id):
        with CursorFromConnectionFromPool() as cursor:
            cursor.execute("SELECT * FROM acts_in where movie_id = %s",(id,))
            acts_in = cursor.fetchall()
            if acts_in:
                actor_ids = []
                for actor in acts_in:
                    actor_ids.append(actor[1])
            #now I have a list with the 4 actor ids, now I have to create a list with the classes
            actors=[]
            
            for id in actor_ids:
                class_actor = Actor.load_by_id(id)
                if class_actor:
                    actors.append(class_actor)

            return actors

    


