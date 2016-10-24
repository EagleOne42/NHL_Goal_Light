#!/bin/sh

api_url="http://live.nhle.com/GameData/RegularSeasonScoreboardv3.jsonp"
#game_id="2015021195"
#game_api="http://live.nhle.com/GameData/20152016/$game_id/gc/gcsb.jsonp"
#http://live.nhle.com/GameData/20152016/2015021195/gc/gcsb.jsonp

#Modify the jsonp file first to make in json format
#All games
#../jq-linux64 -r .games RegularSeasonScoreboardv3.jsonp | grep '\"id\"\|\"ts\"'
#Today only
#../jq-linux64 -r .games RegularSeasonScoreboardv3.jsonp | grep '\"id\"\|\"ts\"' | grep -B1 \"TODAY\"
#Output to copy into here
#jq-linux64 -r .games RegularSeasonScoreboardv3.jsonp | grep '\"id\"\|\"ts\"' | grep -B1 \"TODAY\" | grep id | sed 's/    "id": //g' | sed 's/,/ /g' | tr --delete '\n'

#STL v CHI
#GAME 1 - 2015030161

game_list="2015030175 2015030166"

while [ true ]
do
	echo "Pull Scoreboard"
	mkdir scoreboard/`date +%Y-%m-%d` 2>/dev/null
	curl http://live.nhle.com/GameData/RegularSeasonScoreboardv3.jsonp -H "{'Host': 'live.nhle.com', 'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.118 Safari/537.36', 'Referer': 'http://www.nhl.com/ice/scores.htm'}" -o scoreboard/`date +%Y-%m-%d`/`date +%Y-%m-%d_%T`.RegularSeasonScoreboardv3.jsonp

	for game_id in $game_list ; do
		echo "Pull Game ID: $game_id"
		mkdir $game_id 2>/dev/null
		curl http://live.nhle.com/GameData/20152016/$game_id/gc/gcsb.jsonp -H "{'Host': 'live.nhle.com', 'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.118 Safari/537.36', 'Referer': 'http://www.nhl.com/ice/scores.htm'}" -o $game_id/`date +%Y-%m-%d_%T`.gcsb.jsonp
	done
done

