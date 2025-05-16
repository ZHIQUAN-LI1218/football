from flask import Blueprint, render_template
from .models import Match, GoalScorer

main = Blueprint('main', __name__)

@main.route('/')
def index():
    matches = Match.query.order_by(Match.date.desc()).limit(20).all()
    return render_template('index.html', matches=matches)

@main.route('/match/<int:match_id>')
def match_detail(match_id):
    match = Match.query.get_or_404(match_id)
    goals = GoalScorer.query.filter_by(match_id=match_id).order_by(GoalScorer.minute).all()
    return render_template('detail.html', match=match, goals=goals)
