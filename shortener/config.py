class Config:

class DevelopConfig(Config):
    DEBUG = True
    DATABASE_HOST = 'localhost'

class ProductionConfig(Config):
    DEBUG = False

app_config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig
}