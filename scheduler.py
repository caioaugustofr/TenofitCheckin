# -*- coding: utf-8 -*-
"""
Created on Thu Apr 22 11:00:05 2021

@author: CRIBE2
"""

import json
import requests
import datetime

# =============================================================================
# INITIAL VARIABLES
# =============================================================================
URL_PREFIX = 'https://app.tecnofit.com.br'

TOKENS = ({"nome": 'Pessoa 1', "token":'AB78912310ACEF120938DEE', "hora_checkin": '06:00'},
          {"nome": 'Pessoa 2', "token":'Token 2', "hora_checkin": '08:00'},)


# =============================================================================
# Getting Tomrrow's Date to use in Requests
# =============================================================================
DateToday = datetime.date.today()
DateTomorrow = DateToday + datetime.timedelta(days=1)
DateTomorrowStr = datetime.datetime.strftime(DateTomorrow, "%d/%m/%Y")
print("Date Tomorrow: " + DateTomorrowStr)


# =============================================================================
# Getting Tomorrow's Sessions Available
# =============================================================================
for iToken in TOKENS:
    TOKEN = iToken["token"]
    HOUR_CHECKIN = iToken["hora_checkin"]
    EndpointTomorrowSession = '/ws/app-crossfit?m=listaProgramasDia&wsToken=' + TOKEN + '&data=' + DateTomorrowStr + '&crossfit_programa_id=&buttonInfo=0'
    rTomorrowSession = requests.get(URL_PREFIX + EndpointTomorrowSession)
    Sessions = json.loads(rTomorrowSession.text)
    
    #Getting the Variables Needed for Checkin
    crossfit_agenda_horario_id = ""
    crossfit_programa_id = ""
    print ("")
    print ("---------------------------------")
    print ("Checkin for: " + iToken["nome"])
    print ("---------------------------------")
    print ("Looping the sessions to find one that starts in desired time: " + HOUR_CHECKIN)
    for session in Sessions[0]["dados"]:
        print ("Start Time: " + session["hora_inicio"])
        if (session["hora_inicio"]==HOUR_CHECKIN):
            crossfit_agenda_horario_id = session["agenda_horario_id"]
            crossfit_programa_id = session["programa_id"]
            break
    
    if (not crossfit_agenda_horario_id):
        print ("Time not found for tomorrow.")
        continue
    
    print("crossfit_agenda_horario_id: " + crossfit_agenda_horario_id)
    print("crossfit_programa_id: " + crossfit_programa_id)
    
    # =============================================================================
    # Trying to Checkin
    # =============================================================================
    checkin_success = 0
    print("")
    print("TRYING TO CHECK IN " + DateTomorrowStr + " " + HOUR_CHECKIN)
    EndpointCheckin = '/ws/app-crossfit?m=checkinAluno&wsToken=' + TOKEN + '&data=' + DateTomorrowStr + '&crossfit_agenda_horario_id=' + crossfit_agenda_horario_id + '&crossfit_programa_id=' + crossfit_programa_id + ''
    rCheckin = requests.get(URL_PREFIX + EndpointCheckin)
    jCheckin = json.loads(rCheckin.text)
    
    if (jCheckin[0]["resultado"] == "1"):
        print ("CHECKIN DONE in First Attempt")
        checkin_success = 10
    
    
    # =============================================================================
    # If Checkin Fails, Submit Class Evaluation
    # =============================================================================
    while (checkin_success < 2):
        print ("Checkin Failed!")
        print ("")
        print ("Trying to search for a pending Evaluation...")
        crossfit_checkin_id = ""
        try:
            crossfit_checkin_id = jCheckin[0]["dados"][0]["crossfit_checkin_id"]
        except:
            print("Pending Evaluation not found")
            print("CHECKIN FAILED")
            checkin_success = 5
        if (crossfit_checkin_id):
            print ("Pending Evaluation found: " + crossfit_checkin_id)
            print("")
            print ("Answering Evaluation")
            EndpointEvaluation = '/ws/app-crossfit?m=gravarAvaliacao&wsToken=' + TOKEN + '&crossfit_checkin_id=' + crossfit_checkin_id + '&choach_avaliacao=10&workout_avaliacao=10&observacoes=&anonimo=0&auxiliar=1&choach_aux_avaliacao=10'
            requests.get(URL_PREFIX + EndpointEvaluation)
            print ("Evaluation Answered")
            print ("")
            print ("TRYING TO CHECK IN AGAIN")
            rCheckin = requests.get(URL_PREFIX + EndpointCheckin)
            jCheckin = json.loads(rCheckin.text)
            if (jCheckin[0]["resultado"] == "1"):
                print ("CHECKIN DONE")
                checkin_success = 10
            else:
                checkin_success += 1 
        else:
            checkin_success = 5