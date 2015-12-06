class Constants:
    HOST = '127.0.0.1'
    TEMP = ['Clinton', 'clinton','Hillary', 'Sanders','sanders','FeelTheBern','Trump', 'trump','hillaryclinton','rubio', 'jeb','Jeb','Carson','carson','Fiorina','fiorina','Ted Cruz','TedCruz','Jindal','jindal','Rand','rand']
    PORT = 8000
    KEYWORDS = {'Hillary Clinton': ['Clinton', 'clinton', 'Hillary', 'Hillary Clinton','HillaryClinton'], 
    			'Carly Fiorina':['Fiorina', 'fiorina', 'Carly Fiorina','CarlyFiorina'],
    			'Bernie Sanders':['Sanders', 'sanders', 'Bernie Sanders','FeelTheBern','BernieSanders'], 
    			'Marco Rubio':['rubio', 'Rubio', 'Marco Rubio','MarcoRubio'], 
    			'Donald Trump':['Trump', 'Donald Trump', 'trump','DonaldTrump'],
    			'Ted Cruz': ['Ted Cruz', 'TedCruz', 'cruz','TedCruz'],
    			'Ben Carson':['Carson', 'carson','Ben Carson','BenCarson'],
    			'Rand Paul':['Rand', 'rand', 'Rand Paul','RandPaul']}
    def __init__(self):
        pass

    def set_host(self, host):
        self.HOST = host


