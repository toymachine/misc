print "250000 aflvr. 200000 annu"

a_rente = 5.2
a_jaren = 20
a_bedrag = 200000
a_anuiteit = 1000 #per maand

v_rente = 5.2
v_bedrag = 250000

aftrek_perc = 0.42

totaal_rente = 0

depot = 50000
depot_rente = 3.0 #netto na verm bel.

rest_schuld = v_bedrag + a_bedrag - depot

for i in range(a_jaren):
    a_r = a_bedrag * a_rente / 100.0
    v_r = v_bedrag * v_rente / 100.0
    totaal_rente += (a_r + v_r)
    aflossing = (a_anuiteit * 12) - a_r
    assert aflossing > 0
    bruto_maand = (v_r / 12.0)  + (a_r / 12.0) + (aflossing / 12.0)
    netto_maand = ((v_r / 12.0) * (1 - aftrek_perc)) + ((a_r / 12.0) * (1 - aftrek_perc)) + (aflossing / 12.0)
    print "%d, %d, %3.2f, %3.2f, %3.2f, %3.2f, %3.2f, %3.2f, %3.2f, %3.2f" % (i, v_bedrag, v_r, a_bedrag, a_r, aflossing, netto_maand, bruto_maand, depot, rest_schuld)
    a_bedrag = a_bedrag - aflossing
    depot = depot * (1.0 + depot_rente / 100.0)
    assert a_bedrag > 0

    rest_schuld = v_bedrag + a_bedrag - depot

print "rente betaald (netto)", totaal_rente * (1 - aftrek_perc), "rest schuld", rest_schuld

for i in range(10):
    print i + a_jaren, v_rente * rest_schuld / 100.0 / 12.0
