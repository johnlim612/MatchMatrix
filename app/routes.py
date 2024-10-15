from flask import Blueprint, render_template, request, jsonify
from app import MatchMaking
from app import PlayerManager
from app import FileManager
import json

main = Blueprint('main', __name__, template_folder='templates')


@main.route('/', methods=["GET"])
def upload():
    return render_home_page()


@main.route('/list_students', methods=["GET"])
def upload_student_list():
    player_list = PlayerManager.list_players()
    return render_template("student_list.html", players=player_list)


@main.route('/delete_player', methods=["POST"])
def delete_player():
    player_name = request.form.get("player_name")
    PlayerManager.delete_player(player_name)
    return "deleted successfully", 200


@main.route("/search", methods=["GET"])
def search_name():
    search_term = request.args.get('search_term', '').lower()
    result_names = PlayerManager.search_player(search_term)
    return jsonify(result_names)


@main.route('/new')
def upload_new_student_form():
    return render_template("new_student.html")


@main.route('/submit_student_form', methods=['POST'])
def submit_student():
    data = request.form.to_dict()
    PlayerManager.SubmitNewStudent(data)
    return render_home_page()


@main.route('/create_teams', methods=["GET"])
def create_team():
    player_list_json = request.args.get('added_players')
    player_list = json.loads(player_list_json)

    team1, team2 = MatchMaking.get_balanced_teams(player_list)
    return jsonify(team1, team2)


@main.route('/submit-results', methods=['POST'])
def submit_results():
    data = request.json  # Get the JSON data from the request
    winning_players = data.get('winningPlayers', [])
    losing_players = data.get('losingPlayers', [])

    MatchMaking.update_players_ratings(winning_players, losing_players)
    FileManager.update_last_submitted()
    response_data = {'message': 'Match results received successfully'}
    return jsonify(response_data)


def render_home_page():
    player_list = PlayerManager.list_players(True)
    last_submitted_data = FileManager.open_last_submitted_data()
    return render_template("create_match.html", players=player_list, last_submitted=last_submitted_data)
