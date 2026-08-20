#!/usr/bin/env python3
"""Closed-class Finnish words treated as known regardless of Anki state.

Pronouns, the negative verb, olla, and the highest-frequency particles are
grammatical infrastructure rather than vocabulary. They are mostly absent from
the Anki collection as headwords (or buried inside phrase cards), so without
this list the coverage checker penalises a text for containing the word "jotka".

Deliberately conservative: only closed classes and olla. Everything else has to
earn its place through the collection.
"""
PERSONAL = """
minä minun minua minut minussa minusta minuun minulla minulta minulle minuna minuksi
sinä sinun sinua sinut sinussa sinusta sinuun sinulla sinulta sinulle sinuna sinuksi
hän hänen häntä hänet hänessä hänestä häneen hänellä häneltä hänelle hänenä häneksi
me meidän meitä meidät meissä meistä meihin meillä meiltä meille
te teidän teitä teidät teissä teistä teihin teillä teiltä teille
he heidän heitä heidät heissä heistä heihin heillä heiltä heille
mä mun mua mut sä sun sua sut mä sä ne
itse itseni itsesi itsensä itseään itseäni toisensa toisiaan
"""
DEMONSTRATIVE = """
tämä tämän tätä tässä tästä tähän tällä tältä tälle tänä täksi
nämä näiden näitä näissä näistä näihin näillä näiltä näille näinä näiksi
tuo tuon tuota tuossa tuosta tuohon tuolla tuolta tuolle tuona tuoksi
nuo noiden noita noissa noista noihin noilla noilta noille noina noiksi
se sen sitä siinä siitä siihen sillä siltä sille sinä siksi sen
ne niiden niitä niissä niistä niihin niillä niiltä niille niinä niiksi
tää tän tota toi noi
"""
RELATIVE_INTERROG = """
joka jonka jota jossa josta johon jolla jolta jolle jona joksi
jotka joiden joita joissa joista joihin joilla joilta joille
mikä minkä mitä missä mistä mihin millä miltä mille minä miksi
mitkä miden mitä joita kuka kenen ketä kenessä kenestä keneen kenellä keneltä
kenelle ketkä keiden keitä kumpi kumman kumpaa kumpikaan kumpaakaan
millainen millaisen millaista miten milloin kuinka miksi kun jos että jotta
koska vaikka mutta ja tai sekä eli sillä kuitenkin siksi silti niin kuin
"""
NEGATION = """
en et ei emme ette eivät enkä etkä eikä emmekä ettekä eivätkä
älä älkää älköön älkäämme älkööt
kukaan ketään kenenkään kenellekään mikään mitään minkään missään mistään mihinkään
millään ei_kukaan
"""
OLLA = """
olla olen olet on olemme olette ovat ollut olleet oli olit olimme olitte olivat
ole olisi olisin olisit olisimme olisitte olisivat lienee ollessa oleva olleen
onko ovatko oliko eikö
"""
PARTICLES = """
myös vain jo vielä aina usein joskus harvoin ehkä varmasti tietysti kyllä
juuri melko aivan hyvin todella tosi noin lähes yhtä enää edes vasta heti
sitten nyt tänään eilen huomenna täällä siellä tuolla missä minne mistä
yli alle asti saakka ilman kanssa mukaan takia vuoksi jälkeen ennen aikana
paljon vähän liikaa enemmän vähemmän eniten mieluummin parhaiten
"""
FUNCTION_WORDS = set()
for block in (PERSONAL, DEMONSTRATIVE, RELATIVE_INTERROG, NEGATION, OLLA, PARTICLES):
    FUNCTION_WORDS |= {w for w in block.split() if w and "_" not in w}

if __name__ == "__main__":
    print(len(FUNCTION_WORDS), "function words")
