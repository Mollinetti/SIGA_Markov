import Parameters, Game, Profile

p = Parameters.Params("Functions/test")

p1 = Profile.Profile(p)
p2 = Profile.Profile(p)

g = Game.Game(p, p1, p2)

p1,p2 = g.doGame()

print(p1.payoff)
print(p2.payoff)
