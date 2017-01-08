agent:
	g++ -Ofast -std=c++11 backup.cpp -o backup
	g++ -Ofast -std=c++11 decision.cpp -o decision

calibrate:
	python timingCreator.py

newgame: 
	rm depth

run:
	./decision