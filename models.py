from datetime import datetime
from sqlalchemy import (
    Column, Integer, String, ForeignKey, DateTime, Numeric, CheckConstraint
)
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

# ===== MODELS =====
class Cliente(Base):
    __tablename__ = "clientes"

    id = Column(Integer, primary_key=True)
    nome = Column(String(120), nullable=False)
    email = Column(String(120), nullable=False, unique=True)
    telefone = Column(String(20))

    pedidos = relationship("Pedido", back_populates="cliente", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Cliente id={self.id} nome={self.nome!r} email={self.email!r}>"

class Produto(Base):
    __tablename__ = "produtos"

    id = Column(Integer, primary_key=True)
    titulo = Column(String(160), nullable=False)
    plataforma = Column(String(40), nullable=False)
    preco = Column(Numeric(10, 2), nullable=False)
    estoque = Column(Integer, nullable=False, default=0)

    __table_args__ = (
        CheckConstraint("preco >= 0", name="ck_produto_preco"),
        CheckConstraint("estoque >= 0", name="ck_produto_estoque"),
    )

    itens = relationship("ItemPedido", back_populates="produto")

    def __repr__(self):
        return f"<Produto id={self.id} titulo={self.titulo!r} plataforma={self.plataforma!r} preco={self.preco}>"

class Pedido(Base):
    __tablename__ = "pedidos"

    id = Column(Integer, primary_key=True)
    data_pedido = Column(DateTime, default=datetime.utcnow, nullable=False)
    cliente_id = Column(Integer, ForeignKey('clientes.id'), nullable=False)
    status = Column(String(40), nullable=False)

    cliente = relationship("Cliente", back_populates="pedidos")
    itens = relationship("ItemPedido", back_populates="pedido", cascade="all, delete-orphan")

    def total(self):
        return sum((it.quantidade * it.preco_unitario) for it in self.itens)

    def __repr__(self):
        return f"<Pedido id={self.id} cliente_id={self.cliente_id} status={self.status!r} data_pedido={self.data_pedido}>"

class ItemPedido(Base):
    __tablename__ = "itens_pedido"

    id = Column(Integer, primary_key=True)
    pedido_id = Column(Integer, ForeignKey('pedidos.id'), nullable=False)
    produto_id = Column(Integer, ForeignKey('produtos.id'), nullable=False)
    quantidade = Column(Integer, nullable=False, default=1)
    preco_unitario = Column(Numeric(10, 2), nullable=False)

    pedido = relationship("Pedido", back_populates="itens")
    produto = relationship("Produto", back_populates="itens")

    def __repr__(self):
        return f"<ItemPedido id={self.id} pedido_id={self.pedido_id} produto_id={self.produto_id} quantidade={self.quantidade} preco_unitario={self.preco_unitario}>"


# =============== CONEXÕES E SESSÕES ===============

def get_engine(db_url: str = "sqlite:///loja_jogos.db"):
    return create_engine(db_url, echo=False, future=True)

def create_session(db_url: str = "sqlite:///loja_jogos.db"):
    engine = get_engine(db_url)
    Base.metadata.create_all(engine)
    SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)
    return SessionLocal()
