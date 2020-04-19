"""Dateinamen für PP02 FBu importieren."""
import os
from django.conf import settings
import PersonenDB.models as pDbModels
import KorpusDB.models as kDbModels


def pp02audiofilename0(doIt=False):
	"""Dateinamen für PP02 FBu importieren."""
	csvLines = open(os.path.join(getattr(settings, 'BASE_DIR', None), 'fxFunctions', 'pp02_audiofilename0.csv'), 'r', encoding="utf-8")
	dg = 0
	for csvLine in csvLines:
		if dg > 0 and len(csvLine.strip()) > 3:
			[aSigle, aDateiname, aFragebuch, aErhebungsId] = [x.strip() for x in csvLine.split(';')]
			aErhebungsId = int(aErhebungsId)
			aErhebungsElement = kDbModels.tbl_erhebungen.objects.filter(id=aErhebungsId)
			if aErhebungsElement.count() == 1:
				aSigleElement = pDbModels.tbl_informanten.objects.filter(inf_sigle=aSigle)
				if aSigleElement.count() == 1:
					aInferhebungElement = kDbModels.tbl_inferhebung.objects.filter(ID_Erh=aErhebungsElement[0], tbl_inf_zu_erhebung__ID_Inf=aSigleElement[0])
					if aInferhebungElement.count() == 1:
						aInferhebungElement = aInferhebungElement[0]
						if doIt:
							aInferhebungElement.Audiofile = aDateiname
							aInferhebungElement.save()
							print(dg, 'Erhebung Id:', aInferhebungElement.pk, 'aktuallisiert. Audiofile:', aDateiname)
						else:
							print(dg, 'Erhebung Id:', aInferhebungElement.pk, 'wuerde aktuallisiert. Audiofile:', aDateiname)
					else:
						print(dg, 'Einzel Erhebung wurde nicht eindeutig (', aInferhebungElement.count(), ') gefunden! Sigle:', str(aSigle).encode('ascii', 'ignore').decode("utf-8"), 'Erhebung:', str(aErhebungsId).encode('ascii', 'ignore').decode("utf-8"))
				else:
					print(dg, 'Informant wurde nicht eindeutig (', aSigleElement.count(), ') gefunden!', str(aSigle).encode('ascii', 'ignore').decode("utf-8"))
			else:
				print(dg, 'Erhebung wurde nicht eindeutig (', aErhebungsElement.count(), ') gefunden!', str(aErhebungsId).encode('ascii', 'ignore').decode("utf-8"))
		dg += 1
