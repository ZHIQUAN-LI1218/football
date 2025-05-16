from app.extensions import db

class Tournament(db.Model):
    __tablename__ = 'tournaments'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)

    matches = db.relationship('Match', backref='tournament', lazy=True)


class Match(db.Model):
    __tablename__ = 'matches'
    id = db.Column(db.Integer, primary_key=True)
    home_team = db.Column(db.String, nullable=False)
    away_team = db.Column(db.String, nullable=False)
    home_score = db.Column(db.Integer)
    away_score = db.Column(db.Integer)
    tournament_id = db.Column(db.Integer, db.ForeignKey('tournaments.id'))
    date = db.Column(db.String)
    match_city = db.Column(db.String)
    match_country = db.Column(db.String)

    goals = db.relationship('GoalScorer', backref='match', lazy=True)


class GoalScorer(db.Model):
    __tablename__ = 'goal_scorers'
    id = db.Column(db.Integer, primary_key=True)
    home_team = db.Column(db.String)
    away_team = db.Column(db.String)
    team_scored = db.Column(db.String)
    scorer = db.Column(db.String)
    minute = db.Column(db.Integer)
    match_id = db.Column(db.Integer, db.ForeignKey('matches.id'))
    date = db.Column(db.String)
