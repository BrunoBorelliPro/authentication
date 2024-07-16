from sqlalchemy.orm import Mapped, mapped_column, registry

table_registry = registry()


@table_registry.mapped_as_dataclass
class User:
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(
        primary_key=True, autoincrement=True, init=False
    )
    username: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str] = mapped_column()
