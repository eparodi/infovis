let genrePlaytimeChart;
let genreGamesChart;
let multiplayerChart;
let playedChart;
let dataCount;
let hoursPlayedNumber;
let moneyWastedNumber;
let achievementsEarnedNumber;

$(document).ready(() => {
    genrePlaytimeChart = dc.rowChart("#genrePlaytimeChart");
    genreGamesChart = dc.rowChart("#genreGamesChart");
    multiplayerChart = dc.pieChart("#multiplayerChart");
    playedChart = dc.pieChart("#playedChart");
    dataCount = dc.dataCount('.data-count');
    hoursPlayedNumber = dc.numberDisplay('#hoursPlayedNumber');
    moneyWastedNumber = dc.numberDisplay('#moneyWastedNumber');
    achievementsEarnedNumber = dc.numberDisplay('#achievementsEarnedNumber');

    d3.csv("data/steam_games_decorated._csv", (data) => {
        data = data.filter((data) => data["Genres"] !== "None");

        let ndx = crossfilter(data);
        let all = ndx.groupAll();

        let genre = ndx.dimension((d) => d["Genres"]);
        let multiplayer = ndx.dimension((d) => {
            if (d["Is Multiplayer"] == "True")
                return "Multi-Player";
            return "Single-Player"
        });
        let played = ndx.dimension((d) => {
            if (parseInt(d["Playtime Forever"]) !== 0)
                return "Played";
            return "Not Played"
        });

        let genreGroup = genre.group().reduce(
            (p, v) => {
                p.count += 1;
                p.playtime += parseInt(v["Playtime Forever"]);
                return p;
            },
            (p, v) => {
                p.count -= 1;
                p.playtime -= parseInt(v["Playtime Forever"]);
                return p;
            },
            () => {
                return {
                    count: 0,
                    playtime: 0
                }
            }
        );
        let multiplayerGroup = multiplayer.group();
        let playedGroup = played.group();

        hoursPlayedNumber
            .valueAccessor((d) => d / 60)
            .group(ndx.groupAll().reduceSum((d) => parseInt(d["Playtime Forever"])));

        moneyWastedNumber
            .valueAccessor((d) => d)
            .group(ndx.groupAll().reduceSum((d) => d["Price"]));

        achievementsEarnedNumber
            .valueAccessor((d) => d)
            .group(ndx.groupAll().reduceSum((d) => d["Earned Achievements"]));

        dataCount
            .dimension(ndx)
            .group(all);

        genrePlaytimeChart
            .width(500)
            .height(800)
            .dimension(genre)
            .group(genreGroup)
            .elasticX(true)
            .title((d) => Math.floor(d.value.playtime) / 60 + ":" + d.value.playtime % 60)
            .valueAccessor((d) => d.value.playtime)
            .ordering((d) => - d.value.playtime);

        genreGamesChart
            .width(500)
            .height(800)
            .dimension(genre)
            .group(genreGroup)
            .elasticX(true)
            .title((d) => d.value.count + " games")
            .valueAccessor((d) => d.value.count)
            .ordering((d) => - d.value.count);

        multiplayerChart
            .width(500)
            .height(500)
            .innerRadius(80)
            .radius(200)
            .minAngleForLabel(0)
            .dimension(multiplayer)
            .externalLabels(50)
            .externalRadiusPadding(60)
            .drawPaths(true)
            .group(multiplayerGroup);

        playedChart
            .width(500)
            .height(500)
            .innerRadius(80)
            .radius(200)
            .minAngleForLabel(0)
            .dimension(played)
            .externalLabels(50)
            .externalRadiusPadding(60)
            .drawPaths(true)
            .group(playedGroup);

        dc.renderAll();
    });
    
});