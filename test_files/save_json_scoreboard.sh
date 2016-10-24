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

#game_list="2015021199 2015021201 2015021200"
#game_list="2015021202 2015021203 2015021204 2015021205 2015021206 2015021207 2015021208 2015021209 2015021210 2015021211 2015021212 2015021213 2015021214"

#Friday - confirmed
#game_list="2015021215"
#Sat - confirmed
game_list="2015021216 2015021217 2015021218 2015021219 2015021220 2015021221 2015021222 2015021223 2015021224 2015021225 2015021226 2015021227 2015021228 2015021229 2015021230"

mkdir scoreboard 2>/dev/null

while [ true ]
do
	echo "Pull Scoreboard"
	curl http://live.nhle.com/GameData/RegularSeasonScoreboardv3.jsonp -H "{'Host': 'live.nhle.com', 'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.118 Safari/537.36', 'Referer': 'http://www.nhl.com/ice/scores.htm'}" -o scoreboard/`date +%Y-%m-%d_%T`.RegularSeasonScoreboardv3.jsonp

done

