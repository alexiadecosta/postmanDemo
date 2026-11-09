from flask import Flask, request, jsonify
import random 
import threading

app=Flask(__name__)
attempts=0
winner=None
ticketCounter=0

lock=threading.Lock() #prevents requests from making several winners
@app.route("/api/lottery/tickets", methods=["POST"])
def makeTicket():
    global attempts, winner, ticketCounter
    data=request.get_json(silent=True) or {}
    student_name=data.get("student_name", "Anonymous")
    with lock:
        if winner is not None:
            return jsonify({ "success":False, "message": "Someone has already won the lottery! :O", "winner":winner}),409
        attempts += 1
        ticketCounter +=1
        probability = 0.03 if attempts <=10 else 0.15
        isWinner = random.random() < probability
        ticket = {"ticketId": f"TICKET-{ticketCounter:04d}", "ticketNumber": random.randint(100000, 999999), "student_name": student_name, "attempt": attempts, "winning": is_winner}
        if isWinner:
            winner = student_name
            ticket["message"]=(f"JACKPOT! Congrats, {student_namee}! ദ്ദി( •̀ ᴗ - )")
        else: 
            ticket["message"]="Not a winner, try again! (╥﹏╥)"
        return jsonify({"success":True, "ticket": ticket, "game_status": "WON" if isWinner else "ACTIVE"}), 200
@app.route("/api/lottery/status",methods=["GET"])
def lotteryStatus():
    return jsonify({"totalAttempts":attempts, "game_status":"WON" if winner else "ACTIVE", "winner": winner}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)

        
