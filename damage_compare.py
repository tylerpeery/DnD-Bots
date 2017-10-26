import numpy as np
import random
import matplotlib.pyplot as plt

SAtkModifier = 6wd
SDmgModifier = 4
BAtkModifier = 6+2
BDmgModifier = 4
ACmax = 30
swordDamTwoBonus = np.zeros(ACmax)
swordDamOneBonus = np.zeros(ACmax)
bowDamBonus = np.zeros(ACmax)
ratio = np.zeros(ACmax)
iterations = 1000

for AC in range(1, ACmax+1):

    # check for 2 swords with double damage
    swordDam, swordDamAgain = 0, 0
    for x in range(0, iterations):
        swordAttack = np.random.randint(1, 21, 1) + SAtkModifier
        if swordAttack >= AC:
            swordDam += np.random.randint(1,7,1)+SDmgModifier
        swordAttackAgain = np.random.randint(1, 21, 1)+SAtkModifier
        if swordAttackAgain >= AC:
            swordDamAgain += np.random.randint(1,7,1)+SDmgModifier
    swordDamTwoBonus[AC-1] = swordDam + swordDamAgain

    # check for 2 sword with one damage
    swordDam1, swordDam2 = 0, 0
    for x in range(0, iterations):
        swordAttack1 = np.random.randint(1,21,1)+SAtkModifier
        swordAttack2 = np.random.randint(1,21,1)+SAtkModifier
        if swordAttack1 >= AC:
            swordDam1 += np.random.randint(1,7,1)+SDmgModifier
        if swordAttack2 >= AC:
            swordDam2 += np.random.randint(1,7,1)
    swordDamOneBonus[AC-1] = swordDam1 + swordDam2

    # check for bow damage
    bowDam = 0
    for x in range(0, iterations):
        bowAttack = np.random.randint(1,21,1)+BAtkModifier
        if bowAttack >= AC:
            bowDam += np.random.randint(1,9,1)+BDmgModifier
    bowDamBonus[AC-1] = bowDam

    # check ratio between the contenders
    ratio[AC-1] = swordDamTwoBonus[AC-1]/(bowDamBonus[AC-1]+1)

AC = range(1, ACmax+1)
plt.plot(AC, swordDamOneBonus, label="OneSwordBonus")
plt.plot(AC, swordDamTwoBonus, label="TwoSwordBonus")
plt.plot(AC, bowDamBonus, label="BowBonus")
plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3,
           ncol=2, mode="expand", borderaxespad=0.)
plt.show()

plt.plot(AC, ratio)
plt.show()