from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.views.generic import View
from .models import CompetitionModel
from .forms import AddPlayerForm
import json


class CompetitionPage(View):

    def get(self, request, title="AmongUsThird"):


        competitionModel = CompetitionModel.objects.get(title=title)

        raw_data = json.loads(competitionModel.json_raw_data)
        players = [ {"name" : one_player['name'] } for one_player in raw_data]

        if request.is_ajax():
            print("Returning Json")
            return JsonResponse({'players': players, 'raw_data': raw_data}, status=200)

        context = {
            "title" : "Among Us Competition",
        }

        return render(request, "competition/homepage.html", context=context)

    def post(self, request, title="AmongUsThird"):

        title = "AmongUsThird"

        form_data = request.POST
        print(form_data)

        if form_data['action'] == "add_player":
            new_player = form_data["name"]

            competition_model = CompetitionModel.objects.get(title=title)
            new_json_raw_data = json.loads( competition_model.json_raw_data )
            print(new_json_raw_data)

            new_json_raw_data.append({"name": new_player, "score": 0, "wins": 0, "losses": 0})
            print(new_json_raw_data)

            new_json_raw_data = json.dumps(new_json_raw_data)
            competition_model.json_raw_data = new_json_raw_data
            competition_model.save()

            return JsonResponse({"name": new_player, "score": 0, "wins": 0, "losses": 0})

        if form_data['action'] == "update_winners":
            winner_players = form_data["winners"]

            print(winner_players)

            competition_model = CompetitionModel.objects.get(title=title)
            new_json_raw_data = json.loads(competition_model.json_raw_data)

            for i, element in enumerate(new_json_raw_data):
                if element["name"] in winner_players:
                    new_json_raw_data[i]["wins"] += 1
                    try:
                        new_json_raw_data[i]["score"] = round(new_json_raw_data[i]["wins"] / ( new_json_raw_data[i]["losses"] + new_json_raw_data[i]["wins"]), 2)
                    except Exception as ex:
                        print(ex)

            competition_model.json_raw_data = json.dumps(new_json_raw_data)
            competition_model.save()

            raw_data = new_json_raw_data
            players = [ {"name" : one_player['name'] } for one_player in raw_data]

            return JsonResponse({'raw_data': raw_data}, safe=False)

        if form_data['action'] == "update_loosers":
            looser_players = form_data["loosers"]

            print(looser_players)

            competition_model = CompetitionModel.objects.get(title=title)
            new_json_raw_data = json.loads(competition_model.json_raw_data)

            for i, element in enumerate(new_json_raw_data):
                if element["name"] in looser_players:
                    new_json_raw_data[i]["losses"] += 1
                    try:
                        new_json_raw_data[i]["score"] = round(new_json_raw_data[i]["wins"] / ( new_json_raw_data[i]["losses"] + new_json_raw_data[i]["wins"]), 2)
                    except Exception as ex:
                        print(ex)

            competition_model.json_raw_data = json.dumps(new_json_raw_data)
            competition_model.save()

            raw_data = new_json_raw_data
            players = [ {"name" : one_player['name'] } for one_player in raw_data]

            return JsonResponse({'raw_data': raw_data}, safe=False)

        if form_data['action'] == "remove_players":
            names = form_data["names"]

            print(names)

            competition_model = CompetitionModel.objects.get(title=title)
            new_json_raw_data = json.loads(competition_model.json_raw_data)

            for i, element in enumerate(new_json_raw_data):
                if element["name"] in names:
                    new_json_raw_data.pop(i)

            competition_model.json_raw_data = json.dumps(new_json_raw_data)
            competition_model.save()

            raw_data = new_json_raw_data
            players = [ {"name" : one_player['name'] } for one_player in raw_data]

            print("Returning raw_data_json")
            return JsonResponse({'raw_data': raw_data}, safe=False)

        return redirect('competition:home_page')