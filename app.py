import os
from datetimerange import DateTimeRange
from flask import Flask, redirect,render_template,request,url_for

app = Flask(__name__)
app.config["SECRET_KEY"] = os.urandom(12).hex()

karte = []

@app.route("/")
def home():
    return render_template("index.html",karte=karte)



@app.route("/dodaj-kartu",methods=["GET","POST"])
def dodaj_kartu():
    if request.method == "POST":
        nova_karta = dict(request.form)
        
        #projekcija koja se trenutno treba dodati u listu
        pocetak = nova_karta["datum_vreme_projekcije"] #pocetak projekcije
        kraj = nova_karta["datum_vreme_zavrsetka"] #kraj projekcije
        novi_interval = DateTimeRange(pocetak,kraj) # interval porediti sa intervalom

        greska = False

        if len(karte) != 0:
            
            for i in range(len(karte)):
                #projekcije iz liste
                pocetak_projekcije = karte[i]["datum_vreme_projekcije"]
                print(pocetak_projekcije) 
                kraj_projekcije = karte[i]["datum_vreme_zavrsetka"]
                print(kraj_projekcije)
                interval_vremena = DateTimeRange(pocetak_projekcije,kraj_projekcije)
                
                if(pocetak in interval_vremena) or (kraj in interval_vremena) or (interval_vremena in novi_interval):
                    greska = True
                    break
                else:
                    continue

            if greska == False:
                for i in karte:
                    if i["id"] != nova_karta["id"]:
                        karte.append(nova_karta)
                    else:
                        return render_template("greska.html")
            else:
                return render_template("greska.html")

        else:
            karte.append(nova_karta)

        return redirect(url_for('home'))
    return render_template("dodaj_forma.html")





@app.route("/izmeni/<int:id>",methods=["GET","POST"])
def izmeni(id):
    index = id - 1
    karta = karte[index]
    if request.method == "POST":
        nova_karta = dict(request.form)
    
        pocetak = nova_karta["datum_vreme_projekcije"]
        kraj = nova_karta["datum_vreme_zavrsetka"] 
        novi_interval = DateTimeRange(pocetak,kraj)
        
        if karta["datum_vreme_projekcije"] == nova_karta["datum_vreme_projekcije"] \
            and karta["datum_vreme_zavrsetka"] == nova_karta["datum_vreme_zavrsetka"]:
            karte[index] = nova_karta
            return redirect(url_for('home'))
        else:

            greska = False

            if len(karte) > 1:
                for i in range(len(karte)):
                    if i == index:
                        continue
                    pocetak_projekcije = karte[i]["datum_vreme_projekcije"]
                    kraj_projekcije = karte[i]["datum_vreme_zavrsetka"]
                    interval_vremena = DateTimeRange(pocetak_projekcije,kraj_projekcije)
                    
                    if(pocetak in interval_vremena) or (kraj in interval_vremena) or (interval_vremena in novi_interval):
                        greska = True
                        break
                    else:
                        continue

                if greska == False:
                    karte[index] = nova_karta
                else:
                    return render_template("greska.html")
            else:
                karte[index] = nova_karta
            return redirect(url_for('home'))
    return render_template("izmeni_forma.html",karta=karta,id=id)


@app.route("/obrisi/<int:id>")
def obrisi(id):
    id_karte = id - 1
    karte.pop(id_karte)
    
    return redirect(url_for('home'))


if __name__ == "__main__":
    app.run()