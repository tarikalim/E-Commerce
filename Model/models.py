from sqlalchemy import Enum
import enum
from extensions import db


class OrderStatus(enum.Enum):
    PLACED = 'Order Placed'
    SHIPPED = 'Shipped'
    DELIVERED = 'Delivered'
    CANCELLED = 'Cancelled'


class PaymentType(enum.Enum):
    PAY_DOOR = 'Pay at the door'
    CREDIT_CARD = 'Credit Card'


class Product(db.Model):
    __tablename__ = 'Products'
    ProductID = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(100), nullable=False)
    Price = db.Column(db.Numeric(10, 2), nullable=False)
    StockQuantity = db.Column(db.Integer, default=0)
    Description = db.Column(db.Text)
    CategoryID = db.Column(db.Integer, db.ForeignKey('Categories.CategoryID'))
    # Relationships
    category = db.relationship('Category', back_populates='products')
    cartdetails = db.relationship('CartDetail', back_populates='product')
    orderdetails = db.relationship('OrderDetail', back_populates='product')
    reviews = db.relationship('Review', back_populates='product')

    def to_dict(self):
        return {
            'product_id': self.ProductID,
            'name': self.Name,
            'price': str(self.Price),
            'stock_quantity': self.StockQuantity,
            'description': self.Description,
            'category_id': self.CategoryID,

        }


class User(db.Model):
    __tablename__ = 'Users'
    UserID = db.Column(db.Integer, primary_key=True)
    Username = db.Column(db.String(50), nullable=False, unique=True)
    Password = db.Column(db.String(255), nullable=False)
    Email = db.Column(db.String(100))
    Address = db.Column(db.Text)
    CreditCardID = db.Column(db.String(16))
    # Relationships
    carts = db.relationship('Cart', back_populates='user')
    orders = db.relationship('Order', back_populates='user')
    reviews = db.relationship('Review', back_populates='user')


class Cart(db.Model):
    __tablename__ = 'Cart'
    CartID = db.Column(db.Integer, primary_key=True)
    UserID = db.Column(db.Integer, db.ForeignKey('Users.UserID'))
    # Relationships
    user = db.relationship('User', back_populates='carts')
    cartdetails = db.relationship('CartDetail', back_populates='cart')


class CartDetail(db.Model):
    __tablename__ = 'CartDetails'
    CartID = db.Column(db.Integer, db.ForeignKey('Cart.CartID'), primary_key=True)
    ProductID = db.Column(db.Integer, db.ForeignKey('Products.ProductID'), primary_key=True)
    Quantity = db.Column(db.Integer, default=1)
    # Relationships
    cart = db.relationship('Cart', back_populates='cartdetails')
    product = db.relationship('Product', back_populates='cartdetails')


class Order(db.Model):
    __tablename__ = 'Orders'
    OrderID = db.Column(db.Integer, primary_key=True)
    UserID = db.Column(db.Integer, db.ForeignKey('Users.UserID'), nullable=False)
    OrderDate = db.Column(db.Date, nullable=False)
    Status = db.Column(Enum(OrderStatus), nullable=False)
    Address = db.Column(db.String(255), nullable=False)
    PaymentType = db.Column(Enum(PaymentType), nullable=False)
    # Relationships
    user = db.relationship('User', back_populates='orders')
    orderdetails = db.relationship('OrderDetail', back_populates='order')


class OrderDetail(db.Model):
    __tablename__ = 'OrderDetails'
    OrderID = db.Column(db.Integer, db.ForeignKey('Orders.OrderID'), primary_key=True)
    ProductID = db.Column(db.Integer, db.ForeignKey('Products.ProductID'), primary_key=True)
    Quantity = db.Column(db.Integer)
    SalePrice = db.Column(db.Numeric(10, 2))
    # Relationships
    order = db.relationship('Order', back_populates='orderdetails')
    product = db.relationship('Product', back_populates='orderdetails')


class Category(db.Model):
    __tablename__ = 'Categories'
    CategoryID = db.Column(db.Integer, primary_key=True)
    CategoryName = db.Column(db.String(100))
    Description = db.Column(db.Text)
    # Relationships
    products = db.relationship('Product', back_populates='category')


class Review(db.Model):
    __tablename__ = 'Review'
    ReviewID = db.Column(db.Integer, primary_key=True)
    UserID = db.Column(db.Integer, db.ForeignKey('Users.UserID'), nullable=False)
    ProductID = db.Column(db.Integer, db.ForeignKey('Products.ProductID'), nullable=False)
    Date = db.Column(db.Date, nullable=False)
    Comment = db.Column(db.Text, nullable=False)
    Rate = db.Column(db.Integer, nullable=False)
    # Relationships
    user = db.relationship('User', back_populates='reviews')
    product = db.relationship('Product', back_populates='reviews')


class Admin(db.Model):
    __tablename__ = 'Admins'
    AdminID = db.Column(db.Integer, primary_key=True)
    Password = db.Column(db.String(200), nullable=False)
