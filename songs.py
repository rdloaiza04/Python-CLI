import sqlite3
sqlConnection =  sqlite3.connect('de-challenge.db')
c = sqlConnection.cursor()
class Songs:
    '''
    Class constructor, assigned all the values retreived from the API
    '''
    def __init__(self, artist, duration, name, released_at, song_id, global_rank, last_played_at, times_played):
        self.artist = artist
        self.duration = duration
        self.name = name
        self.released_at = released_at
        self.song_id = song_id
        self.global_rank = global_rank
        self.last_played_at = last_played_at
        self.times_played = times_played
    
    '''
    Function that can insert new songs into the song database
    I: None
    O: None
    '''
    def insertData(self):
        #Conditionals checking if the data received contains an stats = (last_played_at, global_rank, times_played)
        if self.last_played_at != "":
            c.execute("""INSERT INTO song (song_id, released_at, duration_seconds, artist, name, last_played_at, times_played, global_rank) 
            VALUES (:song_id, :released_at, :duration_seconds, :artist, :name, :last_played_at, :times_played, :global_rank)""", 
            {'song_id': self.song_id, 
            'released_at': self. released_at, 
            'duration_seconds': self.duration, 
            'artist':self.artist, 
            'name':self.name, 
            'last_played_at':self.last_played_at, 
            'times_played': self.times_played,
            'global_rank':self.global_rank})
            sqlConnection.commit()

        else:
            c.execute("INSERT INTO song (song_id, released_at, duration_seconds, artist, name) VALUES (:song_id, :released_at, :duration_seconds, :artist, :name)", 
            {'song_id': self.song_id, 
            'released_at': self. released_at, 
            'duration_seconds': self.duration, 
            'artist':self.artist, 
            'name':self.name, 
            })
            sqlConnection.commit()

    '''
    Function that check the existence of a value in a database, in this case, from song database
    I: None
    O: data, with the name associated to the song_id
    '''
    def checkExistence(self):
        c.execute("SELECT name FROM song WHERE song_id=:song_id",{'song_id':self.song_id})
        sqlConnection.commit()
        data = c.fetchall()
        return data

    '''
    Function that can update an entire song from song database
    I: None
    O: None
    '''
    def updateData(self):
        c.execute("""UPDATE song SET released_at = :released_at, duration_seconds = :duration_seconds, artist = :artist, 
                    name = :name, last_played_at = :last_played_at, times_played = :times_played, global_rank = :global_rank
                    WHERE song_id = :song_id""",
            {'song_id': self.song_id, 
            'released_at': self. released_at, 
            'duration_seconds': self.duration, 
            'artist':self.artist, 
            'name':self.name, 
            'last_played_at':self.last_played_at, 
            'times_played': self.times_played,
            'global_rank':self.global_rank})
        sqlConnection.commit()
    
###############################################
##############Extra Functionality##############
###############################################
    '''
    Function that can update a value from an specific field of a determined song, identified by song_id
    I: field, newValue, song_id
    O: None
    '''
    def updateOneField(self, field, newValue, song_id):
        c.execute("""UPDATE song SET :field = :newValue
                    WHERE song_id = :song_id""",
                  {'song_id':song_id, 
                  'field':field, 
                  'newValue': newValue})
        sqlConnection.commit()

    '''
    Function that can delete a value from a database, in this case, from song database
    I: song_id
    O: None
    '''
    @staticmethod
    def deleteData(song_id):
        c.execute("DELETE from song WHERE song_id = :song_id", {'song_id': song_id})
        sqlConnection.commit()