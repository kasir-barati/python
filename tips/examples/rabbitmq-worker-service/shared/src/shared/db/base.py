from sqlalchemy.orm import DeclarativeBase


# Lives outside any entity's own package (db/user, a future db/order, ...)
# so that every entity's model imports the same Base without depending on
# whichever entity happened to define it first.
class Base(DeclarativeBase):
    pass
