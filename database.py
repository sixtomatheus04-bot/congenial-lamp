# Mude disto:
# DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./ecommerce.db")

# Para isto (apenas para teste):
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///:memory:")
