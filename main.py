import pandas as pd
import math


def classify_shot(x: float, y: float):
    distanceFromHoop: float = math.sqrt(math.pow(x, 2) + math.pow(y, 2))

    if (y <= 7.8):
        if (distanceFromHoop >= 22):
            return "C3"
        else:
            return "2PT"
    else:
        if (distanceFromHoop >= 23.75):
            return "NC3"
        else:
            return "2PT"


if __name__ == '__main__':
    # load in data
    shotData = pd.read_csv(r'shots_data.csv')

    # run classification method using x and y coordinates
    shotData["shotType"] = shotData.apply(lambda x: classify_shot(x.x, x.y), axis=1)

    # creating filters
    teamA = (shotData["team"] == "Team A")
    teamB = (shotData["team"] == "Team B")
    isNC3 = (shotData["shotType"] == "NC3")
    isC3 = (shotData["shotType"] == "C3")
    is2pt = (shotData["shotType"] == "2PT")
    isBucket = (shotData["fgmade"] == 1)

    # get number of attemps
    AShotsAttempted: int = shotData[teamA]["shotType"].count()
    BShotsAttempted: int = shotData[teamB]["shotType"].count()

    # calculate 2pt distribution
    aTwoPtDist = (shotData[teamA & is2pt]["shotType"].count() / AShotsAttempted)
    bTwoPtDist = (shotData[teamB & is2pt]["shotType"].count() / BShotsAttempted)

    # calculate NC3 distrubution
    aNC3Dist = (shotData[teamA & isNC3]["shotType"].count() / AShotsAttempted)
    bNC3Dist = (shotData[teamB & isNC3]["shotType"].count() / BShotsAttempted)

    # calculate C3 distrubution
    aC3Dist = (shotData[teamA & isC3]["shotType"].count() / AShotsAttempted)
    bC3Dist = (shotData[teamB & isC3]["shotType"].count() / BShotsAttempted)

    # calculate effective 2pt %
    aTwoPtEfg = (shotData[teamA & is2pt & isBucket]["shotType"].count() / (shotData[teamA & is2pt]["shotType"].count()))
    bTwoPtEfg = (shotData[teamB & is2pt & isBucket]["shotType"].count() / (shotData[teamB & is2pt]["shotType"].count()))

    # calculate effective NC3 %
    aNC3Efg = ((shotData[teamA & isNC3 & isBucket]["shotType"].count() * 1.5) / (
        shotData[teamA & isNC3]["shotType"].count()))
    bNC3Efg = ((shotData[teamB & isNC3 & isBucket]["shotType"].count() * 1.5) / (
        shotData[teamB & isNC3]["shotType"].count()))

    # calculate effective C3 %
    aC3Efg = ((shotData[teamA & isC3 & isBucket]["shotType"].count() * 1.5) / (
        shotData[teamA & isC3]["shotType"].count()))
    bC3Efg = ((shotData[teamB & isC3 & isBucket]["shotType"].count() * 1.5) / (
        shotData[teamB & isC3]["shotType"].count()))

    # print out answers
    print("Team A:")
    print("\t2PT Distribution: \t" + str(aTwoPtDist.round(3)))
    print("\tNC3 Distribution: \t" + str(aNC3Dist.round(3)))
    print("\tC3 Distribution: \t" + str(aC3Dist.round(3)) + "\n")

    print("\t2PT eFG %:        \t" + str(aTwoPtEfg.round(3)))
    print("\tNC3 eFG %:        \t" + str(aNC3Efg.round(3)))
    print("\tC3 eFG %:        \t" + str(aC3Efg.round(3)))

    print("Team B:")
    print("\t2PT Distribution: \t" + str(bTwoPtDist.round(3)))
    print("\tNC3 Distribution: \t" + str(bNC3Dist.round(3)))
    print("\tC3 Distribution: \t" + str(bC3Dist.round(3)) + "\n")

    print("\t2PT eFG %:        \t" + str(bTwoPtEfg.round(3)))
    print("\tNC3 eFG %:        \t" + str(bNC3Efg.round(3)))
    print("\tC3 eFG %:        \t" + str(bC3Efg.round(3)))
