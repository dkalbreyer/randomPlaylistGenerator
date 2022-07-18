BRANCH_NAME = newBranch

newbranch:
	@echo "Aktuelle Version vom Server holen"
	git pull
	@echo "Neuen Branch anlegen mit Namen: $(BRANCH_NAME)"
	git checkout -b $(BRANCH_NAME) main

	@echo "Wenn die Aenderungen vollzogen sind bitte folgende Befehle nacheinander eingeben: "
	@echo "1. add ."
	@echo "2. git commit -m Beschreibung der Aenderungen"
	@echo "3. make mergebranch"

mergebranch:
	@echo "Zurueck zum Master wechseln"
	git checkout main
	@echo "Sicherheitshalber nochmal die aktuelle Version vom Server holen"
	git pull
	@echo "Den Branch mit dem Master zusammenfuehren"
	git merge $(BRANCH_NAME)
	@echo "Den Branch loeschen"
	git branch -d $(BRANCH_NAME)
	@echo "Den neuen Master auf den Server pushen"
	git push
