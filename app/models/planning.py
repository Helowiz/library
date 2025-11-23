from app.extensions import db

class MonthlyPAL(db.Model):
    __tablename__ = "monthly_pal"
    id = db.Column(db.Integer, primary_key=True)
    month = db.Column(db.Integer, nullable=False) 
    year = db.Column(db.Integer, nullable=False)
    theme = db.Column(db.String(100), nullable=True)
    
    selections = db.relationship("MonthlyBookSelection", back_populates="monthly_pal", cascade="all, delete-orphan")

    __table_args__ = (db.UniqueConstraint('month', 'year', name='_month_year_uc'),)

    def __repr__(self):
        return f"<PAL {self.month}/{self.year}>"

class MonthlyBookSelection(db.Model):
    __tablename__ = "monthly_book_selection"
    id = db.Column(db.Integer, primary_key=True)
    
    monthly_pal_id = db.Column(db.Integer, db.ForeignKey('monthly_pal.id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
    
    priority = db.Column(db.Integer, default=1)
    
    note = db.Column(db.String(200), nullable=True)

    monthly_pal = db.relationship("MonthlyPAL", back_populates="selections")
    book = db.relationship("Book")