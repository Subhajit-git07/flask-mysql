from my_app import app
#app.run(host='10.163.58.53',debug=True)

app.run(
    host=app.config.get("HOST", "10.163.58.53"),
    port=app.config.get("PORT", 5001),debug=True
    )     
