from flask import Blueprint, render_template, Flask
from .models import Match, GoalScorer, db
import os
import pandas as pd

main = Blueprint('main', __name__)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///football.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

@main.route('/')
def index():
    matches = Match.query.order_by(Match.date.desc()).limit(20).all()
    return render_template('index.html', matches=matches)

@main.route('/match/<int:match_id>')
def match_detail(match_id):
    match = Match.query.get_or_404(match_id)
    goals = GoalScorer.query.filter_by(match_id=match_id).order_by(GoalScorer.minute).all()
    return render_template('detail.html', match=match, goals=goals)

def create_db():
    with app.app_context():
        db.create_all()

        if Match.query.first() is None:
            df = pd.read_excel('data/data.xlsx')
            for _, row in df.iterrows():
                match = Match(
                    home_team=row['home_team'],
                    away_team=row['away_team'],
                    home_score=row['home_score'],
                    away_score=row['away_score'],
                    tournament_id=row['tournament'],
                    date=row['goal_date'],
                    match_city=row['city'],
                    match_country=row['country'],
                )
                db.session.add(match)
                db.session.flush()
                
                goalScorer = GoalScorer(
                    home_team=row['home_team'],
                    away_team=row['away_team'],
                    team_scored=row['team_scored'],
                    scorer=row['scorer'],
                    minute=row['minute'],
                    match_id=row['match_id'],
                    date=row['goal_date'],
                )
                db.session.add(goalScorer)
                db.session.commit()

create_db()