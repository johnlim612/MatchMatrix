from flask import *
import MatchMaking
import FileManager

app=Flask(__name__)

@app.route('/', methods=["GET"])
def upload():
    player_list = MatchMaking.list_players(True)
    last_submitted_data = FileManager.open_last_submitted_data()
    return render_template("create_match.html", players=player_list, last_submitted = last_submitted_data)

@app.route('/home')
def upload_home():
    return render_template("match_making.html")

@app.route('/start_match')
def upload_matchmaking():
    return render_template("create_match.html")

@app.route('/list_students', methods=["GET"])
def upload_student_list():
    player_list = MatchMaking.list_players()
    return render_template("student_list.html", players=player_list)

@app.route('/delete_player', methods=["POST"])
def delete_player():
    player_name = request.form.get("player_name")
    MatchMaking.delete_player(player_name)
    return "deleted successfully", 200

@app.route("/search", methods=["GET"])
def search_name():
    search_term = request.args.get('search_term', '').lower()
    result_names = MatchMaking.search_player(search_term)
    return jsonify(result_names)

@app.route('/new')
def upload_new_student_form():
    return render_template("new_student.html")

@app.route('/submit_student_form', methods=['POST'])
def submit_student():
    data = request.form.to_dict()
    MatchMaking.SubmitNewStudent(data)
    return render_template("create_match.html")

@app.route('/create_teams', methods=["GET"])
def create_team():
    player_list_json = request.args.get('added_players')
    player_list = json.loads(player_list_json)

    team1, team2 = MatchMaking.create_teams(player_list)
    return jsonify(team1, team2)

@app.route('/submit-results', methods=['POST'])
def submit_results():
    data = request.json  # Get the JSON data from the request
    winning_players = data.get('winningPlayers', [])
    losing_players = data.get('losingPlayers', [])

    MatchMaking.update_players_ratings(winning_players, losing_players)
    FileManager.update_last_submitted()
    response_data = {'message': 'Match results received successfully'}
    return jsonify(response_data)


if __name__ == "__main__":
    app.run(debug = True)

