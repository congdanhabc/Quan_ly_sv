from view.login import UserApp
from check_qdrant import check_qdrant_connection

check_qdrant_connection()
app = UserApp()
