#!/usr/bin/env python3
"""Independent validation of decline.py against hand-verified forms."""
import sys; sys.path.insert(0,'.')
from decline import derive
# (word, slot, expected). Forms cross-checked against Kotus model paradigms
# and standard reference grammars.
CASES = [
 ("katto","sg gen","katon"),("katto","sg part","kattoa"),("katto","sg illat","kattoon"),
 ("katto","pl part","kattoja"),("katto","pl gen","kattojen"),
 ("takki","sg gen","takin"),("takki","sg part","takkia"),("takki","pl part","takkeja"),
 ("takki","sg illat","takkiin"),("takki","pl gen","takkien"),
 ("tyttö","sg gen","tytön"),("tyttö","sg part","tyttöä"),("tyttö","pl part","tyttöjä"),
 ("kaupunki","sg gen","kaupungin"),("kaupunki","sg part","kaupunkia"),
 ("kaupunki","pl part","kaupunkeja"),("kaupunki","sg illat","kaupunkiin"),
 ("aurinko","sg gen","auringon"),("aurinko","sg part","aurinkoa"),
 ("aurinko","sg illat","aurinkoon"),("aurinko","pl part","aurinkoja"),
 ("ilta","sg gen","illan"),("ilta","sg part","iltaa"),("ilta","pl part","iltoja"),
 ("ilta","sg illat","iltaan"),
 ("koira","sg gen","koiran"),("koira","pl part","koiria"),
 ("kirja","sg gen","kirjan"),("kirja","pl part","kirjoja"),
 ("opettaja","pl part","opettajia"),("opettaja","sg part","opettajaa"),
 ("vesi","sg gen","veden"),("vesi","sg part","vettä"),("vesi","pl part","vesiä"),
 ("vesi","sg illat","veteen"),
 ("käsi","sg gen","käden"),("käsi","sg part","kättä"),("käsi","pl part","käsiä"),
 ("lapsi","sg part","lasta"),("lapsi","pl gen","lasten lapsien"),
 ("mies","sg gen","miehen"),("mies","pl part","miehiä"),
 ("nainen","sg gen","naisen"),("nainen","sg part","naista"),("nainen","pl gen","naisten naisien"),
 ("hevonen","sg gen","hevosen"),("hevonen","pl part","hevosia"),
 ("vastaus","sg gen","vastauksen"),("vastaus","pl part","vastauksia"),
 ("kysymys","sg gen","kysymyksen"),("kysymys","pl part","kysymyksiä"),
 ("hame","sg gen","hameen"),("hame","sg part","hametta"),("hame","pl part","hameita"),
 ("huone","sg gen","huoneen"),("huone","sg part","huonetta"),("huone","pl part","huoneita"),
 ("vieras","sg gen","vieraan"),("vieras","sg part","vierasta"),("vieras","pl part","vieraita"),
 ("rikas","sg gen","rikkaan"),("rikas","sg part","rikasta"),
 ("maa","sg part","maata"),("maa","pl part","maita"),("maa","sg illat","maahan"),
 ("työ","sg part","työtä"),("työ","pl part","töitä"),
 ("kieli","sg gen","kielen"),("kieli","sg part","kieltä"),("kieli","pl part","kieliä"),
 ("pieni","sg part","pientä"),("pieni","pl gen","pienten pienien"),
 ("onneton","sg gen","onnettoman"),("onneton","pl part","onnettomia"),
 ("kevät","sg gen","kevään"),("kevät","sg part","kevättä"),
 ("väsynyt","sg gen","väsyneen"),("väsynyt","sg part","väsynyttä"),
 ("lyhyt","sg gen","lyhyen"),("lyhyt","sg part","lyhyttä"),
 ("kaksi","sg gen","kahden"),("kaksi","sg part","kahta"),
 ("perhe","sg gen","perheen"),("perhe","sg part","perhettä"),("perhe","pl part","perheitä"),
 ("silta","sg gen","sillan"),("silta","pl part","siltoja"),
 ("pöytä","sg gen","pöydän"),("pöytä","sg part","pöytää"),("pöytä","pl part","pöytiä"),
 ("kylä","sg gen","kylän"),("kylä","pl part","kyliä"),
 ("mansikka","sg gen","mansikan"),("mansikka","sg part","mansikkaa"),
 ("laatikko","sg gen","laatikon"),("laatikko","sg illat","laatikkoon"),
 ("kala","pl part","kaloja"),("kala","sg gen","kalan"),
 ("puhelin","sg gen","puhelimen"),("puhelin","sg part","puhelinta"),("puhelin","pl part","puhelimia"),
 ("sisar","sg gen","sisaren"),("sisar","sg part","sisarta"),
 ("kaupunkilainen","sg gen","kaupunkilaisen"),("kaupunkilainen","pl part","kaupunkilaisia"),
 ("työpaikka","sg gen","työpaikan"),("työpaikka","sg part","työpaikkaa"),
 ("isoäiti","sg part","isoäitiä"),
 ("ystävä","sg gen","ystävän"),("ystävä","pl part","ystäviä"),
 ("asia","pl part","asioita"),("asia","sg part","asiaa"),
 ("kirjasto","pl part","kirjastoja kirjastoita"),  # Kotus type 2 licenses both("kirjasto","sg gen","kirjaston"),
]
bad=[]
for w,slot,exp in CASES:
    d=derive(w)
    got=d["forms"][slot] if d.get("status")=="ok" else f"<{d.get('status')}>"
    if got!=exp: bad.append((w,slot,got,exp))
print(f"{len(CASES)-len(bad)}/{len(CASES)} hand-verified forms correct")
for b in bad: print(f"  MISMATCH {b[0]:<16}{b[1]:<10} got {b[2]!r}  expected {b[3]!r}")

# ---- full 15-case paradigm spot checks -----------------------------------
from decline import full_paradigm
FULL = [
 ("katto","inessive","katossa","katoissa"),("katto","essive","kattona","kattoina"),
 ("katto","abessive","katotta","katoitta"),("katto","adessive","katolla","katoilla"),
 ("katto","translative","katoksi","katoiksi"),
 ("vesi","inessive","vedessä","vesissä"),("vesi","essive","vetenä","vesinä"),
 ("vesi","adessive","vedellä","vesillä"),("vesi","abessive","vedettä","vesittä"),
 ("nainen","inessive","naisessa","naisissa"),("nainen","adessive","naisella","naisilla"),
 ("kaupunki","inessive","kaupungissa","kaupungeissa"),
 ("kaupunki","essive","kaupunkina","kaupunkeina"),
 ("maa","inessive","maassa","maissa"),("maa","adessive","maalla","mailla"),
 ("työ","inessive","työssä","töissä"),("työ","adessive","työllä","töillä"),
 ("vieras","inessive","vieraassa","vieraissa"),
 ("hame","inessive","hameessa","hameissa"),
 ("koira","inessive","koirassa","koirissa"),("koira","adessive","koiralla","koirilla"),
 ("kala","inessive","kalassa","kaloissa"),
 ("ilta","inessive","illassa","illoissa"),("ilta","essive","iltana","iltoina"),
 ("mies","inessive","miehessä","miehissä"),
 ("kieli","inessive","kielessä","kielissä"),
 ("takki","inessive","takissa","takeissa"),("takki","essive","takkina","takkeina"),
 ("pöytä","inessive","pöydässä","pöydissä"),("pöytä","essive","pöytänä","pöytinä"),
 ("opettaja","inessive","opettajassa","opettajissa"),
 ("vastaus","inessive","vastauksessa","vastauksissa"),
]
bad2=[]
for w,case,esg,epl in FULL:
    d=full_paradigm(w)
    row=next((r for r in d.get("paradigm",[]) if r[0]==case), None)
    if not row or row[1]!=esg or row[2]!=epl:
        bad2.append((w,case,row[1] if row else None,row[2] if row else None,esg,epl))
print(f"{len(FULL)-len(bad2)}/{len(FULL)} full-paradigm spot checks correct")
for b in bad2: print(f"  MISMATCH {b[0]:<12}{b[1]:<12} got {b[2]!r}/{b[3]!r}  expected {b[4]!r}/{b[5]!r}")
